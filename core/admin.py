from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Recipe,Tag

# customaize your admin panels here.
class CustomUserAdmin(UserAdmin):
    """User admin panel customization"""
    list_display = ('email','full_name')
    list_filter = ('is_staff',)
    search_fields = ('admin','full_name')
    ordering = ('full_name',)
    readonly_fields = ('last_login',)

    fieldsets =(
        (None, {'fields': ('email', 'password','full_name')}),
        ('Permissions',
         {'fields': ('last_login',
                     'groups',
                    'user_permissions')
         }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name', 'password1','password2'),
        }),
    )

    filter_horizontal = ('groups','user_permissions')

# register
admin.site.register(User,CustomUserAdmin)
admin.site.register(Recipe)
admin.site.register(Tag)