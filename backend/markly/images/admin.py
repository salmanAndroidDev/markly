from django.contrib import admin
from images.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Admin panel for Image model"""
    list_display = ('id','title', 'slug', 'image', 'created')
    list_filter = ('created',)
