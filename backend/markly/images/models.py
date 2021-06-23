from django.db import models
from django.conf import settings
from django.utils.text import slugify
from rest_framework.reverse import reverse


class Image(models.Model):
    """Image model to store images"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='images')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    likes = models.ManyToManyField('auth.User', related_name='liked_images',
                                   blank=True)

    def get_absolute_url(self):
        return reverse('images:retrieve', args=(self.id,))

    def save(self, *args, **kwargs):
        """auto-generate slug field"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
