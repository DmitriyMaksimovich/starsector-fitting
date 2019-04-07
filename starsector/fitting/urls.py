from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from fitting import views


urlpatterns = [
    path('api/ships/', views.ShipsList.as_view(), name='ships_list'),
    path('api/ships/<pk>/', views.ShipView.as_view(), name='ship_detail'),
    path('api/weapons/', views.WeaponsList.as_view(), name='weapons_list'),
    path('api/weapons/<pk>/', views.WeaponView.as_view(), name='weapon_detail'),
    path('api/filters/ships/<str:filter>', views.ship_filters_view, name='ship_filters_view'),
    path('api/filters/weapons/<str:filter>', views.weapon_filters_view, name='weapon_filters_view'),
    path('api/search/ship/<str:ship_name>/', views.SearchShipView.as_view(), name='find_ship'),
    path('api/available_weapons/<str:ship_name>/', views.AvailableWeapons.as_view(), name='available_weapons'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
