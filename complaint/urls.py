from django.urls import path

import complaint.views as complaint

app_name = 'complaint'

urlpatterns = [
    path('create/<int:pk>/', complaint.create, name='create'),
    path('edit/<int:pk>/', complaint.edit, name='edit'),
]
