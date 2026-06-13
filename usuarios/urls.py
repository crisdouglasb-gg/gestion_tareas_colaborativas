from django.urls import path

from .views import (
    registro_usuario,
    perfil_usuario,
    gestionar_usuarios,
    eliminar_usuario,
    editar_nombre_usuario,
)

urlpatterns = [
    path(
        'registro/',
        registro_usuario,
        name='registro'
    ),
    path(
        'perfil/',
        perfil_usuario,
        name='perfil_usuario'
    ),
    path(
        'usuarios/',
        gestionar_usuarios,
        name='gestionar_usuarios'
    ),
    path(
        'usuarios/eliminar/<int:usuario_id>/',
        eliminar_usuario,
        name='eliminar_usuario'
    ),
    path(
        'usuarios/editar/<int:usuario_id>/',
        editar_nombre_usuario,
        name='editar_nombre_usuario'
    ),
]
