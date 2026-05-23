from django.urls import path

from .views import (
    dashboard_principal,
    actualizar_columna_actividad
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

]