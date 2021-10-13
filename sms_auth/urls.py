from django.urls import path

from .views import SMSAuthenticationSendingView

app_name = 'sms_auth'
urlpatterns = [
    path('send/', SMSAuthenticationSendingView.as_view()),
]
