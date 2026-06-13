from django.urls import path

from .views import (
    paneles_view,
    actualizar_columna_actividad,
)

urlpatterns = [
    path(
        'paneles/',
        paneles_view,
        name='paneles'
    ),
    path(
        'actualizar-columna/',
        actualizar_columna_actividad,
        name='actualizar_columna_actividad'
    ),
]
