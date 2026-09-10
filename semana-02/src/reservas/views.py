from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RESERVAS_DB, CONSULTAS_DB
from .forms import ReservaForm, ConsultaForm

def lista_reservas(request):
    reservas = [dict(r) for r in RESERVAS_DB]

    for r in reservas:
        r['costo_total'] = float(r['duracion_horas']) * float(r['precio_hora'])

    deporte_filtro = request.GET.get('deporte')
    precio_max = request.GET.get('precio_max')

    if deporte_filtro:
        reservas = [r for r in reservas if r['deporte'] == deporte_filtro]
    if precio_max:
        try:
            reservas = [r for r in reservas if r['precio_hora'] <= float(precio_max)]
        except ValueError:
            pass

    reporte_canchas = {}
    for r in RESERVAS_DB:
        cancha = r['cancha']
        reporte_canchas[cancha] = reporte_canchas.get(cancha, 0) + 1

    context = {
        'reservas': reservas,
        'reporte_canchas': reporte_canchas,
        'deporte_filtro': deporte_filtro or '',
        'precio_max': precio_max or ''
    }
    return render(request, 'reservas/lista.html', context)

def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            cruce = any(
                r['cancha'].lower() == data['cancha'].lower() and
                r['fecha'] == data['fecha'] and
                r['hora'] == data['hora'] and
                r['estado'] == 'ACTIVA'
                for r in RESERVAS_DB
            )

            if cruce:
                form.add_error(None, f"La cancha '{data['cancha']}' ya se encuentra reservada en el horario {data['fecha']} {data['hora']}.")
            else:
                nuevo_id = max([r['id'] for r in RESERVAS_DB], default=0) + 1
                nueva = {
                    'id': nuevo_id,
                    'cancha': data['cancha'],
                    'deporte': data['deporte'],
                    'fecha': data['fecha'],
                    'hora': data['hora'],
                    'duracion_horas': data['duracion_horas'],
                    'precio_hora': data['precio_hora'],
                    'cliente': data['cliente'],
                    'estado': 'ACTIVA'
                }
                RESERVAS_DB.append(nueva)
                return redirect('reservas:lista')
    else:
        form = ReservaForm()

    return render(request, 'reservas/crear.html', {'form': form})

def detalle_reserva(request, reserva_id):
    reserva = next((dict(r) for r in RESERVAS_DB if r['id'] == reserva_id), None)
    if reserva:
        reserva['costo_total'] = float(reserva['duracion_horas']) * float(reserva['precio_hora'])
    return render(request, 'reservas/detalle.html', {'reserva': reserva})

def cancelar_reserva(request, reserva_id):
    for r in RESERVAS_DB:
        if r['id'] == reserva_id:
            r['estado'] = 'CANCELADA'
            break
    return redirect('reservas:lista')

def enviar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            CONSULTAS_DB.append(form.cleaned_data)
            messages.success(request, "¡Consulta enviada correctamente!")
            return redirect('reservas:consulta')
    else:
        form = ConsultaForm()
    return render(request, 'reservas/consulta.html', {'form': form})