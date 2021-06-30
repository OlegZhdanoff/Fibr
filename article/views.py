from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

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
        # context = self.get_context_data()
        form.instance.user = self.request.user
        # orderitems = context['orderitems']
        # basket_items = Basket.objects.filter(user=self.request.user)
        #
        # with transaction.atomic():
        #     basket_items.delete()
        #     form.instance.user = self.request.user
        #     self.object = form.save()
        #     if orderitems.is_valid():
        #         orderitems.instance = self.object
        #         orderitems.save()
        #
        #     if self.object.get_total_cost() == 0:
        #         self.object.delete()
        return super().form_valid(form)


class ArticleEditView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/article_edit.html'
    form_class = ArticleEditForm
    success_url = reverse_lazy('authapp:profile')
    success_msg = 'Статья успешно отредактирована'
