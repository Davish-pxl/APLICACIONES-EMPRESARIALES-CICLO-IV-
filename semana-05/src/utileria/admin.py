from django.contrib import admin
from .models import (
    Proveedor, Categoria, Cliente, PerfilCliente, Producto,
    FichaTecnicaProducto, UbicacionAlmacen, Pedido, DetallePedido, ComprobantePago
)
# Registro de modelos en el Django Admin    
admin.site.register(Categoria)
admin.site.register(PerfilCliente)
admin.site.register(UbicacionAlmacen)
admin.site.register(ComprobantePago)

# Inline apilado para la relación 1:1 con FichaTecnicaProducto
class FichaTecnicaInline(admin.StackedInline):
    model = FichaTecnicaProducto
    extra = 1

# Registro del producto con su ficha técnica integrada
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

# Inline tabular para gestionar los productos de un pedido (modelo intermedio N:M).
# Muestra los atributos propios de DetallePedido (cantidad, precio) como columnas de una tabla.
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'proveedor', 'fecha', 'estado')
    search_fields = ('cliente__nombre', 'estado')
    list_filter = ('estado', 'fecha')
    # Se añade el inline para editar la relacion N:M directamente desde el pedido
    inlines = [DetallePedidoInline]


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'ruc')
    search_fields = ('razon_social', 'ruc')