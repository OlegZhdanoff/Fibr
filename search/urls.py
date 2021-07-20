from django.urls import path

import search.views as search

app_name = 'search'

urlpatterns = [
    path('search_article/', search.search_article, name='search_article')

]
