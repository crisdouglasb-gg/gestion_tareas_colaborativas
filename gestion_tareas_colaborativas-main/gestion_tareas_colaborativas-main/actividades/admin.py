from django.contrib import admin

from .models import ActividadProyecto, AsignacionActividad


@admin.register(ActividadProyecto)
class ActividadProyectoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo_actividad',
        'columna_actual',
        'prioridad_actividad',
        'fecha_limite',
        'actividad_archivada'
    )

    list_filter = (
        'prioridad_actividad',
        'actividad_archivada'
    )

    search_fields = (
        'titulo_actividad',
    )

@admin.register(AsignacionActividad)
class AsignacionActividadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'actividad_relacionada',
        'usuario_asignado',
        'asignado_por',
        'asignacion_activa'
    )

    list_filter = (
        'asignacion_activa',
    )

    search_fields = (
        'usuario_asignado__username',
        'actividad_relacionada__titulo_actividad'
    )