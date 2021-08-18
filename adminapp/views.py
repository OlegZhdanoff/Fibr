from django.shortcuts import render


def index(request):
    return render(request, 'adminapp/index.html')


def article_active(request):
    return render(request, 'adminapp/article_active.html')


def article_archive(request):
    return render(request, 'adminapp/article_archive.html')


def users_active(request):
    return render(request, 'adminapp/users_active.html')


def users_archive(request):
    return render(request, 'adminapp/users_archive.html')


def hub_all_streams(request):
    return render(request, 'adminapp/hub_all_streams.html')


def hub_design(request):
    return render(request, 'adminapp/hub_design.html')


def hub_web_development(request):
    return render(request, 'adminapp/hub_web_development.html')


def hub_mobile_development(request):
    return render(request, 'adminapp/hub_mobile_development.html')
