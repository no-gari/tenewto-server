# Generated by Django 4.2 on 2024-09-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_applyavailable_alter_application_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='art_name',
            new_name='art_name1',
        ),
        migrations.AddField(
            model_name='application',
            name='art_name2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='성명'),
        ),
        migrations.AddField(
            model_name='application',
            name='art_name3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='성명'),
        ),
        migrations.AddField(
            model_name='application',
            name='art_name4',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='성명'),
        ),
        migrations.AddField(
            model_name='application',
            name='art_name5',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='성명'),
        ),
    ]
