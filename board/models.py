from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=100, verbose_name='성명')
    phone = models.CharField(max_length=15, verbose_name='성명')
    birthday = models.DateField(verbose_name='생년월일')
    email = models.EmailField(verbose_name='이메일')
    art_name1 = models.CharField(max_length=100, verbose_name='성명')
    art_name2 = models.CharField(max_length=100, verbose_name='성명', null=True, blank=True)
    art_name3 = models.CharField(max_length=100, verbose_name='성명', null=True, blank=True)
    art_name4 = models.CharField(max_length=100, verbose_name='성명', null=True, blank=True)
    art_name5 = models.CharField(max_length=100, verbose_name='성명', null=True, blank=True)
    application = models.FileField(upload_to='files/', verbose_name='참가 신청서', null=True, blank=True)
    image1 = models.ImageField(upload_to='photos/', verbose_name='이미지1')
    image2 = models.ImageField(upload_to='photos/', verbose_name='이미지2', null=True, blank=True)
    image3 = models.ImageField(upload_to='photos/', verbose_name='이미지3', null=True, blank=True)
    image4 = models.ImageField(upload_to='photos/', verbose_name='이미지4', null=True, blank=True)
    image5 = models.ImageField(upload_to='photos/', verbose_name='이미지5', null=True, blank=True)
    when = models.DateField(verbose_name='촬영일시')
    where = models.CharField(max_length=200, verbose_name='촬영장소')
    explanation = models.TextField(verbose_name='설명')
    fixed = models.TextField(verbose_name='보정 내용')
    applied_at = models.DateTimeField(verbose_name='제출 일시', auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = '공모전 지원 내역'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name} - 의 작품'


class ApplyAvailable(models.Model):
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = '지원 가능 여부'
        verbose_name_plural = verbose_name


class Board(models.Model):
    title = models.CharField(max_length=255, verbose_name='제목')
    description = models.TextField(verbose_name='설명')
    file_upload = models.FileField(upload_to='uploads/', verbose_name='첨부파일', null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='작성 일시', auto_now_add=True)
    writer = models.CharField(max_length=255, verbose_name='작성자')

    class Meta:
        verbose_name = '공지사항'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
