from django.contrib import admin
from article.models import Article, Comment, Like, CommentsLike, CommentOnComment

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(CommentsLike)
admin.site.register(CommentOnComment)
