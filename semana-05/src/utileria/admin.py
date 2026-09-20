from django.contrib import admin
from .models import (
    Proveedor, Categoria, Cliente, PerfilCliente, Producto,
    FichaTecnicaProducto, UbicacionAlmacen, Pedido, DetallePedido, ComprobantePago
)

admin.site.register(Categoria)
admin.site.register(PerfilCliente)
admin.site.register(UbicacionAlmacen)
admin.site.register(DetallePedido)
admin.site.register(ComprobantePago)


class FichaTecnicaInline(admin.StackedInline):
    model = FichaTecnicaProducto
    extra = 0


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'stock', 'categoria')
    search_fields = ('nombre', 'codigo')
    list_filter = ('categoria',)
    inlines = [FichaTecnicaInline]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono')
    search_fields = ('nombre',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'proveedor', 'fecha', 'estado')
    search_fields = ('cliente__nombre', 'estado')
    list_filter = ('estado', 'fecha')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'ruc')
    search_fields = ('razon_social', 'ruc')