from django.db import models
from django.utils import timezone

# QuerySet personalizado con métodos encadenables 
class ReservaQuerySet(models.QuerySet):
    """
    QuerySet personalizado para encapsular reglas de negocio de la investigación.
    """
    def activas(self):
        #Filtrar reservas activas
        return self.filter(estado__iexact='ACTIVA')

    def confirmadas(self):
        #Filtrar reservas completadas / confirmadas
        return self.filter(estado__iexact='COMPLETADA')


class Reserva(models.Model):
    cancha = models.CharField(max_length=100)
    deporte = models.CharField(max_length=50)
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=5)
    duracion_horas = models.FloatField(default=1.0)
    precio_hora = models.FloatField(default=20.0)
    cliente = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='ACTIVA')  
    cupos_disponibles = models.IntegerField(default=10)  

    # Asignación del QuerySet personalizado mediante as_manager()
    objects = ReservaQuerySet.as_manager()

    def __str__(self):
        return f"Reserva #{self.id} - {self.cancha}"