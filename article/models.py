from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from django.db.models.expressions import CombinedExpression
from authapp.models import User
from hub.models import Topic


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Раздел')
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Статья')
    image = models.ImageField(upload_to='article_images', blank=True, verbose_name='Фото')
    is_active = models.BooleanField(default=True, verbose_name='Активна', db_index=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать', db_index=True)
    is_moderated = models.BooleanField(default=False, verbose_name='На модерацию', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    moderate_comment = models.TextField(blank=True, verbose_name='Замечания модератора')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    @staticmethod
    def get_user_articles(user):
        return Article.objects.filter(user=user, is_active=True)

    @classmethod
    def get_articles(cls, topic=None, sorting=settings.SORTING.NEWEST):
        if sorting == settings.SORTING.LIKED:
            return cls.get_articles_by_likes(topic)
        elif sorting == settings.SORTING.RATING:
            return cls.get_articles_by_rating(topic)
        elif sorting == settings.SORTING.COMMENTS:
            return cls.get_articles_by_comments(topic)

        if topic:
            return Article.objects.filter(is_active=True, is_published=True, topic=topic).\
                order_by('-created_at')
        else:
            return Article.objects.filter(is_active=True, is_published=True). \
                       order_by('-created_at')[:settings.MAX_ARTICLES_BY_PAGE]

    @staticmethod
    def get_moderated_articles():
        return Article.objects.filter(is_active=True, is_moderated=True)

    def get_total_likes(self):
        """Возвращает количество лайков для текущей статьи"""
        likes = Like.objects.filter(article=self, is_liked=True, is_for_comment=False)

        return len(likes)

    def get_total_dislikes(self):
        """Возвращает количество дизлайков для текущей статьи"""
        likes = Like.objects.filter(article=self, is_disliked=True, is_for_comment=False)

        return len(likes)

    def get_total_comments(self):
        """Возвращает количество комментариев к текущей статье"""
        comments = Comment.objects.filter(article=self)

        return len(comments)

    def get_comments(self):
        """Возвращает комментарии к текущей статье"""
        comments = Comment.objects.filter(article=self)

        return comments

    @property
    def rating(self):
        """Свойство рейтинг"""

        return self.get_total_likes() - self.get_total_dislikes()

    def get_total_views(self):
        """Возвращает количество просмотров к текущей статье"""

        article_views = ArticlesViews.objects.filter(article=self)

        return len(article_views)

    def set_like_state(self, user, like_action):
        """Создает запись лайка или меняет свойство is_liked для существующей"""
        like_object = Like.objects.filter(article=self, user=user)

        if like_object:
            like_object[0].switch_like(like_action)
            like_object[0].save()

        else:
            if like_action == 'like':
                Like.objects.create(article=self, user=user, is_liked=True)
            else:
                Like.objects.create(article=self, user=user, is_disliked=True)

    def decline(self, text):
        self.is_moderated = False
        self.is_published = False
        self.moderate_comment = text
        self.save()

    def set_moderate(self):
        self.is_moderated = True
        self.save()

    def leave_comment(self, user, text):
        """Создание нового комментария к статье"""
        Comment.objects.create(user=user, article=self, text=text)

    def unpublish(self):
        """Снимает статью с публикации"""
        self.is_published = False
        self.save()

    def publish(self):
        """Снимает статью с публикации"""
        self.is_published = True
        self.is_moderated = False
        self.moderate_comment = ''
        self.save()

    def toggle_hide(self):
        """Удаляет/восстанавливает статью"""
        self.is_active = not self.is_active
        self.save()

    def view(self, user):
        article_view = ArticlesViews.objects.filter(user=user, article=self)

        if not article_view:
            ArticlesViews.objects.create(user=user, article=self)

    @classmethod
    def get_articles_by_likes(cls, topic=None):
        if topic:
            return cls.objects.filter(topic=topic).annotate(
                num_likes=Count('like', filter=Q(like__is_liked=True) & Q(like__is_for_comment=False))). \
                order_by('-num_likes')
        else:
            return cls.objects.all().annotate(
                num_likes=Count('like', filter=Q(like__is_liked=True) & Q(like__is_for_comment=False))).\
                order_by('-num_likes')[:settings.MAX_ARTICLES_BY_PAGE]

    @classmethod
    def get_articles_by_rating(cls, topic=None):
        if topic:
            return cls.objects.filter(topic=topic).annotate(
                num_rating=(Count('like', filter=Q(like__is_liked=True) & Q(like__is_for_comment=False))
                            - Count('like', filter=Q(like__is_disliked=True) & Q(like__is_for_comment=False)))). \
                order_by('-num_rating')
        else:
            return cls.objects.all().annotate(
                num_rating=(Count('like', filter=Q(like__is_liked=True) & Q(like__is_for_comment=False))
                            - Count('like', filter=Q(like__is_disliked=True) & Q(like__is_for_comment=False)))). \
                order_by('-num_rating')[:settings.MAX_ARTICLES_BY_PAGE]

    @classmethod
    def get_articles_by_comments(cls, topic=None):
        if topic:
            return cls.objects.filter(topic=topic).annotate(
                num_comments=(Count('comment'))).order_by('-num_comments')
        else:
            return cls.objects.all().annotate(
                num_comments=(Count('comment'))).order_by('-num_comments')[:settings.MAX_ARTICLES_BY_PAGE]


class ArticlesViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_for_comment = models.BooleanField(default=False)

    @property
    def get_author_name(self):
        author_name = self.user.get_full_name()
        return author_name

    @property
    def get_author_avatar(self):
        author_avatar = self.user.image
        return author_avatar

    def get_total_likes(self):
        """Возвращает количество лайков для текущего коммента"""
        likes = CommentsLike.objects.filter(comment=self, is_liked=True)

        return len(likes)

    def get_total_dislikes(self):
        """Возвращает количество дизлайков для текущего коммента"""
        likes = CommentsLike.objects.filter(comment=self, is_disliked=True)

        return len(likes)

    def set_like_state(self, user, like_action):
        """Создает запись лайка коммента или меняет свойство is_liked для существующей"""
        like_object = CommentsLike.objects.filter(comment=self, user=user)

        if like_object:
            like_object[0].switch_like(like_action)
            like_object[0].save()

        else:
            if like_action == 'like':
                CommentsLike.objects.create(comment=self, article=self.article, user=user,
                                            is_liked=True, is_for_comment=True)
            else:
                CommentsLike.objects.create(comment=self, article=self.article, user=user,
                                            is_disliked=True, is_for_comment=True)

    @property
    def get_comments(self):
        comment_replies = CommentOnComment.objects.filter(comment=self)
        return comment_replies

    def reply_comment(self, user, text):
        CommentOnComment.objects.create(user=user, comment=self, text=text, article=self.article, is_for_comment=True)

    def delete_comment(self):
        current_comment = Comment.objects.get(pk=self.pk)
        current_comment.delete()


class CommentOnComment(Comment):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comments')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)
    is_for_comment = models.BooleanField(default=False)

    @staticmethod
    def get_users_article_liked(article):
        likes = Like.objects.filter(article=article, is_liked=True)
        users = [like.user for like in likes]
        return users

    def switch_like(self, like_action):
        """Меняет статус лайка/дизлайка"""
        if like_action == 'like':
            if self.is_like_set:
                self.cancel_liked()
            else:
                self.set_like()

        else:
            if self.is_dislike_set:
                self.cancel_liked()
            else:
                self.set_dislike()

    def set_like(self):
        """Срабатывает при нажатии на кнопку 'like'"""
        self.is_liked = True
        self.is_disliked = False

    def set_dislike(self):
        """Срабатывает при нажатии на кнопку 'dislike'"""
        self.is_liked = False
        self.is_disliked = True

    def cancel_liked(self):
        self.is_liked = False
        self.is_disliked = False

    @property
    def is_like_set(self):
        return self.is_liked and not self.is_disliked

    @property
    def is_dislike_set(self):
        return not self.is_liked and self.is_disliked


class CommentsLike(Like):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
