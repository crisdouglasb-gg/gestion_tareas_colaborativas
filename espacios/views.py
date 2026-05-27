from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import models

from espacios.models import EspacioTrabajo
from paneles.models import ColumnaEstado
from actividades.models import (
    ActividadProyecto,
    ComentarioActividad,
    ArchivoAdjuntoActividad,
)

from notificaciones.models import (
    NotificacionSistema
)


@login_required(login_url='/login/')
def dashboard_principal(request):

    espacios_usuario = EspacioTrabajo.objects.filter(
        miembros_asociados__usuario_miembro=request.user,
        miembros_asociados__miembro_activo=True
    ).distinct()

    columnas_sistema = ColumnaEstado.objects.all().order_by('posicion_columna')

    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related('columna_actual', 'creado_por').order_by('posicion_actividad')

    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')[:10]

    contexto = {
        'espacios_usuario': espacios_usuario,
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
        'notificaciones_usuario': notificaciones_usuario,
    }

    return render(request, 'espacios/dashboard.html', contexto)


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


@login_required(login_url='/login/')
def crear_actividad_frontend(request):

    if request.method == 'POST':
        titulo_actividad = request.POST.get('titulo_actividad')
        descripcion_actividad = request.POST.get('descripcion_actividad')
        prioridad_actividad = request.POST.get('prioridad_actividad')
        fecha_limite = request.POST.get('fecha_limite')

        columna_inicial = ColumnaEstado.objects.filter(nombre_columna='Pendiente').first()

        ActividadProyecto.objects.create(
            columna_actual=columna_inicial,
            creado_por=request.user,
            titulo_actividad=titulo_actividad,
            descripcion_detallada=descripcion_actividad,
            prioridad_actividad=prioridad_actividad,
            fecha_limite=fecha_limite
        )

        return redirect('dashboard')

    return render(request, 'espacios/crear_actividad.html')


@login_required(login_url='/login/')
def editar_actividad_frontend(request, actividad_id):

    from django.contrib.auth.models import User
    from actividades.models import AsignacionActividad

    actividad = ActividadProyecto.objects.get(id=actividad_id)

    if request.method == 'POST':
        actividad.titulo_actividad = request.POST.get('titulo_actividad')
        actividad.descripcion_detallada = request.POST.get('descripcion_actividad')
        actividad.prioridad_actividad = request.POST.get('prioridad_actividad')
        actividad.fecha_limite = request.POST.get('fecha_limite')
        actividad.save()
        return redirect('dashboard')

    asignados = AsignacionActividad.objects.filter(
        actividad_relacionada=actividad,
        asignacion_activa=True
    ).select_related('usuario_asignado')

    ids_asignados = asignados.values_list('usuario_asignado__id', flat=True)

    usuarios_disponibles = User.objects.exclude(
        id__in=ids_asignados
    ).order_by('username')

    contexto = {
        'actividad': actividad,
        'asignados': asignados,
        'usuarios_disponibles': usuarios_disponibles,
    }
    return render(request, 'espacios/editar_actividad.html', contexto)


@login_required(login_url='/login/')
def eliminar_actividad_frontend(request, actividad_id):

    actividad = ActividadProyecto.objects.get(id=actividad_id)
    actividad.delete()
    return redirect('dashboard')


@login_required(login_url='/login/')
def subir_archivo_actividad(request, actividad_id):

    actividad = ActividadProyecto.objects.get(id=actividad_id)

    if request.method == 'POST':
        archivo_recibido = request.FILES.get('archivo_adjunto')
        if archivo_recibido:
            ArchivoAdjuntoActividad.objects.create(
                actividad=actividad,
                usuario_subida=request.user,
                archivo=archivo_recibido
            )
            if actividad.creado_por != request.user:
                NotificacionSistema.objects.create(
                    usuario_destino=actividad.creado_por,
                    mensaje_notificacion=(
                        f'{request.user.username} subió un archivo en: {actividad.titulo_actividad}'
                    ),
                    detalle_adicional=archivo_recibido.name
                )

        return redirect('editar_actividad_frontend', actividad_id=actividad.id)


