from django.db.models.signals import post_save
from django.dispatch import receiver

from actividades.models import AsignacionActividad
from notificaciones.models import NotificacionSistema


@receiver(post_save, sender=AsignacionActividad)
def generar_notificacion_asignacion(sender, instance, created, **kwargs):
    """
    Genera automáticamente una notificación cuando
    una actividad es asignada a un usuario.
    """

    # Evita crear notificaciones en actualizaciones
    if created:
        NotificacionSistema.objects.create(
            usuario_destino=instance.usuario_asignado,
            mensaje_notificacion=(
                f'Se te asignó la actividad: '
                f'{instance.actividad_relacionada.titulo_actividad}'
            ),
            detalle_adicional=(
                'La asignación fue registrada correctamente '
                'dentro del sistema colaborativo.'
            )
        )