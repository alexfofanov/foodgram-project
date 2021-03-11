from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)


admin.site.register(User, UserAdmin)
