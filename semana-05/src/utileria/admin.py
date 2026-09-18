from django.contrib import admin
from .models import (
    Proveedor, Categoria, Cliente, PerfilCliente, Producto,
    FichaTecnicaProducto, UbicacionAlmacen, Pedido, DetallePedido, ComprobantePago
)


class FichaTecnicaInline(admin.StackedInline):
    model = FichaTecnicaProducto
    extra = 1

class UbicacionAlmacenInline(admin.StackedInline):
    model = UbicacionAlmacen
    extra = 1

class PerfilClienteInline(admin.StackedInline):
    model = PerfilCliente
    extra = 1

class ComprobantePagoInline(admin.StackedInline):
    model = ComprobantePago
    extra = 1

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'precio', 'stock', 'categoria')
    search_fields = ('codigo', 'nombre')
    list_filter = ('categoria',)
    inlines = [FichaTecnicaInline, UbicacionAlmacenInline]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono') 
    search_fields = ('nombre', 'telefono')
    inlines = [PerfilClienteInline]

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'proveedor', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    inlines = [DetallePedidoInline, ComprobantePagoInline]

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('ruc', 'razon_social')
    search_fields = ('ruc', 'razon_social')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

admin.site.register(FichaTecnicaProducto)
admin.site.register(UbicacionAlmacen)
admin.site.register(PerfilCliente)
admin.site.register(DetallePedido)
admin.site.register(ComprobantePago)