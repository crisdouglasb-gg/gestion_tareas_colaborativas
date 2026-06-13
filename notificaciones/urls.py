from django.urls import path

from .views import (
    notificaciones_view,
    marcar_notificaciones_leidas,
)

urlpatterns = [
    path(
        'notificaciones/',
        notificaciones_view,
        name='notificaciones'
    ),
    path(
        'marcar-notificaciones-leidas/',
        marcar_notificaciones_leidas,
        name='marcar_notificaciones_leidas'
    ),
]
