from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Gestion.models import Ciudad, Ciudad_Image, CiudadDto
from Sesion.forms import ImageForm
from Sesion.models import Image
from django.contrib import messages
from django.contrib.auth.models import User
from Amigos.models import Relacion
from Viaje.forms import AnadirAmigosForm
from Viaje.models import Viajero, Viaje


@login_required
def anadirAmigoViaje(request):
    context = {}
    if request.method == "POST":
        lista_amigos = request.POST.getlist('checks')
        viaje_id = request.POST.get('viaje')
        if len(lista_amigos) > 0 and viaje_id is not None and viaje_id != "":

            # obtengo viaje
            viaje = Viaje.objects.filter(pk=viaje_id).first()

            # viajeros del viaje ya unidos o invitados
            viajeros = viaje.integrantes.all()
            usuarios_unidos = [v.usuario.id for v in viajeros]

            # obtengo ususarios
            usuarios = User.objects.filter(pk__in=lista_amigos).exclude(pk__in=usuarios_unidos).all()

            # añado los usuarios al viaje
            for usuario in usuarios:
                v = Viajero(viaje=viaje, usuario=usuario, creador=False, administrador=False, viaje_aceptado=False)
                v.save()

            messages.success(request, "Amigos añadidos correctamente")
        else:
            messages.error(request, "Error añadiendo amigos")
    else:
        pass
    
    return redirect('viajestab')
