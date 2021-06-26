from django.urls import path

import article.views as article

app_name = 'article'

urlpatterns = [
    path('<int:pk>/', article.ArticleView.as_view(), name='article'),
]
