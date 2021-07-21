import re

from django.db.models import Q
from django.shortcuts import render

from article.models import Article


def normal_query(query_string,
                 findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                 normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None
    terms = normal_query(query_string)
    for term in terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ["title", ])
        found_entries = Article.objects.filter(entry_query).order_by("-title")
    return render(request, 'search/search_result.html',
                  {'query_string': query_string, 'found_entries': found_entries})
