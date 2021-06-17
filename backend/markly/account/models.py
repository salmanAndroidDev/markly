from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Profile model which has one to one relationship with User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    photo = models.ImageField(upload_to=f'users/profile/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return self.user.username