from django.contrib import admin
from account.models import Profile, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Register profile admin"""
    list_display = ('id', 'user')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Contact admin"""
    ...