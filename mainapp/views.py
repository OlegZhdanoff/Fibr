from django.shortcuts import render
from django.views.generic import ListView

from article.models import Article
from hub.models import Topic


class Index(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.get_articles().order_by('-created_at')[:3]

        return context

def index(request):
    return render(request, 'mainapp/index2.html')