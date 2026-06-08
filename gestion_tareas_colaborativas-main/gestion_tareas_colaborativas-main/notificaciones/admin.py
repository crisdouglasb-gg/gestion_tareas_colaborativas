from django.contrib import admin

from .models import NotificacionSistema


@admin.register(NotificacionSistema)
class NotificacionSistemaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario_destino',
        'mensaje_notificacion',
        'leida',
        'fecha_creacion'
    )

    list_filter = (
        'leida',
    )

    search_fields = (
        'mensaje_notificacion',
    )