# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import logout
from recomendador.models import Asignatura, Calificacion
from recomendador.rate import recomendacion

# Create your views here.

@login_required
def indexView(request):
    usuario_actual = User.objects.get(username = request.user)
    if request.method == "POST":
        asignatura_obj = Asignatura.objects.get(codigo=request.POST.get("codigo"))
        calificacion_usuario = request.POST.get("calificacion")
        try:
            calificacion_vieja = Calificacion.objects.get(usuario_id= usuario_actual.id, asignatura_id = request.POST.get("codigo"))
            calificacion_vieja.calificacion = calificacion_usuario
            calificacion_vieja.save()
        except Calificacion.DoesNotExist as e:
            Calificacion.objects.create(asignatura = asignatura_obj, calificacion= calificacion_usuario, usuario = usuario_actual)
            

    asig = Asignatura.objects.all().filter(estado=True)
    
    for asignatura in asig:
        try:
            calificacion_vieja = Calificacion.objects.get(usuario_id= usuario_actual.id, asignatura_id = asignatura.codigo)
            asignatura.calificacion_vieja = calificacion_vieja.calificacion
            
        except Calificacion.DoesNotExist as e:
            asignatura.calificacion_vieja = '-'
            
        
    return render(request, "index.html", {'asignaturas' : asig})


def logoutUser(request):
   logout(request)
   return HttpResponseRedirect('/login/')   

def register(request):
    if request.method == "POST":
        try:
            user = User.objects.create_user(request.POST.get("email"), request.POST.get("email"), request.POST.get("password"),last_login= date.today())
            user.first_name = request.POST.get("name")
            user.save()
            return redirect("login")
        except IntegrityError as e: 
            if 'unique constraint' in e.message:
                return render(request, "register.html")

    return render(request, "register.html")

def recomendador(request):

    usuario_actual = User.objects.get(username = request.user)
    asignaturas = recomendacion(usuario_actual)
    return render(request, "recomendacion.html", {'asignaturas' : asignaturas[0:5]})
