from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=100, verbose_name='성명')
    phone = models.CharField(max_length=15, verbose_name='성명')
    birthday = models.DateField(verbose_name='생년월일')
    email = models.EmailField(verbose_name='이메일')
    art_name = models.CharField(max_length=100, verbose_name='성명')
    image1 = models.ImageField(upload_to='photos/', verbose_name='이미지1')
    image2 = models.ImageField(upload_to='photos/', verbose_name='이미지2', null=True, blank=True)
    image3 = models.ImageField(upload_to='photos/', verbose_name='이미지3', null=True, blank=True)
    image4 = models.ImageField(upload_to='photos/', verbose_name='이미지4', null=True, blank=True)
    image5 = models.ImageField(upload_to='photos/', verbose_name='이미지5', null=True, blank=True)
    when = models.DateField(verbose_name='촬영일시')
    where = models.CharField(max_length=200, verbose_name='촬영장소')
    explanation = models.TextField(verbose_name='설명')
    fixed = models.TextField(verbose_name='보정 내용')

    def __str__(self):
        return f'{self.name} - {self.art_name}'
