from django.contrib import admin
from api.user.models import User, Profile, ProfileImage, Keyword, Hobby, Match
from django import forms


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'email',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('phone', 'email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('kind', 'code', 'user', 'firebase_token',)


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile',)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile1', 'profile2')
