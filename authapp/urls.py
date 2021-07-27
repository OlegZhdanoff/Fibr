from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.UserLogin.as_view(), name='login'),
    path('logout/', authapp.UserLogout.as_view(), name='logout'),
    path('register/', authapp.RegisterUserView.as_view(), name='register'),
    path('profile/<int:pk>/', authapp.ProfileView.as_view(), name='profile'),
    path('moderation/', authapp.moderation, name='moderation'),
    path('user_info/<int:pk>/', authapp.user_info, name='user_info'),
    path('access-error/', authapp.access_error, name='access_error'),
    path('block-user/<int:pk>/', authapp.block_user, name='block_user'),
    # path('edit/', authapp.edit, name='edit'),
]
