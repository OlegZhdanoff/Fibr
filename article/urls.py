from django.urls import path

import article.views as article

app_name = 'article'

urlpatterns = [
    path('', article.index, name='article'),
]
