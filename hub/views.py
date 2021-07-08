from django.views.generic import DetailView

from hub.models import Topic
from article.models import Article


class TopicView(DetailView):
    model = Topic
    template_name = 'hub/hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['articles'] = Article.objects.filter(topic=self.kwargs.get('pk'))
        context['articles'] = Article.get_articles().filter(topic=self.kwargs.get('pk')).order_by('-created_at')

        return context
