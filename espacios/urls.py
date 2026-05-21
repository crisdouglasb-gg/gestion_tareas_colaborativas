from django.urls import path

from .views import dashboard_principal


urlpatterns = [
    path(
        '',
        dashboard_principal,
        name='dashboard_principal'
    ),
]