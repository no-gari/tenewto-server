# Generated by Django 4.2 on 2024-09-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='uploads/', verbose_name='첨부파일'),
        ),
    ]