from django.urls import path

from authentication.utils import activate_user, change_password
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/confirm/<str:token>/', activate_user, name='activate_user'),
    path('changePW/', change_password, name='change_password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]