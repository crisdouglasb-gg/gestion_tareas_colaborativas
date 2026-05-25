from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

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

    # Mostrar TODAS las actividades
    # para todos los usuarios
    actividades_usuario = ActividadProyecto.objects.filter(
        actividad_archivada=False
    ).select_related(
        'columna_actual',
        'creado_por'
    ).order_by(
        'posicion_actividad'
    )

    # Últimas notificaciones del usuario
    notificaciones_usuario = (
        NotificacionSistema.objects.filter(
            usuario_destino=request.user
        ).order_by(
            '-fecha_creacion'
        )[:10]
    )

    contexto = {
        'espacios_usuario': espacios_usuario,
        'columnas_sistema': columnas_sistema,
        'actividades_usuario': actividades_usuario,
        'notificaciones_usuario': notificaciones_usuario,
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

        if not columna_inicial:
            columna_inicial = ColumnaEstado.objects.first()

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


@login_required(login_url='/login/')
def editar_actividad_frontend(request, actividad_id):

    """
    Permite editar actividades
    directamente desde el dashboard.
    """

    actividad = ActividadProyecto.objects.get(
        id=actividad_id
    )

    if request.method == 'POST':

        actividad.titulo_actividad = request.POST.get(
            'titulo_actividad'
        )

        actividad.descripcion_detallada = request.POST.get(
            'descripcion_actividad'
        )

        actividad.prioridad_actividad = request.POST.get(
            'prioridad_actividad'
        )

        actividad.fecha_limite = request.POST.get(
            'fecha_limite'
        )

        actividad.save()

        return redirect('dashboard')

    contexto = {
        'actividad': actividad
    }

    return render(
        request,
        'espacios/editar_actividad.html',
        contexto
    )


@login_required(login_url='/login/')
def eliminar_actividad_frontend(request, actividad_id):

    """
    Permite eliminar actividades
    desde el dashboard.
    """

    actividad = ActividadProyecto.objects.get(
        id=actividad_id
    )

    actividad.delete()

    return redirect('dashboard')


@login_required(login_url='/login/')
def subir_archivo_actividad(
    request,
    actividad_id
):

    """
    Permite subir archivos
    adjuntos a actividades.
    """

    actividad = ActividadProyecto.objects.get(
        id=actividad_id
    )

    if request.method == 'POST':

        archivo_recibido = request.FILES.get(
            'archivo_adjunto'
        )

        if archivo_recibido:

            ArchivoAdjuntoActividad.objects.create(

                actividad=actividad,

                usuario_subida=request.user,

                archivo=archivo_recibido

            )

            # Crear notificación
            if actividad.creado_por != request.user:

                NotificacionSistema.objects.create(

                    usuario_destino=actividad.creado_por,

                    mensaje_notificacion=(
                        f'{request.user.username} '
                        f'subió un archivo en: '
                        f'{actividad.titulo_actividad}'
                    ),

                    detalle_adicional=(
                        archivo_recibido.name
                    )

                )

        return redirect(
            'editar_actividad_frontend',
            actividad_id=actividad.id
        )


@login_required(login_url='/login/')
def crear_comentario(request, actividad_id):

    """
    Permite crear comentarios
    dinámicos desde frontend.
    """

    actividad = ActividadProyecto.objects.get(
        id=actividad_id
    )

    if request.method == 'POST':

        contenido_comentario = request.POST.get(
            'contenido_comentario'
        )

        nuevo_comentario = ComentarioActividad.objects.create(

            actividad_relacionada=actividad,

            usuario_comentario=request.user,

            contenido_comentario=contenido_comentario

        )

        # Evita notificarse a sí mismo
        if actividad.creado_por != request.user:

            NotificacionSistema.objects.create(

                usuario_destino=actividad.creado_por,

                mensaje_notificacion=(
                    f'{request.user.username} '
                    f'comentó tu actividad: '
                    f'{actividad.titulo_actividad}'
                ),

                detalle_adicional=(
                    nuevo_comentario.contenido_comentario
                )

            )

        return JsonResponse({

            'usuario':
                request.user.username,

            'comentario':
                nuevo_comentario.contenido_comentario

        })

    return JsonResponse({

        'error':
            'Método inválido'


    })


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
    contexto = {
        'espacios_usuario': espacios_usuario,
    }
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
    contexto = {
        'actividades_usuario': actividades_usuario,
    }
    return render(request, 'espacios/actividades.html', contexto)


@login_required(login_url='/login/')
def notificaciones_view(request):
    notificaciones_usuario = NotificacionSistema.objects.filter(
        usuario_destino=request.user
    ).order_by('-fecha_creacion')
    contexto = {
        'notificaciones_usuario': notificaciones_usuario,
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
>>>>>>> Stashed changes
