from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from article.forms import ArticleCreateForm, ArticleEditForm
from article.models import Article, Comment, Like, CommentsLike
from notification.models import Notification


class ArticleView(DetailView):
    model = Article
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(article=self.kwargs.get('pk'), is_for_comment=False)

        return context
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
            article.view(user=self.request.user)
        return super().dispatch(*args, **kwargs)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article/article_create.html'
    form_class = ArticleCreateForm
    success_url = '/'
    success_msg = 'Статья успешно создана'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/article_edit.html'
    form_class = ArticleEditForm
    # success_url = reverse_lazy('auth:profile')
    success_msg = 'Статья успешно отредактирована'

    def get_success_url(self):
        return reverse_lazy('authapp:profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        """
        Called if all forms are valid. Creates a Author instance along
        with associated books and then redirects to a success page.
        """
        self.object = form.save()

        return HttpResponseRedirect(self.get_success_url())


@login_required(login_url='authapp:login')
def article_like(request, pk):
    """Вызывает метод set_like для статьи или редиректит на статью после авторизации"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=pk)
        like_action = request.POST.get('like_action')

        if not Like.objects.filter(article=article, user=request.user):
            if like_action == 'like':
                Notification.add_notice(target=article, type_of=Notification.LIKE)
            else:
                Notification.add_notice(target=article, type_of=Notification.DISLIKE)

        article.set_like_state(user=request.user, like_action=like_action)

    return HttpResponseRedirect(reverse('article:article', args=[str(pk)]))


@login_required(login_url='authapp:login')
def article_comment(request, pk):
    """Вызывает метод leave_comment для статьи или редиректит на статью после авторизации"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=pk)
        article.leave_comment(user=request.user, text=request.POST.get('text'))

        Notification.add_notice(target=article, type_of=Notification.NEW_COMMENT)

    return HttpResponseRedirect(reverse('article:article', args=[str(pk)]))


@login_required(login_url='authapp:login')
def article_publish(request, pk):
    """Модератор публикует статью автора"""
    article = get_object_or_404(Article, id=pk)
    article.publish()

    Notification.add_notice(target=article, type_of=Notification.PUBLISH)

    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]) + '#pills-article')


@login_required(login_url='authapp:login')
def article_unpublish(request, pk):
    """Модератор или автор снимает статью с публикации"""
    article = get_object_or_404(Article, id=pk)
    article.unpublish()

    if not request.user == article.user:
        Notification.add_notice(target=article, type_of=Notification.RM_ARTICLE)

    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]) + '#pills-article')


@login_required(login_url='authapp:login')
def article_moderate(request, pk):
    """Автор отправляет статью на модерацию"""
    article = get_object_or_404(Article, id=pk)
    article.set_moderate()
    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]) + '#pills-article')


@login_required(login_url='authapp:login')
def article_decline(request, pk):
    """Модератор отклоняет статью на модерации"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=pk)
        article.decline(request.POST.get('text'))

        Notification.add_notice(target=article, type_of=Notification.MODERATOR)

    return HttpResponseRedirect(reverse('auth:moderation'))


@login_required(login_url='authapp:login')
def article_delete(request, pk):
    """Автор удаляет статью / Админ восстанавливает"""
    article = get_object_or_404(Article, id=pk)
    article.toggle_hide()

    if not article.user == request.user:
        Notification.add_notice(target=article, type_of=Notification.RESTORE)

    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]) + '#pills-article')


@login_required(login_url='authapp:login')
def comment_like(request, pk):
    """Вызывает метод set_like для комментария или редиректит на статью после авторизации"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        like_action = request.POST.get('like_action')

        if not CommentsLike.objects.filter(comment=comment, user=request.user):
            if like_action == 'like':
                Notification.add_notice(comment=comment, type_of=Notification.COMMENT_LIKE)
            else:
                Notification.add_notice(comment=comment, type_of=Notification.COMMENT_DISLIKE)

        comment.set_like_state(user=request.user, like_action=like_action)
        article_id = comment.article.pk

        return HttpResponseRedirect(reverse('article:article', args=[str(article_id)]))

    return HttpResponseRedirect(reverse('mainapp:index'))


@login_required(login_url='authapp:login')
def comment_reply(request, pk):
    """Вызывает метод leave_comment для статьи или редиректит на статью после авторизации"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        comment.reply_comment(user=request.user, text=request.POST.get('text'))
        article_id = comment.article.pk

        if not comment.user == request.user:
            Notification.add_notice(comment=comment, type_of=Notification.COMMENT_REPLY)

        return HttpResponseRedirect(reverse('article:article', args=[str(article_id)]))

    return HttpResponseRedirect(reverse('mainapp:index'))


@login_required(login_url='authapp:login')
def comment_delete(request, pk):
    """Вызывает метод delete_comment для комментария"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=pk)
        article_id = comment.article.pk
        comment.delete_comment()        

    return HttpResponseRedirect(reverse('article:article', args=[str(article_id)]))
