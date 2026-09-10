from django.urls import path
from . import views

app_name = "utileria"

urlpatterns = [
    path("", views.producto_list, name="producto_list"),
    path("nuevo/", views.producto_create, name="producto_create"),
    path("editar/<int:id>/", views.producto_update, name="producto_update"),
    path("eliminar/<int:id>/", views.producto_delete, name="producto_delete"),
]