from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from actividades.models import ActividadProyecto, ComentarioActividad
from notificaciones.models import NotificacionSistema
from usuarios.decorators import rol_requerido
from usuarios.models import PerfilUsuario


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


@login_required(login_url='/login/')
@rol_requerido('ADMIN')
def editar_nombre_usuario(request, usuario_id):
    from django.contrib.auth.models import User

    if request.method != 'POST':
        return redirect('gestionar_usuarios')

    usuario = get_object_or_404(User, id=usuario_id)
    nuevo_username = request.POST.get('nuevo_username', '').strip()
    nuevo_nombre = request.POST.get('nuevo_nombre', '').strip()

    if nuevo_username and nuevo_username != usuario.username:
        if User.objects.filter(username=nuevo_username).exclude(id=usuario_id).exists():
            messages.error(request, f'El nombre de usuario "{nuevo_username}" ya está en uso.')
            return redirect('gestionar_usuarios')
        usuario.username = nuevo_username

    if nuevo_nombre != usuario.first_name:
        usuario.first_name = nuevo_nombre

    usuario.save()
    messages.success(request, f'Datos de "{usuario.username}" actualizados correctamente.')
    return redirect('gestionar_usuarios')


@login_required(login_url='/login/')
@rol_requerido('ADMIN')
def eliminar_usuario(request, usuario_id):
    from django.contrib.auth.models import User

    if request.method != 'POST':
        return redirect('gestionar_usuarios')

    usuario_a_eliminar = get_object_or_404(User, id=usuario_id)

    if usuario_a_eliminar == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('gestionar_usuarios')

    if usuario_a_eliminar.is_superuser:
        messages.error(request, f'No se puede eliminar a "{usuario_a_eliminar.username}" porque es superusuario. Usa el panel de administración.')
        return redirect('gestionar_usuarios')

    confirmacion = request.POST.get('confirmacion_username', '')
    if confirmacion != usuario_a_eliminar.username:
        messages.error(request, 'El nombre de usuario no coincide. No se eliminó nada.')
        return redirect('gestionar_usuarios')

    nombre = usuario_a_eliminar.username
    usuario_a_eliminar.delete()
    messages.success(request, f'Usuario "{nombre}" eliminado correctamente junto con todos sus datos.')
    return redirect('gestionar_usuarios')


@login_required(login_url='/login/')
@rol_requerido('ADMIN')
def gestionar_usuarios(request):
    from django.contrib.auth.models import User

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nuevo_rol = request.POST.get('rol')
        if nuevo_rol in ('ADMIN', 'LIDER', 'MIEMBRO'):
            perfil = PerfilUsuario.objects.get(usuario_id=usuario_id)
            if perfil.usuario != request.user:
                perfil.rol = nuevo_rol
                perfil.save()
                messages.success(request, f'Rol de {perfil.usuario.username} actualizado a {perfil.get_rol_display()}.')
            else:
                messages.error(request, 'No puedes cambiar tu propio rol.')
        return redirect('gestionar_usuarios')

    usuarios = User.objects.select_related('perfil').order_by('-is_superuser', 'username')
    for u in usuarios:
        if not hasattr(u, 'perfil') or u.perfil is None:
            PerfilUsuario.objects.get_or_create(
                usuario=u,
                defaults={'rol': 'ADMIN' if u.is_superuser else 'MIEMBRO'}
            )

    usuarios = User.objects.select_related('perfil').order_by('-is_superuser', 'username')
    return render(request, 'usuarios/gestionar_usuarios.html', {'usuarios': usuarios})
