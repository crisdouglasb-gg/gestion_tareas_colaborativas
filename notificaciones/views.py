from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from notificaciones.models import NotificacionSistema


@login_required(login_url='/login/')
def notificaciones_view(request):
    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')
    no_leidas = notificaciones_usuario.filter(leida=False).count()
    contexto = {
        'notificaciones_usuario': notificaciones_usuario,
        'no_leidas': no_leidas,
    }
    return render(request, 'notificaciones/notificaciones.html', contexto)


@login_required(login_url='/login/')
def marcar_notificaciones_leidas(request):
    if request.method == 'POST':
        NotificacionSistema.objects.filter(
            usuario_destino=request.user,
            leida=False
        ).update(leida=True)
        messages.success(request, 'Todas las notificaciones fueron marcadas como leídas.')
    return redirect('notificaciones')
