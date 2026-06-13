from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from actividades.models import ActividadProyecto, ComentarioActividad
from notificaciones.models import NotificacionSistema


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.email = request.POST.get('email', '')
            usuario.first_name = request.POST.get('first_name', '')
            usuario.save()
            login(request, usuario)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required(login_url='/login/')
def perfil_usuario(request):
    total_tareas = ActividadProyecto.objects.filter(
        creado_por=request.user,
        actividad_archivada=False
    ).count()

    total_comentarios = ComentarioActividad.objects.filter(
        usuario_comentario=request.user
    ).count()

    notif_no_leidas = NotificacionSistema.objects.filter(
        usuario_destino=request.user,
        leida=False
    ).count()

    if request.method == 'POST':
        from django.contrib.auth import update_session_auth_hash
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmar = request.POST.get('password_confirmar')

        if not request.user.check_password(password_actual):
            messages.error(request, 'La contraseña actual es incorrecta.')
        elif password_nueva != password_confirmar:
            messages.error(request, 'Las contraseñas nuevas no coinciden.')
        elif len(password_nueva) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
        else:
            request.user.set_password(password_nueva)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada correctamente.')
            return redirect('perfil_usuario')

    contexto = {
        'total_tareas': total_tareas,
        'total_comentarios': total_comentarios,
        'notif_no_leidas': notif_no_leidas,
    }
    return render(request, 'usuarios/perfil.html', contexto)
