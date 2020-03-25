# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

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

