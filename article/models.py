from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    name = models.CharField(max_length=64)
    short_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='article_images', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

