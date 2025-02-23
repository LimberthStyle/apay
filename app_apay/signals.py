from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Dealer

@receiver(post_delete, sender=Dealer)
def eliminar_archivo_fotocheck(sender, instance, **kwargs):
    if instance.fotocheck:
        instance.fotocheck.delete(False)
