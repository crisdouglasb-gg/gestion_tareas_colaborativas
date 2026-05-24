from django.contrib import admin

from .models import (
    ActividadProyecto,
    AsignacionActividad,
    ComentarioActividad
)

admin.site.register(ActividadProyecto)

admin.site.register(AsignacionActividad)

admin.site.register(ComentarioActividad)