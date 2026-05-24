
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from espacios.models import EspacioTrabajo
from paneles.models import ColumnaEstado
from actividades.models import ActividadProyecto


@login_required(login_url='/login/')
def dashboard_principal(request):

    """
    Dashboard principal del sistema Kanban.
    """

    espacios_usuario = EspacioTrabajo.objects.filter(
        miembros_asociados__usuario_miembro=request.user,
        miembros_asociados__miembro_activo=True
    ).distinct()

    columnas_sistema = ColumnaEstado.objects.all().order_by(
        'posicion_columna'
    )

    actividades_usuario = ActividadProyecto.objects.filter(
        creado_por=request.user,
        actividad_archivada=False
    ).select_related(
        'columna_actual'
    )

    contexto = {
        'espacios_usuario': espacios_usuario,
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
    }

    return render(
        request,
        'espacios/dashboard.html',
        contexto
    )


@login_required
def actualizar_columna_actividad(request):

    """
    Actualiza la columna de una actividad
    cuando el usuario mueve tarjetas
    mediante drag and drop.
    """

    if request.method == 'POST':

        actividad_id = request.POST.get(
            'actividad_id'
        )

        columna_destino_id = request.POST.get(
            'columna_destino_id'
        )

        try:

            actividad = ActividadProyecto.objects.get(
                id=actividad_id
            )

            nueva_columna = ColumnaEstado.objects.get(
                id=columna_destino_id
            )

            actividad.columna_actual = nueva_columna

            actividad.save()

            return JsonResponse({
                'estado': 'ok',
                'mensaje': (
                    'La actividad fue movida '
                    'correctamente.'
                )
            })

        except Exception as error:

            return JsonResponse({
                'estado': 'error',
                'mensaje': str(error)
            })

    return JsonResponse({
        'estado': 'error',
        'mensaje': 'Método HTTP inválido.'
    })