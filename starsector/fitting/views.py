from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, pagination, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_404_NOT_FOUND
from fitting.models import Ships, Weapons, Fitting
from fitting.serializers import ShipSerializer, WeaponSerializer, FittingSerializer


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
        if style is not None:
            queryset = queryset.filter(style=style)
        hull_size = self.request.query_params.get('hull_size', None)
        if hull_size is not None:
            queryset = queryset.filter(hull_size=hull_size)
        mod = self.request.query_params.get('mod', None)
        if mod is not None:
            queryset = queryset.filter(mod_name=mod)
        return queryset

    @method_decorator(cache_page(60*60*24))
    def dispatch(self, *args, **kwargs):
        return super(ShipsList, self).dispatch(*args, **kwargs)


class ShipView(generics.RetrieveAPIView):
    queryset = Ships.objects.all()
    serializer_class = ShipSerializer

    @method_decorator(cache_page(60*60*24))
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

    @method_decorator(cache_page(60*60*24))
    def dispatch(self, *args, **kwargs):
        return super(WeaponsList, self).dispatch(*args, **kwargs)


class WeaponView(generics.RetrieveAPIView):
    queryset = Weapons.objects.all()
    serializer_class = WeaponSerializer

    @method_decorator(cache_page(60*60*24))
    def dispatch(self, *args, **kwargs):
        return super(WeaponView, self).dispatch(*args, **kwargs)


@cache_page(60*60*24)
@api_view()
def ship_filters_view(request, filter):
    if filter not in ('hull_size', 'style'):
        return Response(status=HTTP_404_NOT_FOUND)
    queryset = Ships.objects.distinct(filter)
    values = [getattr(row, filter) for row in queryset]
    return Response({'count': len(values),
                     'values': values})


@cache_page(60*60*24)
@api_view()
def weapon_filters_view(request, filter):
    if filter not in ('weapon_type', 'size', 'mod_name'):
        return Response(status=HTTP_404_NOT_FOUND)
    queryset = Weapons.objects.distinct(filter)
    values = [getattr(row, filter) for row in queryset]
    return Response({'count': len(values),
                     'values': values})
