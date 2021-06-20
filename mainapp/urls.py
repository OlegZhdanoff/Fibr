from django.urls import path

import mainapp.views as mainapp

app_name = 'main'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('hub/web-dev/', mainapp.hub_web_dev, name='web-dev'),
    path('hub/administration/', mainapp.hub_administration, name='administration'),
    path('hub/design/', mainapp.hub_design, name='design'),
    path('hub/management/', mainapp.hub_management, name='management'),
    path('hub/marketing/', mainapp.hub_marketing, name='marketing'),
    path('article/1/', mainapp.article, name='article'),

]
