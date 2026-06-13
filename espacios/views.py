import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models

from espacios.models import EspacioTrabajo
from paneles.models import ColumnaEstado
from actividades.models import ActividadProyecto
from notificaciones.models import NotificacionSistema


@login_required(login_url='/login/')
def dashboard_principal(request):

    espacios_usuario = EspacioTrabajo.objects.filter(
        miembros_asociados__usuario_miembro=request.user,
        miembros_asociados__miembro_activo=True
    ).distinct()

    columnas_sistema = ColumnaEstado.objects.all().order_by('posicion_columna')

    actividades_usuario = list(
        ActividadProyecto.objects.filter(actividad_archivada=False)
        .select_related('columna_actual', 'creado_por')
        .order_by('posicion_actividad')
    )

    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')[:10]

    notif_no_leidas = NotificacionSistema.objects.filter(
        usuario_destino=request.user, leida=False
    ).count()

    col_counts = defaultdict(int)
    pri_counts = {'BAJA': 0, 'MEDIA': 0, 'ALTA': 0, 'URGENTE': 0}
    pendientes = en_proceso = completadas = 0

    for act in actividades_usuario:
        nombre = act.columna_actual.nombre_columna if act.columna_actual else 'Sin columna'
        col_counts[nombre] += 1
        p = act.prioridad_actividad
        if p in pri_counts:
            pri_counts[p] += 1
        nl = nombre.lower()
        if 'pendiente' in nl:
            pendientes += 1
        elif 'progres' in nl:
            en_proceso += 1
        elif 'complet' in nl:
            completadas += 1

    contexto = {
        'espacios_usuario': espacios_usuario,
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
        'notificaciones_usuario': notificaciones_usuario,
        'notif_no_leidas': notif_no_leidas,
        'pendientes': pendientes,
        'en_proceso': en_proceso,
        'completadas': completadas,
        'chart_col_labels': json.dumps(list(col_counts.keys())),
        'chart_col_data': json.dumps(list(col_counts.values())),
        'chart_pri_data': json.dumps([pri_counts['BAJA'], pri_counts['MEDIA'], pri_counts['ALTA'], pri_counts['URGENTE']]),
    }

    return render(request, 'espacios/dashboard.html', contexto)


@login_required(login_url='/login/')
def mis_tareas(request):
    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related('columna_actual', 'creado_por').order_by('posicion_actividad')
    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')[:10]
    contexto = {
        'actividades_usuario': actividades_usuario,
        'notificaciones_usuario': notificaciones_usuario,
    }
    return render(request, 'espacios/mis_tareas.html', contexto)


@login_required(login_url='/login/')
def buscar_actividades(request):
    consulta = request.GET.get('q', '')
    resultados = []

    if consulta:
        resultados = ActividadProyecto.objects.filter(
            actividad_archivada=False
        ).filter(
            models.Q(titulo_actividad__icontains=consulta) |
            models.Q(descripcion_detallada__icontains=consulta)
        ).select_related('columna_actual', 'creado_por').order_by('-fecha_creacion')

    contexto = {
        'consulta': consulta,
        'resultados': resultados,
        'total': len(resultados),
    }
    return render(request, 'espacios/busqueda.html', contexto)
