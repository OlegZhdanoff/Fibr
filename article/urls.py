from django.urls import path

import article.views as article

app_name = 'article'

urlpatterns = [
    path('<int:pk>/', article.ArticleView.as_view(), name='article'),
    path('create/', article.ArticleCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', article.ArticleEditView.as_view(), name='edit'),
    path('comment_article/<int:pk>/', article.article_comment, name='comment_article'),

    path('like/<int:pk>', article.article_like, name='like_article'),
    path('publish/<int:pk>', article.article_publish, name='publish'),
    path('unpublish/<int:pk>', article.article_unpublish, name='unpublish'),
    path('delete/<int:pk>', article.article_delete, name='delete'),
    path('decline/<int:pk>', article.article_decline, name='decline'),
    path('moderate/<int:pk>', article.article_moderate, name='moderate'),

    path('like/comment/<int:pk>/', article.comment_like, name='like_comment'),

    path('comment/reply/<int:pk>', article.comment_reply, name='reply_comment'),

    path('search/', article.SearchResultsView.as_view(), name='search_results'),

]
