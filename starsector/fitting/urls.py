from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from fitting import views


urlpatterns = [
    path('ship/', views.ShipsList.as_view(), name='ships_list'),
    path('ship/<pk>/', views.ShipView.as_view(), name='ship_detail'),
    path('ship/<str:ship_name>/<str:field>/', views.ship_field_detail, name='ship_field_detail'),
    path('weapon/', views.WeaponsList.as_view(), name='weapons_list'),
    path('weapon/<pk>/', views.WeaponView.as_view(), name='weapon_detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
