from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView

from article.models import Article
from hub.models import Topic


class Index(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorting'] = self.request.GET.get('sorting', settings.SORTING.NEWEST)
        # context['sorting'] = self.kwargs.get('sorting', settings.SORTING.NEWEST)

        context['articles'] = Article.get_articles(sorting=context['sorting'])

        return context
