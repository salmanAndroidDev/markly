from django.contrib import admin
from actions.models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    """Admin panel for action model"""
    list_display = ('user', 'verb', 'created', 'target')
    list_filter = ('created',)
    search_fields = ('verb',)
