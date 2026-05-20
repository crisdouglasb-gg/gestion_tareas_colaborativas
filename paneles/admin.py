from django.contrib import admin

from .models import PanelTrabajo


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