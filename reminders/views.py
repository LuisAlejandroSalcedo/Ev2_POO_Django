import datetime
from pyexpat.errors import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Reminder

def index(request):
    if request.method == "POST":
        if request.POST.get("contenido") == "" or request.POST.get("contenido").isspace():
            context = {"reminders": Reminder.objects.order_by("-important"), "messages":"El contenido no puede estar vacío"}
            return render(request, "reminders/index.html", context, status=400)

        if len(request.POST.get("contenido")) < 3 or len(request.POST.get("contenido")) > 120: 
            context = {"reminders": Reminder.objects.order_by("-important"), "messages":"El contenido debe tener entre 3 y 120 caracteres"}
            return render(request, "reminders/index.html", context, status=400)

        content = request.POST.get("contenido")
        important = request.POST.get("importante") == "on"
        reminder = Reminder(content=content, important=important, createdAt=timezone.now().timestamp())
        reminder.save()
    context = {"reminders": Reminder.objects.order_by("-important"), "messages": "Reminder creado con éxito"}
    return render(request, "reminders/index.html", context, status=201)

def editar(request, id):
    reminder = Reminder.objects.get(id=id)
    if request.method == "POST":
        if request.POST.get("contenido") == "" or request.POST.get("contenido").isspace():
            context = {"reminders": Reminder.objects.order_by("-important"), "id": reminder.id, "messages":"El contenido no puede estar vacío"}
            return render(request, "reminders/Editar.html", context, status=400)

        if len(request.POST.get("contenido")) < 3 or len(request.POST.get("contenido")) > 120: 
            context = {"reminders": Reminder.objects.order_by("-important"), "id": reminder.id, "messages":"El contenido debe tener entre 3 y 120 caracteres"}
            return render(request, "reminders/Editar.html", context, status=400)

        reminder.content = request.POST.get("contenido")
        reminder.important = request.POST.get("importante") == "on"
        reminder.save()
        return redirect("index")
    context = {"reminder": reminder, "messages": "Recordatorio editado con éxito"}
    return render(request, "reminders/Editar.html", context, status=200)

def eliminar(request, id):
    reminder = Reminder.objects.get(id=id)
    reminder.delete()
    return redirect("index")