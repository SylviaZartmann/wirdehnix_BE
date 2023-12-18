from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from filmography.serializer import FilmoSerializer
from .models import Filmography

@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
class FilmoViewSet(viewsets.ModelViewSet):
    serializer_class = FilmoSerializer
    queryset = Filmography.objects.all()