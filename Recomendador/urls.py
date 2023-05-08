from django.urls import path

from Recomendador import views
urlpatterns = [
    path('recomendadorDestinos/', views.recomendadorDestinos, name = "recomendadorDestinos"),
    path('formulario/', views.rd_formulario, name = "formulario"),
    path('destinos/', views.destinos, name = "destinos"),
    
]