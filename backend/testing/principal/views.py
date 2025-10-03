from rest_framework import viewsets
from .models import Principal
from .serializers import PrincipalSerializer

class PrincipalViewSet(viewsets.ModelViewSet):
    queryset = Principal.objects.all()
    serializer_class = PrincipalSerializer
