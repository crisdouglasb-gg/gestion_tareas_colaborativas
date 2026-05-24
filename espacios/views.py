from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

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

    # Actividades creadas por el usuario
    actividades_creadas = ActividadProyecto.objects.filter(
        creado_por=request.user,
        actividad_archivada=False
    )

    # Actividades asignadas al usuario
    actividades_asignadas = ActividadProyecto.objects.filter(
        usuarios_asignados__usuario_asignado=request.user,
        usuarios_asignados__asignacion_activa=True,
        actividad_archivada=False
    )

    # Unifica actividades sin duplicados
    actividades_usuario = (
        actividades_creadas |
        actividades_asignadas
    ).distinct().select_related(
        'columna_actual'
    ).order_by(
        'posicion_actividad'
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
@login_required(login_url='/login/')
def crear_actividad_frontend(request):

    """
    Permite crear nuevas actividades
    desde el formulario visual frontend.
    """

    if request.method == 'POST':

        titulo_actividad = request.POST.get(
            'titulo_actividad'
        )

        descripcion_actividad = request.POST.get(
            'descripcion_actividad'
        )

        prioridad_actividad = request.POST.get(
            'prioridad_actividad'
        )

        fecha_limite = request.POST.get(
            'fecha_limite'
        )

        columna_inicial = ColumnaEstado.objects.filter(
            nombre_columna='Pendiente'
        ).first()

        ActividadProyecto.objects.create(

            columna_actual=columna_inicial,

            creado_por=request.user,

            titulo_actividad=titulo_actividad,

            descripcion_detallada=descripcion_actividad,

            prioridad_actividad=prioridad_actividad,

            fecha_limite=fecha_limite

        )

        return redirect('dashboard')

    return render(
        request,
        'espacios/crear_actividad.html'
    )