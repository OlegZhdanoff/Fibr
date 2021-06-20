from django.views.generic import ListView

from hub.models import Topic


# Копипаст тут для MVP. В будущем можно сделать просмотр всех хабов через одну вьюху
class DesignView(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Дизайн'
        context['article'] = 'Дизайн'

        return context


class WebDevView(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Веб-разработка'
        context['article'] = 'Веб-разработка'

        return context


class AdministrationView(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Администрирование'
        context['article'] = 'Администрирование'

        return context


class ManagementView(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Менеджмент'
        context['article'] = 'Менеджмент'

        return context


class MarketingView(ListView):
    model = Topic
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Маркетинг'
        context['article'] = 'Маркетинг'

        return context
