from django.conf import settings
from django.db import models


class PerfilUsuario(models.Model):

    ROLES = (
        ('ADMIN', 'Administrador'),
        ('LIDER', 'Líder'),
        ('MIEMBRO', 'Miembro'),
    )

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil'
    )

    rol = models.CharField(
        max_length=10,
        choices=ROLES,
        default='MIEMBRO'
    )

    def es_admin(self):
        return self.rol == 'ADMIN'

    def es_lider_o_superior(self):
        return self.rol in ('ADMIN', 'LIDER')

    class Meta:
        verbose_name = 'Perfil de usuario'
        verbose_name_plural = 'Perfiles de usuario'

    def __str__(self):
        return f'{self.usuario.username} — {self.get_rol_display()}'
