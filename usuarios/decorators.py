from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import PerfilUsuario


def rol_requerido(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login/')
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            perfil, _ = PerfilUsuario.objects.get_or_create(
                usuario=request.user,
                defaults={'rol': 'MIEMBRO'}
            )
            if perfil.rol not in roles:
                messages.error(request, f'Tu rol de {perfil.get_rol_display()} no tiene permisos para realizar esta acción.')
                referer = request.META.get('HTTP_REFERER')
                return redirect(referer if referer else 'dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
