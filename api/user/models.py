from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils.translation import gettext_lazy as _
from api.helpers import get_conversation_between
from api.utils import FilenameChanger
from django.utils import timezone
from api.chat.models import Chat
from django.db.models import Q
from model_utils import Choices
from django.db import models
import uuid


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    username = None
    email = models.EmailField(verbose_name=_('이메일'), unique=True)
    phone = models.CharField(verbose_name=_('휴대폰'), max_length=11, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    VERIFY_FIELDS = []
    REGISTER_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    @property
    def is_social(self):
        return hasattr(self, 'social')


class Keyword(models.Model):
    title = models.CharField(verbose_name=_('키워드'), max_length=16, null=True, blank=True)

    class Meta:
        verbose_name = '키워드'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Hobby(models.Model):
    title = models.CharField(verbose_name=_('취미'), max_length=16, null=True, blank=True)

    class Meta:
        verbose_name = '취미'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Profile(models.Model):
    GENDER_CHOICES = Choices(
        ("M", "남성"),
        ("W", "여성"),
    )
    RELIGION_CHOICES = Choices(
        ('noreligion', '무교'),
        ('christianity', '기독교'),
        ('buddism', '불교'),
        ('catholicism', '천주교'),
        ('other', '기타'),
        ('noshow', '밝히기 싫어'),
    )
    SMOKE_CHOICES = Choices(
        ('no', '비흡연자'),
        ('yes', '흡연자'),
        ('electronic', '전자담배'),
    )
    SCHOOL_CHOICES = Choices(
        ('a', '학사'),
        ('d', '석사'),
        ('e', '기타'),
    )
    JOB_CHOICES = Choices(
        ('a', '학생'),
        ('b', '직장인'),
        ('c', '프리랜서/창업'),
        ('d', '준비 중'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, verbose_name=_('닉네임'), null=True, blank=True)
    avatar = models.ImageField(verbose_name=_('아바타'), null=True, blank=True, upload_to=FilenameChanger('profile'))
    created_at = models.DateTimeField(verbose_name=_('생성 일자'), auto_now_add=True, null=True, blank=True)
    kind = models.CharField(max_length=32, verbose_name=_('종류'), null=True, blank=True)
    code = models.CharField(max_length=1024, verbose_name=_('SNS 고유 코드'), null=True, blank=True)
    points = models.PositiveIntegerField(default=0, verbose_name=_('포인트'), null=True, blank=True)
    firebase_token = models.CharField(max_length=1024, verbose_name=_('파이어베이스 토큰'), null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('위도'), null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('경도'), null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True, verbose_name=_('생일'))
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('나이'))
    city = models.TextField(max_length=15, null=True, blank=True, verbose_name=_('도시'))
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.M,
        max_length=1,
        verbose_name=_('성별')
    )
    blocked_profiles = models.ManyToManyField(
        "self", symmetrical=False, related_name="blocked_by", blank=True, verbose_name=_('차단한 프로필')
    )
    religion = models.CharField(max_length=32, choices=RELIGION_CHOICES, default='other', verbose_name=_('종교'))
    smoke = models.CharField(max_length=32, choices=SMOKE_CHOICES, default='no', verbose_name=_('흡연 여부'))
    height = models.IntegerField(verbose_name=_('키'), null=True, blank=True)
    mbti = models.CharField(max_length=4, verbose_name=_('MBTI'), null=True, blank=True)
    keywords = models.ManyToManyField(Keyword, verbose_name=_('키워드'), blank=True)
    job = models.CharField(max_length=1, choices=JOB_CHOICES, verbose_name=_('직업'), null=True, blank=True)
    job_detail = models.CharField(max_length=32, verbose_name=_('직장 명'), null=True, blank=True)
    school_level = models.CharField(max_length=1, verbose_name=_('학력'), choices=SCHOOL_CHOICES, null=True, blank=True)
    school_name = models.CharField(max_length=32, verbose_name=_('학교 이름'), null=True, blank=True)
    school_major = models.CharField(max_length=32, verbose_name=_('학교 전공'), null=True, blank=True)

    def block_profile(self, blocked_profile):
        # Remove likes between
        self.likes.remove(blocked_profile)
        blocked_profile.likes.remove(self)

        # Check for existing match between profiles and delete it
        match_qs = Match.objects.filter(
            Q(profile1=self, profile2=blocked_profile)
            | Q(profile1=blocked_profile, profile2=self)
        )
        if match_qs.exists():
            match_qs.delete()

        # check is there is any conversation between and delete it
        conversation = get_conversation_between(self, blocked_profile)
        if conversation:
            conversation.delete()

        self.blocked_profiles.add(blocked_profile)

    def delete(self, *args, **kwargs):
        chats = Chat.objects.filter(user_set=self)
        if chats.count() >= 1:
            for chat in chats:
                chat.delete()
        super().delete()

    class Meta:
        verbose_name = '프로필'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.email + '의 프로필'


class ProfileImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE, verbose_name=_('프로필'))
    profile_image = models.ImageField(
        verbose_name=_('프로필 이미지'), null=True, blank=True, upload_to=FilenameChanger('profile')
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('생성 시각'))

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=False)
        super().delete()

    class Meta:
        verbose_name = '프로필 이미지'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.profile.nickname + '의 이미지'


class SocialKindChoices(models.TextChoices):
    KAKAO = 'kakao', '카카오'
    APPLE = 'apple', '애플'


class EmailVerifier(models.Model):
    email = models.EmailField(verbose_name='이메일')
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')


class PhoneVerifier(models.Model):
    phone = models.CharField(verbose_name='휴대폰번호', max_length=11)
    code = models.CharField(verbose_name='인증번호', max_length=6)
    token = models.CharField(verbose_name='토큰', max_length=40)
    created = models.DateTimeField(verbose_name='생성일시')
