from django.urls import path

from .views import (
    dashboard_principal,
    actualizar_columna_actividad,
    crear_actividad_frontend,
    editar_actividad_frontend,
    eliminar_actividad_frontend,
    subir_archivo_actividad
)

urlpatterns = [

    path(
        '',
        dashboard_principal,
        name='dashboard'
    ),

    path(
        'actualizar-columna/',
        actualizar_columna_actividad,
        name='actualizar_columna_actividad'
    ),

    path(
        'crear-actividad/',
        crear_actividad_frontend,
        name='crear_actividad_frontend'
    ),

    path(
        'editar-actividad/<int:actividad_id>/',
        editar_actividad_frontend,
        name='editar_actividad_frontend'
    ),

    path(
    'eliminar-actividad/<int:actividad_id>/',
    eliminar_actividad_frontend,
    name='eliminar_actividad_frontend'
),
path(
    'subir-archivo/<int:actividad_id>/',
    subir_archivo_actividad,
    name='subir_archivo_actividad'
),
]