from django.db import models
from django.db.models import Count, Q

from article.models import Article, Comment
from authapp.models import User


class Notification(models.Model):
    """Модель уведомлений юзера о различных изменениях касаемо его контента"""

    MODERATOR = 'Отклонено модератором!'
    LIKE = 'Лайк на статью'
    DISLIKE = 'Дизлайк на статью'
    NEW_COMMENT = 'Новый комментарий'
    RM_ARTICLE = "Снято с публикации"
    DEL_COMMENT = 'Комментарий удален'
    PUBLISH = 'Статья опубликована'
    RESTORE = 'Cтатья восстановлена'
    COMMENT_LIKE = 'Лайк на коммент'
    COMMENT_DISLIKE = 'Дизлайк на коммент'
    COMMENT_REPLY = 'Ответ на коммент'

    TYPE_CHOICES = (
        (MODERATOR, 'Отклонено модератором!'),
        (LIKE, 'Лайк на статью'),
        (DISLIKE, 'Дизлайк на статью'),
        (NEW_COMMENT, 'Новый комментарий'),
        (RM_ARTICLE, 'Снято с публикации'),
        (DEL_COMMENT, 'Комментарий удален'),
        (PUBLISH, 'Статья опубликована'),
        (RESTORE, 'Статья восстановлена'),
        (COMMENT_LIKE, 'Лайк на коммент'),
        (COMMENT_DISLIKE, 'Дизлайк на коммент'),
        (COMMENT_REPLY, 'Ответ на коммент'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='Комментарий', null=True)
    read = models.BooleanField(verbose_name='Прочитано', default=False, db_index=True)
    type_of = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='тип', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def clear_all(user_pk):
        Notification.objects.filter(user=user_pk, read=False).update(read=True)

    def clear(self):
        self.read = True
        self.save()

    @staticmethod
    def total_count(user_pk):
        return Notification.objects.filter(user=user_pk).count()

    @staticmethod
    def total_unread_count(user_pk):
        return Notification.objects.filter(user=user_pk, read=False).count()

    @staticmethod
    def get_unread(user_pk):
        return Notification.objects.filter(user=user_pk, read=False).order_by('-created_at')

    @staticmethod
    def get_all(user_pk):
        return Notification.objects.filter(user=user_pk).order_by('-created_at')

    @classmethod
    def add_notice(cls, type_of, target=None, comment=None):
        if target:
            cls.objects.create(user=target.user, target=target, type_of=type_of).save()
        elif comment:
            cls.objects.create(user=comment.user, target=comment.article, comment=comment, type_of=type_of).save()

    @classmethod
    def get_new_comments_articles(cls, user):
        return Article.objects.filter(user=user).annotate(
            num_notices=Count('notification', filter=Q(notification__type_of=cls.NEW_COMMENT) & Q(
                notification__read=False))) \
            .filter(num_notices__gt=0).order_by('-num_notices')

    @classmethod
    def get_new_comments_reply(cls, user):
        return Comment.objects.filter(user=user).annotate(
            num_notices=Count('notification', filter=Q(notification__type_of=cls.COMMENT_REPLY) & Q(
                notification__read=False))) \
            .filter(num_notices__gt=0).order_by('-num_notices')

    @classmethod
    def get_new_liked_articles(cls, user):
        return Article.objects.filter(user=user).annotate(
            num_likes=Count('notification',
                            filter=Q(notification__type_of=cls.LIKE) & Q(notification__read=False))) \
            .filter(num_likes__gt=0).order_by('-num_likes')

    @classmethod
    def get_new_disliked_articles(cls, user):
        return Article.objects.filter(user=user).annotate(
            num_dislikes=Count('notification',
                               filter=Q(notification__type_of=cls.DISLIKE) & Q(notification__read=False))) \
            .filter(num_dislikes__gt=0).order_by('-num_dislikes')

    @classmethod
    def get_new_liked_comments(cls, user):
        return Comment.objects.filter(user=user).annotate(
            num_likes=Count('notification',
                            filter=Q(notification__type_of=cls.COMMENT_LIKE) & Q(notification__read=False))) \
            .filter(num_likes__gt=0).order_by('-num_likes')

    @classmethod
    def get_new_disliked_comments(cls, user):
        return Comment.objects.filter(user=user).annotate(
            num_dislikes=Count('notification',
                               filter=Q(notification__type_of=cls.COMMENT_DISLIKE) & Q(notification__read=False))) \
            .filter(num_dislikes__gt=0).order_by('-num_dislikes')

    @classmethod
    def get_article_notices(cls, article):
        return Notification.objects.filter(target=article, type_of__in=(cls.LIKE, cls.DISLIKE, cls.NEW_COMMENT))

    @classmethod
    def get_article_comment_notices(cls, comment):
        return Notification.objects.filter(comment=comment, type_of__in=(cls.COMMENT_LIKE, cls.COMMENT_DISLIKE,
                                                                         cls.COMMENT_REPLY))
