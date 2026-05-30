from django.urls import path

from .views import (
    dashboard_principal,
    actualizar_columna_actividad,
    crear_actividad_frontend,
    editar_actividad_frontend,
    eliminar_actividad_frontend,
    subir_archivo_actividad,
    crear_comentario,
    mis_tareas,
    espacios_view,
    paneles_view,
    actividades_view,
    notificaciones_view,
    registro_usuario,
    marcar_notificaciones_leidas,
    perfil_usuario,
    asignar_usuario_actividad,
    buscar_actividades,
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

    path(
        'crear-comentario/<int:actividad_id>/',
        crear_comentario,
        name='crear_comentario'
    ),

    path(
        'mis-tareas/',
        mis_tareas,
        name='mis_tareas'
    ),


    path(
        'paneles/',
        paneles_view,
        name='paneles'
    ),

    path(
        'actividades/',
        actividades_view,
        name='actividades'
    ),

    path(
        'notificaciones/',
        notificaciones_view,
        name='notificaciones'
    ),

    path(
        'registro/',
        registro_usuario,
        name='registro'
    ),

    path(
        'marcar-notificaciones-leidas/',
        marcar_notificaciones_leidas,
        name='marcar_notificaciones_leidas'
    ),

    path(
        'perfil/',
        perfil_usuario,
        name='perfil_usuario'
    ),

    path(
        'asignar-usuario/<int:actividad_id>/',
        asignar_usuario_actividad,
        name='asignar_usuario_actividad'
    ),

    path(
        'buscar/',
        buscar_actividades,
        name='buscar_actividades'
    ),

]