from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from article.models import Comment
from notification.models import Notification


@login_required
def clear_all(request):
    Notification.clear_all(request.user.pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def del_all(request):
    Notification.del_all(request.user.pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def open_article(request, pk):
    notice = get_object_or_404(Notification, id=pk)
    notice.clear()
    return HttpResponseRedirect(reverse('article:article', kwargs={'pk': notice.target.pk}))


@login_required
def edit_article(request, pk):
    notice = get_object_or_404(Notification, id=pk)
    notice.clear()
    return HttpResponseRedirect(reverse('article:edit', kwargs={'pk': notice.target.pk}))


@login_required
def open_article_with_many_notices(request, pk):
    """открываем статью и очищаем все уведомления по новым лайкам/дизлайкам/комментариям для неё"""
    for notice in Notification.get_article_notices(pk):
        notice.clear()
    return HttpResponseRedirect(reverse('article:article', kwargs={'pk': pk}))


@login_required
def open_article_comment_with_many_notices(request, pk):
    """открываем статью со своим комментом и очищаем все уведомления по новым лайкам/дизлайкам/ответам для нашего
    комментария"""
    comment = get_object_or_404(Comment, id=pk)
    for notice in Notification.get_article_comment_notices(pk):
        notice.clear()
    return HttpResponseRedirect(reverse('article:article', kwargs={'pk': comment.article.pk}))
