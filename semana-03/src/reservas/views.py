from django.shortcuts import render, redirect
from .models import Reserva

def lista_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, "reservas/lista.html", {"reservas": reservas})

def crear_reserva(request):
    if request.method == "POST":
        cancha = request.POST.get("cancha")
        deporte = request.POST.get("deporte")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        duracion_horas = float(request.POST.get("duracion_horas") or 1.0)
        precio_hora = float(request.POST.get("precio_hora") or 20.0)
        cliente = request.POST.get("cliente")

        Reserva.objects.create(
            cancha=cancha,
            deporte=deporte,
            fecha=fecha,
            hora=hora,
            duracion_horas=duracion_horas,
            precio_hora=precio_hora,
            cliente=cliente,
            estado="ACTIVA"
        )
        return redirect("reservas:lista")

    return render(request, "reservas/crear.html")