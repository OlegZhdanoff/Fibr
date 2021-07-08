from django.urls import path

import article.views as article

app_name = 'article'

urlpatterns = [
    path('<int:pk>/', article.ArticleView.as_view(), name='article'),
    path('create/', article.ArticleCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', article.ArticleEditView.as_view(), name='edit'),

    path('like/<int:pk>', article.article_like, name='like_article'),
    path('toggle/<int:pk>', article.article_toggle, name='toggle'),
    path('delete/<int:pk>', article.article_delete, name='delete'),

]
