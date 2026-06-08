from django.conf import settings
from django.db import models


class EspacioTrabajo(models.Model):
    nombre_espacio = models.CharField(
        max_length=120,
        verbose_name='Nombre del espacio'
    )

    descripcion_general = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='espacios_creados'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    espacio_archivado = models.BooleanField(
        default=False
    )

    class Meta:
        verbose_name = 'Espacio de trabajo'
        verbose_name_plural = 'Espacios de trabajo'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre_espacio
    
class MiembroEspacio(models.Model):
    ROLES_DISPONIBLES = (
        ('ADMINISTRADOR', 'Administrador'),
        ('COLABORADOR', 'Colaborador'),
        ('LECTOR', 'Lector'),
    )

    espacio_relacionado = models.ForeignKey(
        EspacioTrabajo,
        on_delete=models.CASCADE,
        related_name='miembros_asociados'
    )

    usuario_miembro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='espacios_participando'
    )

    rol_participacion = models.CharField(
        max_length=20,
        choices=ROLES_DISPONIBLES,
        default='COLABORADOR'
    )

    fecha_union = models.DateTimeField(
        auto_now_add=True
    )

    miembro_activo = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = 'Miembro del espacio'
        verbose_name_plural = 'Miembros de espacios'

        unique_together = (
            'espacio_relacionado',
            'usuario_miembro'
        )

    def __str__(self):
        return f'{self.usuario_miembro} -> {self.espacio_relacionado}'    