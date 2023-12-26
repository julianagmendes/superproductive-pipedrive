from django.contrib import admin
from user_management.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')


admin.site.register(CustomUser, CustomUserAdmin)