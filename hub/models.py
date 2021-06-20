from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=64)
    short_description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Тематика'
        verbose_name_plural = 'Тематики'

    def __str__(self):
        return self.name
