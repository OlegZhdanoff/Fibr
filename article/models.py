from django.db import models
from authapp.models import User
from hub.models import Topic


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='Раздел')
    title = models.CharField(max_length=64, unique=True, verbose_name='Название')
    content = models.TextField(blank=True, verbose_name='Статья')
    image = models.ImageField(upload_to='article_images', blank=True, verbose_name='Фото')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    @staticmethod
    def get_user_articles(user):
        return Article.objects.filter(user=user)

    def get_total_likes(self):
        """Возвращает количество лайков для текущей статьи"""
        likes = Like.objects.filter(article=self, is_liked=True)

        return len(likes)

    def set_like(self, user):
        """Создает запись лайка или меняет свойство is_liked для существующей"""
        like_object = Like.objects.filter(article=self, user=user)

        if like_object:
            like_object[0].switch_like()
            print(f"debug {like_object[0].id}\nstate: {like_object[0].is_liked}")

        else:
            Like.objects.create(article=self, user=user)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)

    @staticmethod
    def get_users_article_liked(article):
        likes = Like.objects.filter(article=article, is_liked=True)
        users = [like.user for like in likes]
        return users

    def switch_like(self):
        """Меняет значение is_liked на противоположное"""
        self.is_liked = not self.is_liked
        self.save()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
