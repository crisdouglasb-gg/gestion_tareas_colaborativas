from django.urls import path

from .views import (
    dashboard_principal,
    mis_tareas,
    buscar_actividades,
)

urlpatterns = [
    path(
        '',
        dashboard_principal,
        name='dashboard'
    ),
    path(
        'mis-tareas/',
        mis_tareas,
        name='mis_tareas'
    ),
    path(
        'buscar/',
        buscar_actividades,
        name='buscar_actividades'
    ),
]
