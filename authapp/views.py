from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView

from authapp.forms import UserRegisterForm, UserAuthenticationForm, UserEditForm, UserProfileEditForm
from authapp.models import User
from django.db import transaction


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
        form = UserEditForm(instance=request.user)

    context = {
        'form': form,
        # 'articles': ArticleViews.objects.filter(user=request.user)
    }
    return render(request, 'authapp/profile.html', context)


@transaction.atomic
def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))
    else:
        edit_form = UserEditForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)
    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'authapp/edit.html', content)
