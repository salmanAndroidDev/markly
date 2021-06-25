from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from images.models import Image


@receiver(m2m_changed, sender=Image.likes.through)
def user_like_change(sender, instance, **kwargs):
    """Sync total_likes field the same size with likes"""
    instance.total_likes = instance.likes.count()
    instance.save()
