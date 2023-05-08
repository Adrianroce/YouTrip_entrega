from django.urls import path

from Viaje import views
urlpatterns = [
    path('anadirAmigoViaje/', views.anadirAmigoViaje, name = "anadirAmigoViaje"),
]