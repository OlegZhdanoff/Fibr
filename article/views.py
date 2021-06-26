from django.views.generic import DetailView

from article.models import Article


class ArticleView(DetailView):
    model = Article
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(topic=self.kwargs.get('pk'))

        return context
