from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

import article.models
from authapp.forms import UserProfileForm


class UserLogin(LoginView):
    template_name = 'authapp/login.html'


class UserLogout(LogoutView):
    next_page = '/'


def user_register():
    pass


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
        'article': article.models.Article,
    }
    return render(request, 'authapp/profile.html', context)
