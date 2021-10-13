from django.urls import path

from .views import UserView, LoginView

app_name = 'user'
urlpatterns = [
    path('', UserView.as_view()),
    path('login/', LoginView.as_view()),
]
