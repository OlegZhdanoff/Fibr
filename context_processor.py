from article.models import Article
from hub.models import Topic


# Добавляет в контекст меню категорий(хабов)
def topic_list(request):
    return {"topic_list": Topic.objects.all()}


def moderated_article_count(self):
    return {'moderated_articles_count': Article.get_moderated_articles().count()}
#     return 2
