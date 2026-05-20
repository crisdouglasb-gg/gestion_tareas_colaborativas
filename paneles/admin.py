from django.contrib import admin

from .models import PanelTrabajo, ColumnaEstado

@admin.register(PanelTrabajo)
class PanelTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_panel',
        'espacio_padre',
        'posicion_visual',
        'panel_archivado'
    )

    search_fields = (
        'nombre_panel',
    )

    list_filter = (
        'panel_archivado',
    )

@admin.register(ColumnaEstado)
class ColumnaEstadoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_columna',
        'panel_relacionado',
        'posicion_columna',
        'columna_archivada'
    )

    list_filter = (
        'columna_archivada',
    )

    search_fields = (
        'nombre_columna',
    )    