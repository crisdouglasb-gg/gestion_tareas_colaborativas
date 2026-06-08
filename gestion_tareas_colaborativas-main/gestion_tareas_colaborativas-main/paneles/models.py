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
    
class ColumnaEstado(models.Model):
    # Relación con el panel donde existirá la columna
    panel_relacionado = models.ForeignKey(
        PanelTrabajo,
        on_delete=models.CASCADE,
        related_name='columnas_kanban'
    )

    # Nombre visible de la columna
    nombre_columna = models.CharField(
        max_length=80,
        verbose_name='Nombre de columna'
    )

    # Permite ordenar visualmente las columnas
    posicion_columna = models.PositiveIntegerField(
        default=0
    )

    # Control de color para futuras mejoras visuales
    color_identificacion = models.CharField(
        max_length=30,
        default='gris'
    )

    # Permite ocultar columnas sin borrarlas
    columna_archivada = models.BooleanField(
        default=False
    )

    # Fecha de creación automática
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Columna de estado'
        verbose_name_plural = 'Columnas de estado'

        # Orden automático para drag & drop futuro
        ordering = ['posicion_columna', 'id']

    def __str__(self):
        return f'{self.panel_relacionado} - {self.nombre_columna}'    