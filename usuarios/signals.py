from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import PerfilUsuario

User = get_user_model()


@receiver(post_save, sender=User)
def crear_perfil_al_registrar(sender, instance, created, **kwargs):
    if created:
        rol_inicial = 'ADMIN' if instance.is_superuser else 'MIEMBRO'
        PerfilUsuario.objects.create(usuario=instance, rol=rol_inicial)
