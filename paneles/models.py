from django.db import models

from espacios.models import EspacioTrabajo


class PanelTrabajo(models.Model):
    espacio_padre = models.ForeignKey(
        EspacioTrabajo,
        on_delete=models.CASCADE,
        related_name='paneles_disponibles'
    )

    nombre_panel = models.CharField(
        max_length=120,
        verbose_name='Nombre del panel'
    )

    descripcion_panel = models.TextField(
        blank=True,
        null=True
    )

    posicion_visual = models.PositiveIntegerField(
        default=0
    )

    panel_archivado = models.BooleanField(
        default=False
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Panel de trabajo'
        verbose_name_plural = 'Paneles de trabajo'
        ordering = ['posicion_visual', 'id']

    def __str__(self):
        return self.nombre_panel