from django.urls import path

import search.views as search

app_name = 'search'

urlpatterns = [
    path('search_result/', search.search, name='search_result'),
]
