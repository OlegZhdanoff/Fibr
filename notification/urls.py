from django.urls import path

import notification.views as notification

app_name = 'notification'

urlpatterns = [
    path('clear-all/', notification.clear_all, name='clear_all'),
    path('open-article/<int:pk>/', notification.open_article, name='open_article'),
    path('open-article-many/<int:pk>/', notification.open_article_with_many_notices, name='open_article_many'),
    path('open-article-comment-many/<int:pk>/', notification.open_article_comment_with_many_notices,
         name='open_article_comment_many'),
    path('edit-article/<int:pk>/', notification.edit_article, name='edit_article'),
]
