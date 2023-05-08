from django.db import models
from django.conf import settings

class Relacion(models.Model):
    relacion_id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seguidos")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seguidores")
    fecha = models.DateField()
    pendiente = models.BooleanField()