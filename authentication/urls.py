from django.urls import path

from authentication.utils import activate_user, change_password, send_pw_reset_mail
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/confirm/<str:token>/', activate_user, name='activate_user'), #send_pw_reset_mail
    path('mailresetPW/', send_pw_reset_mail, name='reset_password'),
    path('changePW/confirm/<str:token>/', change_password, name='change_password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]