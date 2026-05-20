from django.conf import settings
from django.db import models


class NotificacionSistema(models.Model):
    # Usuario que recibirá la notificación
    usuario_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificaciones_recibidas'
    )

    # Mensaje principal visible para el usuario
    mensaje_notificacion = models.CharField(
        max_length=255
    )

    # Permite controlar si el usuario ya leyó la notificación
    leida = models.BooleanField(
        default=False
    )

    # Información adicional opcional
    detalle_adicional = models.TextField(
        blank=True,
        null=True
    )

    # Fecha automática de creación
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Notificación del sistema'
        verbose_name_plural = 'Notificaciones del sistema'

        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.mensaje_notificacion