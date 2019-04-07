from rest_framework import generics, pagination, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from fitting.models import Ships, Weapons, Fitting
from fitting.serializers import ShipSerializer, WeaponSerializer, FittingSerializer


class ShipsPaginator(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = None


class WeaponsPaginator(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = None


class ShipsList(generics.ListAPIView):
    serializer_class = ShipSerializer
    pagination_class = ShipsPaginator

    def get_queryset(self):
        queryset = Ships.objects.all()
        style = self.request.query_params.get('style', None)
        if style is not None:
            queryset = queryset.filter(style=style)
        hull_size = self.request.query_params.get('hull_size', None)
        if hull_size is not None:
            queryset = queryset.filter(hull_size=hull_size)
        mod = self.request.query_params.get('mod', None)
        if mod is not None:
            queryset = queryset.filter(mod_name=mod)
        return queryset

    def dispatch(self, *args, **kwargs):
        return super(ShipsList, self).dispatch(*args, **kwargs)


class ShipView(generics.RetrieveAPIView):
    queryset = Ships.objects.all()
    serializer_class = ShipSerializer

    def dispatch(self, *args, **kwargs):
        return super(ShipView, self).dispatch(*args, **kwargs)


class WeaponsList(generics.ListAPIView):
    serializer_class = WeaponSerializer
    pagination_class = WeaponsPaginator

    def get_queryset(self):
        queryset = Weapons.objects.all()
        size = self.request.query_params.get('size', None)
        if size is not None:
            queryset = queryset.filter(size=size)
        weapon_type = self.request.query_params.get('weapon_type', None)
        if weapon_type is not None:
            queryset = queryset.filter(weapon_type=weapon_type)
        mod = self.request.query_params.get('mod', None)
        if mod is not None:
            queryset = queryset.filter(mod_name=mod)
        return queryset

    def dispatch(self, *args, **kwargs):
        return super(WeaponsList, self).dispatch(*args, **kwargs)


class WeaponView(generics.RetrieveAPIView):
    queryset = Weapons.objects.all()
    serializer_class = WeaponSerializer

    def dispatch(self, *args, **kwargs):
        return super(WeaponView, self).dispatch(*args, **kwargs)


class FitingsView(generics.ListAPIView):
    serializer_class = FittingSerializer
    pagination_class = ShipsPaginator

    def get_queryset(self):
        queryset = Fitting.objects.all()
        return queryset


class SearchShipView(generics.ListAPIView):
    serializer_class = ShipSerializer
    pagination_class = ShipsPaginator

    def get_queryset(self):
        ship_name = self.kwargs['ship_name']
        queryset = Ships.objects.filter(ship_name__icontains=ship_name)
        return queryset


class AvailableWeapons(generics.ListAPIView):
    serializer_class = WeaponSerializer

    def get_available_weapons_properties(self, ship: Ships):
        weapon_types = set()
        weapon_sizes = set()
        ship_slots = ship.weapon_slots
        for slot in ship_slots:
            weapon_types.add(ship_slots[slot]['type'])
            weapon_sizes.add(ship_slots[slot]['size'])
        return {'types': weapon_types, 'sizes': weapon_sizes}

    def get_available_weapons(self, ship):
        weapons_properties = self.get_available_weapons_properties(ship)
        sizes = weapons_properties['sizes']
        types = weapons_properties['types']
        weapons = Weapons.objects.filter(size__in=sizes).filter(weapon_type__in=types)
        return weapons

    def get_queryset(self):
        hull_id = self.kwargs['ship_name']
        ship = Ships.objects.get(pk=hull_id)
        weapons = self.get_available_weapons(ship)
        return weapons


@api_view()
def ship_filters_view(request, filter):
    if filter not in ('hull_size', 'style'):
        return Response(status=HTTP_404_NOT_FOUND)
    queryset = Ships.objects.distinct(filter)
    values = [getattr(row, filter) for row in queryset]
    return Response({'count': len(values),
                     'values': values})


@api_view()
def weapon_filters_view(request, filter):
    if filter not in ('weapon_type', 'size', 'mod_name'):
        return Response(status=HTTP_404_NOT_FOUND)
    queryset = Weapons.objects.distinct(filter)
    values = [getattr(row, filter) for row in queryset]
    return Response({'count': len(values),
                     'values': values})
