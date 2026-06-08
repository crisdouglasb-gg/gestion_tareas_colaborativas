# notificaciones/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import NotificacionSistema

@login_required
def mis_notificaciones(request):
    notificaciones = NotificacionSistema.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')
    return render(request, 'notificaciones/lista.html', {'notificaciones': notificaciones})

@login_required
def marcar_leida(request, pk):
    notif = get_object_or_404(NotificacionSistema, pk=pk, usuario=request.user)
    notif.leida = True
    notif.save()
    return redirect('mis_notificaciones')