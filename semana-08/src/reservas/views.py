from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, connection, reset_queries
from django.db.models import Sum, Count, F
from django.contrib import messages
from .models import Reserva

# CREAR RESERVA TRANSACCIONAL CON transaction.atomic() Y F()

def crear_reserva(request):
    if request.method == "POST":
        cancha = request.POST.get("cancha")
        deporte = request.POST.get("deporte")
        fecha = request.POST.get("fecha")
        hora = request.POST.get("hora")
        duracion_horas = float(request.POST.get("duracion_horas") or 1.0)
        precio_hora = float(request.POST.get("precio_hora") or 20.0)
        cliente = request.POST.get("cliente")
        cupos_solicitados = int(request.POST.get("cupos", 1))

        try:
            # Bloque atómico: o se ejecutan todas las operaciones o ninguna
            with transaction.atomic():
                # Crear la reserva
                reserva = Reserva.objects.create(
                    cancha=cancha,
                    deporte=deporte,
                    fecha=fecha,
                    hora=hora,
                    duracion_horas=duracion_horas,
                    precio_hora=precio_hora,
                    cliente=cliente,
                    estado="ACTIVA"
                )

                # Descontar el campo entero en la BD usando F()
                actualizados = Reserva.objects.filter(
                    pk=reserva.pk,
                    cupos_disponibles__gte=cupos_solicitados
                ).update(cupos_disponibles=F("cupos_disponibles") - cupos_solicitados)

                # Si no había cupos suficientes, se lanza error para provocar ROLLBACK
                if actualizados == 0:
                    raise ValueError(f"Cupos insuficientes para la cancha {cancha}.")

            messages.success(request, f"¡Reserva #{reserva.id} creada con éxito!")
            return redirect("reservas:lista")

        except ValueError as e:
            # Captura de error fuera de atomic() para informar y ejecutar Rollback limpio
            messages.error(request, str(e))
            return redirect("reservas:crear")

    return render(request, "reservas/crear.html")

# LISTA DE RESERVAS USANDO EL QUERYSET PERSONALIZADO

def lista_reservas(request):
    # Uso de métodos encadenables del QuerySet personalizado (.activas()) 
    reservas = Reserva.objects.activas()
    return render(request, "reservas/lista.html", {"reservas": reservas})

# REPORTES CON AGGREGATE Y ANNOTATE
def reporte_reservas(request):
    # aggregate(): Total recaudado general mediante expresiones F()
    total_recaudado = Reserva.objects.aggregate(
        total=Sum(F('duracion_horas') * F('precio_hora'))
    )['total'] or 0.0

    # annotate(): Cantidad de reservas acumuladas por deporte 
    por_deporte = Reserva.objects.values('deporte').annotate(
        total_reservas=Count('id')
    ).order_by('-total_reservas')

    # values() + annotate(): Reservas agrupadas por estado
    por_estado = Reserva.objects.values('estado').annotate(
        cantidad=Count('id')
    )

    context = {
        'total_recaudado': total_recaudado,
        'por_deporte': por_deporte,
        'por_estado': por_estado,
    }
    return render(request, 'reservas/reporte.html', context)