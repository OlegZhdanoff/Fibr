from django.urls import path

import article.views as article

app_name = 'article'

urlpatterns = [
    path('<int:pk>/', article.ArticleView.as_view(), name='article'),
    path('create-article/', article.ArticleCreateView.as_view(), name='article_create'),
    path('edit/<int:pk>/', article.ArticleEditView.as_view(), name='article_edit'),
]
