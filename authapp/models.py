from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_avatars', blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

    def get_age(self):
        pass