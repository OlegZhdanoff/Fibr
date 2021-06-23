from hub.models import Topic


# Добавляет в контекст меню категорий(хабов)
def topic_list(request):
    return {"topic_list": Topic.objects.all()}
