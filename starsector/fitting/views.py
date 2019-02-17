from fitting.models import Ships
from fitting.serializers import ShipSerializer
from rest_framework import generics

class ShipsListCreate(generics.ListCreateAPIView):
    queryset = Ships.objects.all()
    serializer_class = ShipSerializer

