from rest_framework import serializers
from images.models import Image
from django.utils.text import slugify

from utils import download_image


class ImageCreateSerializer(serializers.ModelSerializer):
    """Image serializer to create an image"""

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')

    def validate_url(self, value):
        """Validate that url is image file with jpg or jpeg extensions"""
        valid_extensions = ('jpg', 'jpeg')
        extension = value.split('.')[-1].lower()
        if extension not in valid_extensions:
            raise serializers.ValidationError('Pick only jpg or jpeg urls')
        return value

    def save(self, **kwargs):
        """Overriding save method to create an appropriate Image instance"""
        image_url = self.validated_data['url']
        name = slugify(self.validated_data['title'])
        extension = image_url.split('.')[-1].lower()
        image_name = f"{name}.{extension}"

        # kwargs.update({'image': download_image(image_url)})

        image = super().save(**kwargs)
        image.image.save(image_name,
                         download_image(image_url),
                         save=False)
        return image.save()


class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer to retrieve, update, delete image,
    """

    class Meta:
        model = Image
        fields = ('user', 'title', 'slug', 'image', 'description', 'created', 'likes')
        read_only_fields = ('created',)
