from django.urls import path

from .views import (
    registro_usuario,
    perfil_usuario,
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
]
