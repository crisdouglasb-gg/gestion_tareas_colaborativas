from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from actividades.models import ActividadProyecto, ComentarioActividad, ArchivoAdjuntoActividad
from paneles.models import ColumnaEstado
from notificaciones.models import NotificacionSistema


@login_required(login_url='/login/')
def actividades_view(request):
    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related('columna_actual', 'creado_por').order_by('posicion_actividad')
    contexto = {'actividades_usuario': actividades_usuario}
    return render(request, 'actividades/actividades.html', contexto)


@login_required(login_url='/login/')
def crear_actividad_frontend(request):
    if request.method == 'POST':
        titulo_actividad = request.POST.get('titulo_actividad')
        descripcion_actividad = request.POST.get('descripcion_actividad')
        prioridad_actividad = request.POST.get('prioridad_actividad')
        fecha_limite = request.POST.get('fecha_limite') or None

        columna_inicial = ColumnaEstado.objects.filter(nombre_columna='Pendiente').first()

        nueva_actividad = ActividadProyecto.objects.create(
            columna_actual=columna_inicial,
            creado_por=request.user,
            titulo_actividad=titulo_actividad,
            descripcion_detallada=descripcion_actividad,
            prioridad_actividad=prioridad_actividad,
            fecha_limite=fecha_limite
        )

        return redirect('editar_actividad_frontend', actividad_id=nueva_actividad.id)

    return render(request, 'actividades/crear_actividad.html')


@login_required(login_url='/login/')
def editar_actividad_frontend(request, actividad_id):
    from django.contrib.auth.models import User
    from actividades.models import AsignacionActividad

    actividad = get_object_or_404(ActividadProyecto, id=actividad_id)

    if request.method == 'POST':
        actividad.titulo_actividad = request.POST.get('titulo_actividad')
        actividad.descripcion_detallada = request.POST.get('descripcion_actividad')
        actividad.prioridad_actividad = request.POST.get('prioridad_actividad')
        actividad.fecha_limite = request.POST.get('fecha_limite') or None
        actividad.save()
        messages.success(request, f'Actividad "{actividad.titulo_actividad}" guardada correctamente.')
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
    return render(request, 'actividades/editar_actividad.html', contexto)


@login_required(login_url='/login/')
def eliminar_actividad_frontend(request, actividad_id):
    actividad = get_object_or_404(ActividadProyecto, id=actividad_id)
    if request.method == 'POST':
        titulo = actividad.titulo_actividad
        actividad.delete()
        messages.success(request, f'Actividad "{titulo}" eliminada.')
        return redirect('actividades')
    return render(request, 'actividades/confirmar_eliminar.html', {'actividad': actividad})


@login_required(login_url='/login/')
def subir_archivo_actividad(request, actividad_id):
    actividad = get_object_or_404(ActividadProyecto, id=actividad_id)

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
    actividad = get_object_or_404(ActividadProyecto, id=actividad_id)

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
def asignar_usuario_actividad(request, actividad_id):
    from django.contrib.auth.models import User
    from actividades.models import AsignacionActividad

    actividad = get_object_or_404(ActividadProyecto, id=actividad_id)

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
