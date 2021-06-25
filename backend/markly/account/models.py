from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse


class Profile(models.Model):
    """
    Profile model which has one to one relationship with User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)

    photo = models.ImageField(upload_to=f'users/profile/%Y/%m/%d',
                              blank=True)

    def get_absolute_url(self):
        return reverse('account:detail', args=(self.id,))

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    """Contact is an intermediary model for ManyToMany relationship"""
    follow_from = models.ForeignKey('auth.User',
                                    related_name='rel_from_set',
                                    on_delete=models.CASCADE)
    follow_to = models.ForeignKey('auth.User',
                                  related_name='rel_to_set',
                                  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.follow_from} follow {self.follow_to}'


user_class = get_user_model()
user_class.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               symmetrical=False,
                                               related_name='followers'))
