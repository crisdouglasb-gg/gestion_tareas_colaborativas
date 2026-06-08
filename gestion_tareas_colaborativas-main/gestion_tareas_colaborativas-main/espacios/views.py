# espacios/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import EspacioTrabajo

@login_required
def lista_espacios(request):
    espacios = EspacioTrabajo.objects.filter(
        miembros=request.user
    ).distinct()
    return render(request, 'espacios/lista.html', {'espacios': espacios})

@login_required
def detalle_espacio(request, pk):
    espacio = get_object_or_404(EspacioTrabajo, pk=pk, miembros=request.user)
    return render(request, 'espacios/detalle.html', {'espacio': espacio})

@login_required
def crear_espacio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        espacio = EspacioTrabajo.objects.create(nombre=nombre)
        espacio.miembros.add(request.user)  # el creador es miembro automáticamente
        return redirect('lista_espacios')
    return render(request, 'espacios/crear.html') 