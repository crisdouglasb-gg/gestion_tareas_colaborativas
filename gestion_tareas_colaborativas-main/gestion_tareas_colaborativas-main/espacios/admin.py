from django.contrib import admin

from .models import EspacioTrabajo

from .models import MiembroEspacio


@admin.register(EspacioTrabajo)
class EspacioTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_espacio',
        'propietario',
        'fecha_creacion',
        'espacio_archivado'
    )

    search_fields = (
        'nombre_espacio',
    )

    list_filter = (
        'espacio_archivado',
        'fecha_creacion'
    )

@admin.register(MiembroEspacio)
class MiembroEspacioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario_miembro',
        'espacio_relacionado',
        'rol_participacion',
        'miembro_activo'
    )

    list_filter = (
        'rol_participacion',
        'miembro_activo'
    )

    search_fields = (
        'usuario_miembro__username',
        'espacio_relacionado__nombre_espacio'
    )    