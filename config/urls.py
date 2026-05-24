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

    # Login del sistema
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='usuarios/login.html'
        ),
        name='login'
    ),

    # Logout del sistema
    path(
    'logout/',
    auth_views.LogoutView.as_view(
        next_page='/login/'
    ),
    name='logout'
),

    # Dashboard principal
    path(
        '',
        include('espacios.urls')
    ),

]
urlpatterns += static(

    settings.MEDIA_URL,

    document_root=settings.MEDIA_ROOT

)