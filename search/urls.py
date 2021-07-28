from django.urls import path

import search.views as search

app_name = 'search'

urlpatterns = [
    path('search_result/', search.SearchResultsView.as_view(), name='search_result'),
]
