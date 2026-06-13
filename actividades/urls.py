from django.urls import path

from .views import (
    actividades_view,
    crear_actividad_frontend,
    editar_actividad_frontend,
    eliminar_actividad_frontend,
    subir_archivo_actividad,
    crear_comentario,
    asignar_usuario_actividad,
)

urlpatterns = [
    path(
        'actividades/',
        actividades_view,
        name='actividades'
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
    path(
        'crear-comentario/<int:actividad_id>/',
        crear_comentario,
        name='crear_comentario'
    ),
    path(
        'asignar-usuario/<int:actividad_id>/',
        asignar_usuario_actividad,
        name='asignar_usuario_actividad'
    ),
]
