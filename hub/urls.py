from django.urls import path

import hub.views as hub

app_name = 'hub'

urlpatterns = [
    path('<int:pk>/', hub.TopicView.as_view(), name='topic')

]
