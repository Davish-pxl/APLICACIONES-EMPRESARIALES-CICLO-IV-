"""
Módulo de vistas para la aplicación utileria.
Contiene la gestión CRUD original y la vista transaccional del Ejercicio 3.
"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido, DetallePedido, Categoria, FichaTecnicaProducto
from django.db import transaction
from django.db.models import F
from django.contrib import messages

from django.shortcuts import render
from django.db.models import Sum, F
from .models import Pedido, DetallePedido


class StockInsuficiente(Exception):
    """Señala que no hay unidades disponibles suficientes para el pedido."""


def producto_list(request):
    productos = Producto.objects.select_related('categoria', 'ficha_tecnica').all()
    return render(request, "utileria/producto_list.html", {"productos": productos})

def producto_create(request):
    if request.method == "POST":
        Producto.objects.create(
            codigo=request.POST.get("codigo"),
            nombre=request.POST.get("nombre"),
            precio=request.POST.get("precio"),
            stock=request.POST.get("stock")
        )
        return redirect("utileria:producto_list")
    return render(request, "utileria/producto_form.html")

def producto_update(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.codigo = request.POST.get("codigo")
        producto.nombre = request.POST.get("nombre")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")
        categoria_id = request.POST.get("categoria")
        if categoria_id:
            producto.categoria_id = categoria_id
            
        producto.save()

        especificaciones = request.POST.get("especificaciones")
        peso_gramos = request.POST.get("peso_gramos")
        if especificaciones and peso_gramos:
            FichaTecnicaProducto.objects.update_or_create(
                producto=producto,
                defaults={
                    "especificaciones": especificaciones,
                    "peso_gramos": peso_gramos
                }
            )

        return redirect("utileria:producto_list")

    categorias = Categoria.objects.all()
    return render(request, "utileria/producto_form.html", {
        "producto": producto,
        "categorias": categorias
    })

def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
        return redirect("utileria:producto_list")
    return render(request, "utileria/producto_confirm_delete.html", {"producto": producto})

def pedido_list(request):
    # Ejercicio 13: pendientes() y del_mes() conservan los filtros del listado.
    # select_related carga Cliente y Proveedor con JOIN en la consulta principal.
    # prefetch_related carga DetallePedido y Producto en consultas separadas,
    # evitando consultas N+1 durante el recorrido de la plantilla.
    pedidos = Pedido.objects.pendientes().del_mes().select_related(
        'cliente', 'proveedor'
    ).prefetch_related('detallepedido_set__producto')
    return render(request, 'utileria/pedido_list.html', {'pedidos': pedidos})

def detalle_create(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == "POST":
        producto_id = request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio_unitario = request.POST.get("precio_unitario")
        
        producto = get_object_or_404(Producto, id=producto_id)
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )
        return redirect("utileria:pedido_list")
    
    productos = Producto.objects.all()
    return render(request, "utileria/detalle_form.html", {"pedido": pedido, "productos": productos})

def detalle_delete(request, id):
    detalle = get_object_or_404(DetallePedido, id=id)
    if request.method == "POST":
        detalle.delete()
        return redirect("utileria:pedido_list")
    return render(request, "utileria/detalle_confirm_delete.html", {"detalle": detalle})

def reporte_view(request):
    # Reporte 1: calcula el monto total de ventas a partir de los detalles registrados.
    total_global = DetallePedido.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    # MODIFICADO: reutilizar el método del manager personalizado para agrupar por estado.
    pedidos_por_estado = Pedido.objects.conteo_por_estado()
    total_pedidos = Pedido.objects.count()

    context = {
        'total_global': total_global,
        'pedidos_por_estado': pedidos_por_estado,
        'total_pedidos': total_pedidos,
    }
    return render(request, 'utileria/reporte.html', context)


# ==========================================
# EJERCICIO 3: VISTA TRANSACCIONAL
# ==========================================

def registrar_pedido_transaccion(request):
    """
    Operación transaccional con transaction.atomic() y F():
    - Modifica múltiples modelos: Producto (descuenta stock), Pedido (crea orden) y DetallePedido.
    - Si no hay stock suficiente, lanza una excepción y cancela todo por completo (rollback).
    - Aplica el patrón Post/Redirect/Get (PRG) al finalizar.
    """
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        try:
            cantidad = int(request.POST.get('cantidad', ''))
        except (TypeError, ValueError):
            # MODIFICADO: informar cantidades vacías o no enteras sin dejar fallar la vista.
            messages.error(request, 'Ingrese una cantidad entera válida.')
            return redirect('utileria:registrar_pedido_transaccion')

        if cantidad < 1:
            # MODIFICADO: impedir cantidades cero o negativas antes de iniciar la transacción.
            messages.error(request, 'La cantidad debe ser mayor que cero.')
            return redirect('utileria:registrar_pedido_transaccion')

        try:
            # MODIFICADO: agrupar descuento de stock y creación del pedido/detalle.
            with transaction.atomic():
                # MODIFICADO: bloquear el producto y descontar con F() solo si alcanza el stock.
                producto = Producto.objects.select_for_update().get(pk=producto_id)
                stock_actualizado = Producto.objects.filter(
                    pk=producto.pk,
                    stock__gte=cantidad
                ).update(stock=F('stock') - cantidad)

                if not stock_actualizado:
                    # MODIFICADO: la excepción sale de atomic() y revierte cualquier cambio del bloque.
                    raise StockInsuficiente(
                        f'Stock insuficiente. Disponible: {producto.stock}, '
                        f'Solicitado: {cantidad}.'
                    )

                # MODIFICADO: crear registros solo después de confirmar el descuento.
                nuevo_pedido = Pedido.objects.create(estado='Completado')
                DetallePedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

        except StockInsuficiente as error:
            # MODIFICADO: informar el rechazo después del rollback automático de atomic().
            messages.error(request, str(error))
            return redirect('utileria:registrar_pedido_transaccion')
        except (Producto.DoesNotExist, ValueError):
            # MODIFICADO: reportar un ID de producto que no existe o no es válido.
            messages.error(request, 'El producto seleccionado no existe o no es válido.')
            return redirect('utileria:registrar_pedido_transaccion')

        # MODIFICADO: confirmar éxito solo cuando toda la transacción terminó correctamente.
        messages.success(request, f'¡Pedido #{nuevo_pedido.id} registrado con éxito!')
        # Se conserva el patrón Post/Redirect/Get para evitar reenvíos del formulario.
        return redirect('utileria:registrar_pedido_transaccion')

    return render(request, 'utileria/registrar_pedido.html', {'productos': productos})