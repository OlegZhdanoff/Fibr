from django.shortcuts import render
from django.views.generic import ListView

from hub.models import Topic


class Index(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fibr'
        context['article'] = 'Все потоки'

        return context
