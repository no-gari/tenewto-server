# Generated by Django 4.2 on 2024-09-24 00:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_alter_board_writer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='explanation',
        ),
        migrations.RemoveField(
            model_name='application',
            name='when',
        ),
        migrations.RemoveField(
            model_name='application',
            name='where',
        ),
    ]
