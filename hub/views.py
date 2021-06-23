from django.views.generic import DetailView

from hub.models import Topic


class TopicView(DetailView):
    model = Topic
    template_name = 'hub/hub.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
