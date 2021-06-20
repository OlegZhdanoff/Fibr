from django.shortcuts import render


def index(request):
    context = {'title': 'Fibr',
               'article': 'Все потоки'}
    return render(request, 'index.html', context)


def hub_design(request):
    context = {'title': 'Fibr',
               'article': 'Дизайн'}
    return render(request, 'index.html', context)


def hub_web_dev(request):
    context = {'title': 'Fibr',
               'article': 'Веб-разработка'}
    return render(request, 'index.html', context)


def hub_administration(request):
    context = {'title': 'Fibr',
               'article': 'Администрирование'}
    return render(request, 'index.html', context)


def hub_management(request):
    context = {'title': 'Fibr',
               'article': 'Менеджмент'}
    return render(request, 'index.html', context)


def hub_marketing(request):
    context = {'title': 'Fibr',
               'article': 'Маркетинг'}
    return render(request, 'index.html', context)


def article(request):
    context = {'title': 'Fibr'}
    return render(request, 'article.html', context)
