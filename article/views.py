from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from article.forms import ArticleCreateForm, ArticleEditForm
from article.models import Article, Comment


class ArticleView(DetailView):
    model = Article
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(topic=self.kwargs.get('pk'))
        context['comments'] = Comment.objects.filter(article=self.kwargs.get('pk'), is_for_comment=False)

        return context


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
        article.set_like_state(user=request.user, like_action=request.POST.get('like_action'))

    return HttpResponseRedirect(reverse('article:article', args=[str(pk)]))


@login_required(login_url='authapp:login')
def article_comment(request, pk):
    """Вызывает метод leave_comment для статьи или редиректит на статью после авторизации"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=pk)
        article.leave_comment(user=request.user, text=request.POST.get('text'))

    return HttpResponseRedirect(reverse('article:article', args=[str(pk)]))


@login_required(login_url='authapp:login')
def article_toggle(request, pk):
    """Публикует/Снимает статью с публикации"""
    article = get_object_or_404(Article, id=pk)
    article.toggle_publish()
    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]))


@login_required(login_url='authapp:login')
def article_decline(request, pk):
    """Публикует/Снимает статью с публикации"""
    article = get_object_or_404(Article, id=pk)
    article.is_moderated = False
    article.save()
    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]))


@login_required(login_url='authapp:login')
def article_delete(request, pk):
    """Удаляет/восстанавливает статью"""
    article = get_object_or_404(Article, id=pk)
    article.toggle_hide()
    return HttpResponseRedirect(reverse('auth:profile', args=[str(request.user.pk)]))


@login_required(login_url='authapp:login')
def comment_like(request, pk):
    """Вызывает метод set_like для комментария или редиректит на статью после авторизации"""
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=pk)
        comment.set_like_state(user=request.user, like_action=request.POST.get('like_action'))
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

        return HttpResponseRedirect(reverse('article:article', args=[str(article_id)]))

    return HttpResponseRedirect(reverse('mainapp:index'))
