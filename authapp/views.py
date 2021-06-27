from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from authapp.models import User
from authapp.forms import UserRegisterForm


class UserLogin(LoginView):
    template_name = 'authapp/login.html'


class UserLogout(LogoutView):
    next_page = '/'


class RegisterUserView(CreateView):
    model = User
    template_name = 'authapp/register.html'
    form_class = UserRegisterForm
    success_url = '/'
    success_msg = 'Пользователь успешно создан'
