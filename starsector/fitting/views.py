from django.http import HttpResponse, JsonResponse
from rest_framework import generics, pagination
from fitting.models import Ships
from fitting.serializers import ShipSerializer

class StandartPaginator(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = None


class ShipsListCreate(generics.ListCreateAPIView):
    queryset = Ships.objects.all()
    serializer_class = ShipSerializer
    pagination_class = StandartPaginator


def ship_detail(request, ship_name):
    try:
        ship = Ships.objects.get(ship_name=ship_name)
    except Ships.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ShipSerializer(ship)
        return JsonResponse(serializer.data)
    else:
        return HttpResponse(status=405)


def ship_field_detail(request, ship_name, field):
    try:
        ship = Ships.objects.get(ship_name=ship_name)
        field_value = getattr(ship, field)
    except Ships.DoesNotExist:
        return HttpResponse(status=404)
    except AttributeError:
        return HttpResponse(status=404)

    if request.method == "GET":
        return JsonResponse({field: field_value})
    else:
        return HttpResponse(status=405)

