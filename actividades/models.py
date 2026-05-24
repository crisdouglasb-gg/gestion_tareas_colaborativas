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
    
class AsignacionActividad(models.Model):
    # Relación con la actividad asignada
    actividad_relacionada = models.ForeignKey(
        ActividadProyecto,
        on_delete=models.CASCADE,
        related_name='usuarios_asignados'
    )

    # Usuario responsable de la actividad
    usuario_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actividades_asignadas'
    )

    # Usuario que realizó la asignación
    asignado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='asignaciones_realizadas'
    )

    # Permite mantener historial sin borrar registros
    asignacion_activa = models.BooleanField(
        default=True
    )

    # Fecha automática de asignación
    fecha_asignacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Asignación de actividad'
        verbose_name_plural = 'Asignaciones de actividades'

        # Evita duplicar asignaciones
        unique_together = (
            'actividad_relacionada',
            'usuario_asignado'
        )

    def __str__(self):
        return f'{self.usuario_asignado} → {self.actividad_relacionada}'
    
class ComentarioActividad(models.Model):

    # Actividad relacionada
    actividad_relacionada = models.ForeignKey(
        ActividadProyecto,
        on_delete=models.CASCADE,
        related_name='comentarios_actividad'
    )

    # Usuario que comenta
    usuario_comentario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comentarios_realizados'
    )

    # Contenido del comentario
    contenido_comentario = models.TextField()

    # Fecha automática
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

        ordering = ['-fecha_creacion']

    def __str__(self):

        return (
            f'Comentario de '
            f'{self.usuario_comentario}'
        )