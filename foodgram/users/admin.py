from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(User)


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)


admin.site.register(User, UserAdmin)
