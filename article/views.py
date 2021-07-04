from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from article.forms import ArticleCreateForm, ArticleEditForm
from article.models import Article


class ArticleView(DetailView):
    model = Article
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(topic=self.kwargs.get('pk'))

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
    success_url = reverse_lazy('authapp:profile')
    success_msg = 'Статья успешно отредактирована'


def article_like(request, pk):
    """Вызывает метод set_like для статьи"""
    article = get_object_or_404(Article, id=request.POST.get('article_id'))
    article.set_like(user=request.user)

    return HttpResponseRedirect(reverse('article:article', args=[str(pk)]))
