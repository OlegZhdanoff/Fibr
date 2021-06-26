from django.shortcuts import render


def index(request):
    context = {'title': 'How to Fight Fraud with Artificial Intelligence and Intelligent Analytics'}
    return render(request, 'article/article.html', context)
