from django import forms
from django.contrib.auth.models import User
from Viaje.models import Viaje

class ViajeForm(forms.Form):
    descripcion = forms.CharField(required=True)
    presupuesto = forms.CharField(required=True)
    fecha_inicio = forms.CharField(required=True)
    fecha_fin = forms.CharField(required=True)
    destino = forms.CharField(required=True)


class AnadirAmigosForm(forms.Form):
    lista_amigos = forms.MultipleChoiceField(choices=[(c.id, c.username) for c in User.objects.all()], required=True)
    viaje = forms.IntegerField(required=True)


class ViajeGestionarForm(forms.Form):
    lista_viajes = forms.MultipleChoiceField(choices=[(c.viaje_id, c.destino.nombre) for c in Viaje.objects.all()], required=True)