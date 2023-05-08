from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Recomendador.forms import CuestionarioForm
from Gestion.views import obtener_img_ciudad, getContext
from django.contrib import messages
from Gestion.models import Ciudad, CiudadDto, Ciudad_Mes
import math
from django.utils.dateparse import parse_date

# constantes
CIUDADES_MOSTRAR = 9
MAX_DIF = 4  # las preguntas tienen 5 respuestas, la diferencia maxima es 4 (5-1)

# funciones
def obtener_similitud(v1, v2):
    """recibe 2 vectores y devuelve la similitus entre ellos (entre 0 y 1)"""
    """
    Calcula el porcentaje de afinidad entre dos vectores.
    """
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma longitud.")
    
    # Calcula la suma del producto de los elementos de los vectores.
    producto_punto = sum(i*j for i,j in zip(v1, v2))
    
    # Calcula la magnitud de cada vector.
    magnitud_v1 = sum(i**2 for i in v1) ** 0.5
    magnitud_v2 = sum(i**2 for i in v2) ** 0.5
    
    # Calcula el coseno del ángulo entre los vectores.
    coseno_angulo = producto_punto / (magnitud_v1 * magnitud_v2)
    
    # Convierte el coseno del ángulo en porcentaje.
    porcentaje = int(round(coseno_angulo * 100, 2))
    
    return porcentaje


def distancia_L2(v1, v2):
    """Recibe dos vectores y devuelve la distancia L2"""
    return math.sqrt(sum([(v1[i] - v2[i])**2 for i in range(len(v1))]))

def ordenar_por_similitud(d, v):
    """Recebi diccionario(clave, vector) y vector_x. 
    Devuelve las claves del diccionario ordenadas por similitud respecto a vector_x"""
    pares = [(ciudad_id, distancia_L2(d[ciudad_id], v),
              obtener_similitud(d[ciudad_id], v)) for ciudad_id in d.keys()]
    pares_ordenados = sorted(pares, key=lambda x: x[1])
    return [(par[0], par[2]) for par in pares_ordenados]

def obtener_ciudades(d):
    destinos_recomendados = Ciudad.objects.filter(pk__in=d.keys()).all()

    lst_ciudades = []
    for dr in destinos_recomendados:
        img = obtener_img_ciudad(dr.ciudad_id)
        lst_ciudades.append(CiudadDto(dr, afinidad=d[dr.ciudad_id], img=img))
        lst_ciudades_ordenados = sorted(lst_ciudades, key=lambda x: x.afinidad, reverse=True)

    return lst_ciudades_ordenados

def obtener_destinos_fechas(fd, fh, min_destinos=CIUDADES_MOSTRAR):
    """obtiene al menos 'min_ciudades' en las fechas indicadas
    si en las fechas no encuentra al menos las ciudades indicadas ampliara el rango"""

    fd_month = fd.month
    fh_month = fh.month
    n_ciudades = 0

    iter = 1
    max_iter = 20 # control de flujo
    while min_destinos > n_ciudades and iter < max_iter:
        c = Ciudad_Mes.objects\
                .filter(mes__gte=fd_month, mes__lte=fh_month)\
                .all()\
                .distinct('ciudad')

        # actualizamos datos
        fd_month -= 1
        fh_month += 1

        n_ciudades = len(c)
        iter += 1
    
    return [ciu.ciudad.ciudad_id for ciu in c]


# vistas
@login_required
def recomendadorDestinos(request):
    return render(request, 'recomendador.html')

@login_required
def rd_formulario(request):
    ctx = getContext(request)

    if request.method == "POST":
        form = CuestionarioForm(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data.get("p1")
            p2 = form.cleaned_data.get("p2")
            p3 = form.cleaned_data.get("p3")
            p4 = form.cleaned_data.get("p4")
            p5 = form.cleaned_data.get("p5")
            fecha_inicio = form.cleaned_data.get("fecha_inicio")
            fecha_fin = form.cleaned_data.get("fecha_fin")

            # nuestro vector de referencia
            v = [str(p1), str(p2), str(p3), str(p4), str(p5)]
            
            # mensaje de pruebas
            messages.success(request, f"Formulario recibido {p1} {p2} {p3} {p4} {p5} ")
        
            url = reverse('destinos') + '?eleccion=' + ','.join(v) + f",{fecha_inicio}" + f",{fecha_fin}"
            return redirect(url)
        else:
            messages.error(request, f"Error al obtener el formulario...")
    return render(request, 'formulario.html', ctx)

@login_required
def destinos(request):
    
    ctx = getContext(request)

    if request.method == "POST":
        pass
    else:
        eleccion = request.GET.getlist('eleccion')[0].split(',')

        if eleccion is not None and len(eleccion) == 7:
            # obtengo datos
            eleccion, fecha_inicio, fecha_fin = eleccion[:5], parse_date(eleccion[5]), parse_date(eleccion[6])

            v = [int(e) for e in eleccion]

            # obtenemos las ciudades a las que se puede viajar en esas fechas
            destinos_fechas = obtener_destinos_fechas(fecha_inicio, fecha_fin, min_destinos=CIUDADES_MOSTRAR)

            # codigo obtener ciudads y datos a mostrar
            # obtener los datos de las ciudades
            datos_destinos = Ciudad.objects\
                .filter()\
                .values('ciudad_id','familia',
                        'gastronomia','cultura','transporte','pareja').all()
            d = {}

            for dd in datos_destinos:
                if dd["ciudad_id"] in destinos_fechas:
                    d[dd["ciudad_id"]] = [int(dd["familia"]), int(dd["gastronomia"]),int(dd["cultura"]),int(dd["transporte"]), int(dd["pareja"])]
                
            # obtenemos los destinos mas similares
            destinos_similares_ordenados = ordenar_por_similitud(d, v)

            # obtenemos las X ciudades mas similares
            ciudades_mas_similares = dict(destinos_similares_ordenados[:CIUDADES_MOSTRAR])

            # obtenemos las ciudades a mostrar
            destinos_recomendados = obtener_ciudades(ciudades_mas_similares)

            messages.success(request, "Todo okey")

            ctx["destinos"] = destinos_recomendados

    return render(request, 'destinos.html', ctx)
