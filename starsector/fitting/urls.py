from django.urls import path
from fitting import views


urlpatterns = [
    path('ship/', views.ShipsListCreate.as_view()),
    path('ship/<str:ship_name>/', views.ship_detail),
    path('ship/<str:ship_name>/<str:field>/', views.ship_field_detail),
]
