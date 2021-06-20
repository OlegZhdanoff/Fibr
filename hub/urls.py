from django.urls import path

import hub.views as hub

app_name = 'hub'

urlpatterns = [
    path('web-dev/', hub.WebDevView.as_view(), name='web-dev'),
    path('administration/', hub.AdministrationView.as_view(), name='administration'),
    path('design/', hub.DesignView.as_view(), name='design'),
    path('management/', hub.ManagementView.as_view(), name='management'),
    path('marketing/', hub.MarketingView.as_view(), name='marketing'),

]
