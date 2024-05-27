from django.db import models

from api.utils import FilenameChanger


class Chat(models.Model):
    user_set = models.ManyToManyField('user.User', verbose_name='참여자', blank=True)
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='수정일시', auto_now=True)

    class Meta:
        verbose_name = '채팅'
        verbose_name_plural = verbose_name
        ordering = ['-updated', '-created']

    def get_last_message(self):
        return self.message_set.first()


class MessageSenderTypeChoices(models.TextChoices):
    SENDER = 'S', '발신자'
    RECEIVER = 'R', '수신자'


class Message(models.Model):
    chat = models.ForeignKey('chat.Chat', verbose_name='채팅', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', verbose_name='유저', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='텍스트', null=True, blank=True)
    message_image = models.ImageField(verbose_name='메세지 이미지', null=True, blank=True, upload_to=FilenameChanger('message'))
    created = models.DateTimeField(verbose_name='생성일시', auto_now_add=True)

    class Meta:
        verbose_name = '메세지'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return self.text
