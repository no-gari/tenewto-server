# Generated by Django 4.2 on 2024-09-29 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_remove_application_explanation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='art_name1',
            field=models.CharField(max_length=100, verbose_name='작품1 제목'),
        ),
        migrations.AlterField(
            model_name='application',
            name='art_name2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='작품2 제목'),
        ),
        migrations.AlterField(
            model_name='application',
            name='art_name3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='작품3 제목'),
        ),
        migrations.AlterField(
            model_name='application',
            name='art_name4',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='작품4 제목'),
        ),
        migrations.AlterField(
            model_name='application',
            name='art_name5',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='작품5 제목'),
        ),
    ]
