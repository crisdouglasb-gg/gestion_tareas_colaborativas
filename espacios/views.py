from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from espacios.models import EspacioTrabajo, MiembroEspacio
from paneles.models import ColumnaEstado
from actividades.models import ActividadProyecto


@login_required
def dashboard_principal(request):
    """
    Dashboard principal estilo Kanban.

    Muestra espacios del usuario y
    actividades agrupadas por columnas.
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