from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('article_active/', adminapp.article_active, name='article_active'),
    path('article_archive/', adminapp.article_archive, name='article_archive'),
    path('users_active/', adminapp.users_active, name='users_active'),
    path('users_archive/', adminapp.users_archive, name='users_archive'),
    path('hub_all_streams/', adminapp.hub_all_streams, name='hub_all_streams'),
    path('hub_design/', adminapp.hub_design, name='hub_design'),
    path('hub_web_development/', adminapp.hub_web_development, name='hub_web_development'),
    path('hub_mobile_development/', adminapp.hub_mobile_development, name='hub_mobile_development'),

]
