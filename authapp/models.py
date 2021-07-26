import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class User(AbstractUser):
    image = models.ImageField(upload_to='users_avatars', blank=True, default='users_avatars/default.jpg')
    birthday = models.DateField(blank=True, null=True)
    is_moderator = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    blocked_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def get_age(self):
        pass

    def is_not_blocked(self):
        # self.blocked_time = timezone.now() + timezone.timedelta(minutes=30)
        # self.save()
        # print(self.blocked_time)
        # print(self.username)
        if self.is_blocked and self.blocked_time < timezone.now():
            self.is_blocked = False
        return not self.is_blocked


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )

    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, max_length=512, verbose_name='обо мне')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='пол')

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()
