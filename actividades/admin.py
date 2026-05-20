from django.contrib import admin

from .models import ActividadProyecto


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