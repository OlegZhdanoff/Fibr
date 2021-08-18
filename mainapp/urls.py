from django.urls import path

import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    # path('<str:sorting>/', mainapp.Index.as_view(), name='index'),
    path('', mainapp.Index.as_view(), name='index'),
    # path('', mainapp.index, name='index'),
]
