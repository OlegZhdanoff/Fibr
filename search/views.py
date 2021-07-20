from django.views.generic import ListView
from article.models import Article


class SearchResultsView(ListView):
    model = Article
    template_name = 'search/search_result.html'
    # form_class = ArticleSearchForm
    success_url = '/'
    success_msg = 'Поиск статьи'


    def get_queryset(self): 
        text_for_search = self.request.GET.get('q').lower()
        object_list = Article.get_articles().filter(content__icontains = text_for_search)

        # object_list = Articleobjects.filter(
        #     Q(name__icontains=title) | Q(state__icontains=title)
        # )

        # name = self.kwargs.get('name', '')
        # object_list = Article.objects.all()
        # if name:
        #     object_list = object_list.filter(name__icontains=name)
        return object_list
