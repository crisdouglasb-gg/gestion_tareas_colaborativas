from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='usuarios/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/login/'
        ),
        name='logout'
    ),

    path('', include('espacios.urls')),
    path('', include('actividades.urls')),
    path('', include('paneles.urls')),
    path('', include('notificaciones.urls')),
    path('', include('usuarios.urls')),

]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
