from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLogin.as_view(), name='login'),
    path('logout/', authapp.UserLogout.as_view(), name='logout'),
    path('profile/', authapp.profile, name='profile'),
]
