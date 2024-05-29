# Generated by Django 4.2 on 2024-05-30 01:26

import api.utils
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_emailverifier_id_alter_phoneverifier_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='나이'),
        ),
        migrations.AddField(
            model_name='profile',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='생일'),
        ),
        migrations.AddField(
            model_name='profile',
            name='blocked_profiles',
            field=models.ManyToManyField(blank=True, related_name='blocked_by', to='user.profile', verbose_name='차단한 프로필'),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.TextField(max_length=15, null=True, verbose_name='도시'),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', '남성'), ('W', '여성')], default='M', max_length=1, verbose_name='성별'),
        ),
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='위도'),
        ),
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='user.profile', verbose_name='좋아요한 프로필'),
        ),
        migrations.AddField(
            model_name='profile',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='경도'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nationality',
            field=models.TextField(max_length=20, null=True, verbose_name='국적'),
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=api.utils.FilenameChanger('profile'), verbose_name='프로필 사진')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='생성 시각')),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.profile', verbose_name='프로필')),
            ],
            options={
                'verbose_name': '프로필 이미지',
                'verbose_name_plural': '프로필 이미지',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='매칭 시각')),
                ('profile1', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile1_matches', to='user.profile', verbose_name='사용자1')),
                ('profile2', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile2_matches', to='user.profile', verbose_name='사용자2')),
            ],
            options={
                'verbose_name': '매칭',
                'verbose_name_plural': '매칭',
            },
        ),
    ]
