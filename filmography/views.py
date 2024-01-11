from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from filmography.serializer import FilmoSerializer
from .models import Filmography

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class FilmoViewSet(viewsets.ModelViewSet):
    serializer_class = FilmoSerializer
    queryset = Filmography.objects.all()
    
    def get_queryset(self):

        queryset = cache.get('videoList')
        if not queryset:
            queryset = Filmography.objects.all()
            cache.set('videoList', queryset, CACHE_TTL)

        return queryset