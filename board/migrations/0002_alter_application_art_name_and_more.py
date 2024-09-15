# Generated by Django 4.2 on 2024-09-16 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='art_name',
            field=models.CharField(max_length=100, verbose_name='성명'),
        ),
        migrations.AlterField(
            model_name='application',
            name='birthday',
            field=models.DateField(verbose_name='생년월일'),
        ),
        migrations.AlterField(
            model_name='application',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='이메일'),
        ),
        migrations.AlterField(
            model_name='application',
            name='explanation',
            field=models.TextField(verbose_name='설명'),
        ),
        migrations.AlterField(
            model_name='application',
            name='fixed',
            field=models.TextField(verbose_name='보정 내용'),
        ),
        migrations.AlterField(
            model_name='application',
            name='image1',
            field=models.ImageField(upload_to='photos/', verbose_name='이미지1'),
        ),
        migrations.AlterField(
            model_name='application',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='이미지2'),
        ),
        migrations.AlterField(
            model_name='application',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='이미지3'),
        ),
        migrations.AlterField(
            model_name='application',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='이미지4'),
        ),
        migrations.AlterField(
            model_name='application',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='이미지5'),
        ),
        migrations.AlterField(
            model_name='application',
            name='name',
            field=models.CharField(max_length=100, verbose_name='성명'),
        ),
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='성명'),
        ),
        migrations.AlterField(
            model_name='application',
            name='when',
            field=models.DateField(verbose_name='촬영일시'),
        ),
        migrations.AlterField(
            model_name='application',
            name='where',
            field=models.CharField(max_length=200, verbose_name='촬영장소'),
        ),
    ]