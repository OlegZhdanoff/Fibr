from django.conf import settings
from django.views.generic import DetailView

from hub.models import Topic
from article.models import Article


class TopicView(DetailView):
    model = Topic
    template_name = 'hub/hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorting'] = self.request.GET.get('sorting', settings.SORTING.NEWEST)
        context['articles'] = Article.get_articles(topic=self.kwargs.get('pk'), sorting=context['sorting'])

        return context
