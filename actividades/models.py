from django.conf import settings
from django.db import models

from paneles.models import ColumnaEstado


class ActividadProyecto(models.Model):
    # Opciones de prioridad para organizar tareas
    PRIORIDADES_DISPONIBLES = (
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    )

    # Columna donde se encuentra actualmente la actividad
    columna_actual = models.ForeignKey(
        ColumnaEstado,
        on_delete=models.CASCADE,
        related_name='actividades_asociadas'
    )

    # Usuario creador de la actividad
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades_creadas'
    )

    # Título principal visible en la tarjeta
    titulo_actividad = models.CharField(
        max_length=180
    )

    # Descripción extendida de la tarea
    descripcion_detallada = models.TextField(
        blank=True,
        null=True
    )

    # Nivel de prioridad
    prioridad_actividad = models.CharField(
        max_length=10,
        choices=PRIORIDADES_DISPONIBLES,
        default='MEDIA'
    )

    # Posición visual para drag & drop
    posicion_actividad = models.PositiveIntegerField(
        default=0
    )

    # Fecha límite opcional
    fecha_limite = models.DateField(
        blank=True,
        null=True
    )

    # Permite archivar actividades sin eliminarlas
    actividad_archivada = models.BooleanField(
        default=False
    )

    # Fecha automática de creación
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    # Fecha automática de actualización
    fecha_actualizacion = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Actividad de proyecto'
        verbose_name_plural = 'Actividades de proyecto'

        # Orden importante para drag & drop futuro
        ordering = ['posicion_actividad', '-fecha_creacion']

    def __str__(self):
        return self.titulo_actividad