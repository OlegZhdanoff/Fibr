from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from authapp.models import User
from authapp.forms import UserRegisterForm, UserAuthenticationForm, UserProfileForm
from django.urls import reverse
from django.shortcuts import render

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
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authapp:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'authapp/profile.html', context)
