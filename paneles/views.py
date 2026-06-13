from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from actividades.models import ActividadProyecto, AsignacionActividad
from paneles.models import ColumnaEstado


@login_required(login_url='/login/')
def paneles_view(request):
    columnas_sistema = ColumnaEstado.objects.all().order_by('posicion_columna')
    actividades_usuario = list(
        ActividadProyecto.objects.filter(actividad_archivada=False)
        .select_related('columna_actual', 'creado_por')
        .order_by('posicion_actividad')
    )
    asignaciones = AsignacionActividad.objects.filter(
        asignacion_activa=True,
        actividad_relacionada__in=actividades_usuario
    ).select_related('usuario_asignado', 'actividad_relacionada')

    asignados_por_actividad = {}
    for a in asignaciones:
        aid = a.actividad_relacionada_id
        if aid not in asignados_por_actividad:
            asignados_por_actividad[aid] = []
        asignados_por_actividad[aid].append(a.usuario_asignado)

    for act in actividades_usuario:
        act.usuarios_asignados_list = asignados_por_actividad.get(act.id, [])

    contexto = {
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
    }
    return render(request, 'paneles/paneles.html', contexto)


@login_required
def actualizar_columna_actividad(request):
    if request.method == 'POST':
        actividad_id = request.POST.get('actividad_id')
        columna_destino_id = request.POST.get('columna_destino_id')
        try:
            actividad = ActividadProyecto.objects.get(id=actividad_id)
            nueva_columna = ColumnaEstado.objects.get(id=columna_destino_id)
            actividad.columna_actual = nueva_columna
            actividad.save()
            return JsonResponse({'estado': 'ok', 'mensaje': 'La actividad fue movida correctamente.'})
        except Exception as error:
            return JsonResponse({'estado': 'error', 'mensaje': str(error)})

    return JsonResponse({'estado': 'error', 'mensaje': 'Método HTTP inválido.'})
