from django.urls import path
from .views import FilmoViewSet

urlpatterns = [
    path('', FilmoViewSet.as_view({'get': 'list', 'post': 'create'}), name='Filmography'),
]