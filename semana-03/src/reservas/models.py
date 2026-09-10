from django.db import models

class Reserva(models.Model):
    cancha = models.CharField(max_length=100)
    deporte = models.CharField(max_length=50)
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=5)
    duracion_horas = models.FloatField(default=1.0)
    precio_hora = models.FloatField(default=20.0)
    cliente = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='ACTIVA')

    def __str__(self):
        return f"Reserva #{self.id} - {self.cancha}"