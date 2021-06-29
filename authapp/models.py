from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# from article.models import ArticleView


class User(AbstractUser):
    image = models.ImageField(upload_to='users_avatars', blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

    def get_age(self):
        pass


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    # article = models.OneToOneField(ArticleView, blank=True)
    article = models.TextField(blank=True, max_length=512, verbose_name='обо мне')
    about_me = models.TextField(blank=True, max_length=512, verbose_name='обо мне')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='пол')

    @receiver(post_save, sender=User)
    def create_user_profile(self, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, instance,  **kwargs):
        instance.userprofile.save()
