from django.urls import path
from . import views

app_name = "utileria"

urlpatterns = [
    path("", views.producto_list, name="producto_list"),
    path("nuevo/", views.producto_create, name="producto_create"),
    path("editar/<int:id>/", views.producto_update, name="producto_update"),
    path("eliminar/<int:id>/", views.producto_delete, name="producto_delete"),
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("pedidos/<int:pedido_id>/detalle/nuevo/", views.detalle_create, name="detalle_create"),
    path("detalle/eliminar/<int:id>/", views.detalle_delete, name="detalle_delete"),
]