@login_required(login_url='/login/')
def crear_comentario(request, actividad_id):

    actividad = ActividadProyecto.objects.get(id=actividad_id)

    if request.method == 'POST':
        contenido_comentario = request.POST.get('contenido_comentario')
        nuevo_comentario = ComentarioActividad.objects.create(
            actividad_relacionada=actividad,
            usuario_comentario=request.user,
            contenido_comentario=contenido_comentario
        )
        if actividad.creado_por != request.user:
            NotificacionSistema.objects.create(
                usuario_destino=actividad.creado_por,
                mensaje_notificacion=(
                    f'{request.user.username} comentó tu actividad: {actividad.titulo_actividad}'
                ),
                detalle_adicional=nuevo_comentario.contenido_comentario
            )
        return JsonResponse({
            'usuario': request.user.username,
            'comentario': nuevo_comentario.contenido_comentario
        })

    return JsonResponse({'error': 'Método inválido'})


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
def espacios_view(request):
    espacios_usuario = EspacioTrabajo.objects.filter(
        miembros_asociados__usuario_miembro=request.user,
        miembros_asociados__miembro_activo=True
    ).distinct()
    contexto = {'espacios_usuario': espacios_usuario}
    return render(request, 'espacios/espacios.html', contexto)


@login_required(login_url='/login/')
def paneles_view(request):
    columnas_sistema = ColumnaEstado.objects.all().order_by('posicion_columna')
    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related('columna_actual', 'creado_por').order_by('posicion_actividad')
    contexto = {
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
    }
    return render(request, 'espacios/paneles.html', contexto)


@login_required(login_url='/login/')
def actividades_view(request):
    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related('columna_actual', 'creado_por').order_by('posicion_actividad')
    contexto = {'actividades_usuario': actividades_usuario}
    return render(request, 'espacios/actividades.html', contexto)


@login_required(login_url='/login/')
def notificaciones_view(request):
    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')
    no_leidas = notificaciones_usuario.filter(leida=False).count()
    contexto = {
        'notificaciones_usuario': notificaciones_usuario,
        'no_leidas': no_leidas,
    }
    return render(request, 'espacios/notificaciones.html', contexto)


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
    return render(request, 'registration/registro.html', {'form': form})


@login_required(login_url='/login/')
def marcar_notificaciones_leidas(request):
    """
    Marca todas las notificaciones del usuario como leídas.
    """
    if request.method == 'POST':
        NotificacionSistema.objects.filter(
            usuario_destino=request.user,
            leida=False
        ).update(leida=True)
        messages.success(request, 'Todas las notificaciones fueron marcadas como leídas.')
    return redirect('notificaciones')


@login_required(login_url='/login/')
def perfil_usuario(request):
    """
    Muestra el perfil del usuario con sus estadísticas.
    """
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
    return render(request, 'espacios/perfil.html', contexto)


@login_required(login_url='/login/')
def asignar_usuario_actividad(request, actividad_id):
    """
    Asigna o desasigna un usuario a una actividad.
    """
    from django.contrib.auth.models import User
    from actividades.models import AsignacionActividad

    actividad = ActividadProyecto.objects.get(id=actividad_id)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        accion = request.POST.get('accion')
        usuario = User.objects.get(id=usuario_id)

        if accion == 'asignar':
            AsignacionActividad.objects.get_or_create(
                actividad_relacionada=actividad,
                usuario_asignado=usuario,
                defaults={'asignado_por': request.user}
            )
            messages.success(request, f'{usuario.username} asignado correctamente.')

        elif accion == 'desasignar':
            AsignacionActividad.objects.filter(
                actividad_relacionada=actividad,
                usuario_asignado=usuario
            ).delete()
            messages.success(request, f'{usuario.username} removido de la actividad.')

    return redirect('editar_actividad_frontend', actividad_id=actividad_id)


@login_required(login_url='/login/')
def buscar_actividades(request):
    """
    Búsqueda global de actividades
    por título o descripción.
    """
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