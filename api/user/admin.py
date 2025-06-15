from django.contrib import admin
from api.user.models import User, Profile, ProfileImage, Keyword, Hobby
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
    pass


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    pass
