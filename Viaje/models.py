from django.db import models
from django.conf import settings
from Gestion.models import Ciudad, UsuarioDto
from datetime import date

class Viaje(models.Model):
    viaje_id = models.AutoField(primary_key=True)
    destino = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name="imagenes")
    presupuesto = models.FloatField()
    descripcion = models.CharField(blank=True, max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valoracion = models.FloatField(null=True)


class Viajero(models.Model):
    viajero_id = models.AutoField(primary_key=True)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name="integrantes")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="viajes")
    creador = models.BooleanField()
    administrador = models.BooleanField()
    viaje_aceptado = models.BooleanField()


# dto
class ViajeDto():
    def __init__(self, viaje, viajeros = []):
        if viaje is not None:
            self.viaje_id = viaje.viaje_id 
            self.destino = viaje.destino 
            self.presupuesto = viaje.presupuesto
            self.descripcion = viaje.descripcion 
            self.fecha_inicio = viaje.fecha_inicio 
            self.fecha_fin = viaje.fecha_fin 
            self.valoracion = viaje.valoracion 
            self.viajeros = [ViajeroDto(v) for v in viajeros]
            
            tr = viaje.fecha_inicio - date.today()
            self.tiempo_restante = tr.days


class ViajeroDto():
    def __init__(self, viajero):
        if viajero is not None:
            self.viajero_id = viajero.viajero_id 
            self.viaje = viajero.viaje 
            self.usuario = UsuarioDto(viajero.usuario) 
            self.creador = viajero.creador 
            self.administrador = viajero.administrador 
            self.viaje_aceptado = viajero.viaje_aceptado 