"""Fibr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mainapp.urls', namespace='mainapp')),
    path('hub/', include('hub.urls', namespace='hub')),
    path('article/', include('article.urls', namespace='article')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('admin-staff/', include('adminapp.urls', namespace='admin-staff')),
    path('summernote/', include('django_summernote.urls')),
    path('search/', include('search.urls', namespace='search')),

    # Оставил параметры админки по дефолту
    path('admin/', admin.site.urls),
    path('notification/', include('notification.urls', namespace='notification')),
    path('complaint/', include('complaint.urls', namespace='complaint')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
