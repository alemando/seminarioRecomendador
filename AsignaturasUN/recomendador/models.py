from django.db import models

# Create your models here.

class Asignatura(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=60)
    estado = models.BooleanField()

#Clase que asocia la asignatura a el usuario y la calificacion otorgada
class Calificacion(models.Model):
    producto = models.ForeignKey(Asignatura, on_delete=models.CASCADE,)
    calificacion = models.IntegerField()
    usuario =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

