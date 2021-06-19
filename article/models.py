from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField


class Subject(models.Model):
    class Meta:
        db_table = "Тематика" #название таблицы в БД

    subject_name = models.CharField(max_length=100) #название тематики
    subject_description = TextField() # описание тематики

    def __str__(self):
        return self.subject_name


class Article(models.Model):
    class Meta:
        db_table = "Статьи" #название таблицы в БД

    article_user = models.ForeignKey(User, on_delete=models.CASCADE) # имя пользователя
    article_subject = models.ForeignKey(Subject, on_delete=models.CASCADE) # привязка к тематике
    article_name = models.CharField(max_length=100) # имя стати
    article_content = TextField() # текст статьи
    article_date = models.DateTimeField('Время создания статьи')

    def __str__(self):
        return self.article_name
