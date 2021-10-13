from django.urls import path

from .views import SMSAuthenticationSendingView, SMSAuthenticationVerificationView

app_name = 'sms_auth'
urlpatterns = [
    path('send/', SMSAuthenticationSendingView.as_view()),
    path('verify/', SMSAuthenticationVerificationView.as_view()),
]
