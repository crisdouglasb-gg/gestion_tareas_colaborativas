from notificaciones.models import NotificacionSistema


def notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        count = NotificacionSistema.objects.filter(
            usuario_destino=request.user,
            leida=False
        ).count()
        return {'notif_no_leidas': count}
    return {'notif_no_leidas': 0}
