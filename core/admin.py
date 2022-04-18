from django.contrib import admin
from core.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ['email', 'first_name', 'last_name', 'username']
    exclude = ('password',)


admin.site.register(User, UserAdmin)
