from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
from django.utils.translation import gettext_lazy as _


# Register your models here.


class MyUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('first_login', 'last_login', 'date_joined')}),
        # Additional fields
        (_('Additional info'), {'fields': ('user_photo', 'user_gender', 'bio')}),
    )


admin.site.register(MyUser, MyUserAdmin)
