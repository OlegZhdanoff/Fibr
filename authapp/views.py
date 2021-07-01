from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from article.models import Article
from authapp.forms import UserRegisterForm, UserAuthenticationForm, UserProfileForm, UserProfileEditForm
from authapp.models import User


class UserLogin(LoginView):
    form_class = UserAuthenticationForm
    template_name = 'authapp/login.html'


class UserLogout(LogoutView):
    next_page = '/'


class RegisterUserView(CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    success_msg = 'Пользователь успешно создан'


def profile(request):
    if request.method == 'POST':
        form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'articles': Article.get_user_articles(request.user.pk)
    }
    print(request.user.pk)
    return render(request, 'authapp/profile.html', context)
