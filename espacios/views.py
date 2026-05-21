from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import EspacioTrabajo, MiembroEspacio


@login_required
def dashboard_principal(request):
    """
    Dashboard principal del sistema.

    Muestra únicamente los espacios
    relacionados con el usuario autenticado.
    """

    espacios_usuario = EspacioTrabajo.objects.filter(
        miembros_asociados__usuario_miembro=request.user,
        miembros_asociados__miembro_activo=True
    ).distinct()

    contexto = {
        'espacios_usuario': espacios_usuario
    }

    return render(
        request,
        'espacios/dashboard.html',
        contexto
    )