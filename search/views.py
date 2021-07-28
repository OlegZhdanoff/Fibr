from django.db.models import Q
from django.views.generic import ListView

from article.models import Article
from hub.models import Topic
from authapp.models import User


class SearchResultsView(ListView):
    model = Article
    template_name = 'search/search_result.html'

    def get_search_parameters(self):
        # Дает список Q-объектов с параметрами по заданным фильтрам
        search_parameters = []

        keyword = self.request.GET.get('keyword')
        topic = self.request.GET.get('topic')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        author = self.request.GET.get('author')

        if keyword:
            text_contain = Q(title__icontains=keyword) | Q(content__icontains=keyword)
            search_parameters.append(text_contain)

        if topic:
            topic = Topic.objects.filter(name__icontains=topic)
            topic_parameter = Q(topic=topic[0].id)
            search_parameters.append(topic_parameter)

        if start_date:
            start_date_parameter = Q(created_at__gte=start_date)
            search_parameters.append(start_date_parameter)

        if end_date:
            start_date_parameter = Q(created_at__lte=end_date)
            search_parameters.append(start_date_parameter)

        if author:
            authors = User.objects.filter(Q(first_name__icontains=author) | Q(last_name__icontains=author))
            author_parameter = Q(user__in=authors)
            search_parameters.append(author_parameter)

        return search_parameters

    def get_queryset(self):
        search_parameters = self.get_search_parameters()
        found_entries = Article.objects.filter(*search_parameters)

        return found_entries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['found_entries'] = self.get_queryset()

        return context
