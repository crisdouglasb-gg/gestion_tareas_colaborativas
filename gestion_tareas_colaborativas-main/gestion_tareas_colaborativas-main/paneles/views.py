# paneles/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import PanelTrabajo
from espacios.models import EspacioTrabajo

@login_required
def lista_paneles(request, espacio_pk):
    # Primero verificás que el espacio le pertenece al usuario
    espacio = get_object_or_404(EspacioTrabajo, pk=espacio_pk, miembros=request.user)

    # Después traés los paneles de ESE espacio
    paneles = PanelTrabajo.objects.filter(espacio=espacio)
    return render(request, 'paneles/lista.html', {'paneles': paneles, 'espacio': espacio})

@login_required
def detalle_panel(request, pk):
    panel = get_object_or_404(
        PanelTrabajo,
        pk=pk,
        espacio__miembros=request.user   # un salto: espacio → miembros
    )
    return render(request, 'paneles/detalle.html', {'panel': panel})