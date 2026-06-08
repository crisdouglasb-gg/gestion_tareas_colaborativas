# actividades/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ActividadProyecto

@login_required
def lista_actividades(request):
    actividades = ActividadProyecto.objects.filter(
        columna__panel__espacio__miembros=request.user  # tres saltos
    ).distinct()
    return render(request, 'actividades/lista.html', {'actividades': actividades})

@login_required
def detalle_actividad(request, pk):
    actividad = get_object_or_404(
        ActividadProyecto,
        pk=pk,
        columna__panel__espacio__miembros=request.user
    )
    return render(request, 'actividades/detalle.html', {'actividad': actividad})

@login_required
def editar_actividad(request, pk):
    actividad = get_object_or_404(
        ActividadProyecto,
        pk=pk,
        columna__panel__espacio__miembros=request.user
    )
    if request.method == 'POST':
        actividad.titulo = request.POST.get('titulo', actividad.titulo)
        actividad.save()
        return redirect('detalle_actividad', pk=pk)
    return render(request, 'actividades/editar.html', {'actividad': actividad})

@login_required
def eliminar_actividad(request, pk):
    actividad = get_object_or_404(
        ActividadProyecto,
        pk=pk,
        columna__panel__espacio__miembros=request.user
    )
    if request.method == 'POST':
        actividad.delete()
        return redirect('lista_actividades')
    return render(request, 'actividades/confirmar_eliminar.html', {'actividad': actividad})