from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'role')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    ordering = ('username',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.role == 'UserAdmin':
                    return True
        return False

class ProfileAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
       
    list_display = ('user', 'name', 'date_of_birth', 'loyalty_points')
    list_filter = ('user__role',)
    search_fields = ('user__username', 'name')
    ordering = ('user__username',)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            if not request.user.is_anonymous:
                if request.user.role == 'CinemaManager':
                    return False
                if request.user.role == 'UserAdmin':
                    return True
        return False

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)