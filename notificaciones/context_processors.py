from notificaciones.models import NotificacionSistema
from usuarios.models import PerfilUsuario


def notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        count = NotificacionSistema.objects.filter(
            usuario_destino=request.user,
            leida=False
        ).count()
        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=request.user,
            defaults={'rol': 'ADMIN' if request.user.is_superuser else 'MIEMBRO'}
        )
        return {'notif_no_leidas': count, 'mi_perfil': perfil}
    return {'notif_no_leidas': 0, 'mi_perfil': None}
