from django.shortcuts import render


def index(request):
    context = {'title': 'Fibr',
               'article': 'Все потоки'}
    return render(request, 'mainapp/index.html', context)
