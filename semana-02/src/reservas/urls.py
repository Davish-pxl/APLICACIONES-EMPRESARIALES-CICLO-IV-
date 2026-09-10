from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.lista_reservas, name='lista'),
    path('crear/', views.crear_reserva, name='crear'),
    path('detalle/<int:reserva_id>/', views.detalle_reserva, name='detalle'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar'),
    path('consulta/', views.enviar_consulta, name='consulta'),
]