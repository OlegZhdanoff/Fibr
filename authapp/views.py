from django.contrib.auth.views import LoginView, LogoutView


class UserLogin(LoginView):
    template_name = 'authapp/login.html'


class UserLogout(LogoutView):
    next_page = '/'


def user_register():
    pass
