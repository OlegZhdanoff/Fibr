from django.db import models

from article.models import Article, Comment
from authapp.models import User


class Complaint(models.Model):
    """Модель системы жалоб на пользователей, статьи и комментарии"""

    USER = 'Жалоба на пользователя'
    ARTICLE = 'Жалоба на статью'
    COMMENT = 'Жалоба на комментарий'

    TYPE_CHOICES = (
        (USER, 'Жалоба на пользователя'),
        (ARTICLE, 'Жалоба на статью'),
        (COMMENT, 'Жалоба на комментарий'),
    )

    ACTIVE = 'На рассмотрении'
    ACCEPTED = 'Принята'
    DECLINE = 'Отклонена'

    STATUS = (
        (ACTIVE, 'На рассмотрении'),
        (ACCEPTED, 'Принята'),
        (DECLINE, 'Отклонена')
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomplaint')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий', null=True)
    type_of = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип', db_index=True)
    status = models.CharField(max_length=50, choices=STATUS, default=ACTIVE, verbose_name='Статус', db_index=True)
    text = models.TextField(verbose_name='Текст')
    text_moderator = models.TextField(blank=True, verbose_name='Ответ модератора')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, owner, target, type_of, text):
        obj = None
        if type_of == cls.USER:
            obj = cls.objects.create(owner=owner, user=target, type_of=type_of, text=text)
        elif type_of == cls.ARTICLE:
            obj = cls.objects.create(owner=owner, article=target, type_of=type_of, text=text)
        elif type_of == cls.COMMENT:
            obj = cls.objects.create(owner=owner, comment=target, type_of=type_of, text=text)
        if obj:
            obj.save()
        return obj
