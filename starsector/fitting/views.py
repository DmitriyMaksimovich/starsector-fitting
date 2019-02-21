from rest_framework import generics, pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from fitting.models import Ships, Weapons
from fitting.serializers import ShipSerializer, WeaponSerializer


class ShipsPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = None


class WeaponsPaginator(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = None


class ShipsList(generics.ListAPIView):
    serializer_class = ShipSerializer
    pagination_class = ShipsPaginator

    def get_queryset(self):
        queryset = Ships.objects.all()
        style = self.request.query_params.get('style', None)
        hull_size = self.request.query_params.get('hull_size', None)
        if style is not None:
            queryset = queryset.filter(style=style)
        if hull_size is not None:
            queryset = queryset.filter(hull_size=hull_size)
        return queryset


class ShipView(generics.RetrieveAPIView):
    queryset = Ships.objects.all()
    serializer_class = ShipSerializer


@api_view()
def ship_field_detail(request, ship_name, field):
    try:
        ship = Ships.objects.get(ship_name=ship_name)
        field_value = getattr(ship, field)
    except (Ships.DoesNotExist, AttributeError):
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response({field: field_value})


class WeaponsList(generics.ListAPIView):
    serializer_class = WeaponSerializer
    pagination_class = WeaponsPaginator

    def get_queryset(self):
        queryset = Weapons.objects.all()
        size = self.request.query_params.get('size', None)
        weapon_type = self.request.query_params.get('weapon_type', None)
        if size is not None:
            queryset = queryset.filter(size=size)
        if weapon_type is not None:
            queryset = queryset.filter(weapon_type=weapon_type)
        return queryset


class WeaponView(generics.RetrieveAPIView):
    queryset = Weapons.objects.all()
    serializer_class = WeaponSerializer
