from django.urls import path
from fitting import views


urlpatterns = [
    path('api/ships/', views.ShipsListCreate.as_view()),
]
