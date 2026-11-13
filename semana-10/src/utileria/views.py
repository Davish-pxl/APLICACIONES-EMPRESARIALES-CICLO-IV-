from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Sum, Count, F
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido, Categoria, FichaTecnicaProducto, Cliente


# Excepción personalizada para señalar cuando el stock no es suficiente
class StockInsuficiente(Exception):
    """Señala que no hay unidades disponibles suficientes para el pedido."""
    pass

# VISTAS CRUD PRINCIPALES (PRODUCTOS)

def producto_list(request):
    # Optimización N+1 usando select_related para traer Categoria y FichaTecnica en una sola consulta
    productos = Producto.objects.select_related('categoria', 'ficha_tecnica').all()
    return render(request, "utileria/producto_list.html", {"productos": productos})


def producto_create(request):
    if request.method == "POST":
        categoria_id = request.POST.get("categoria")
        
        # Creación del producto vinculando la categoría seleccionada
        producto = Producto.objects.create(
            codigo=request.POST.get("codigo"),
            nombre=request.POST.get("nombre"),
            precio=request.POST.get("precio"),
            stock=request.POST.get("stock"),
            categoria_id=categoria_id if categoria_id else None
        )

        # Procesar Ficha Técnica opcional si se enviaron especificaciones o peso
        especificaciones = request.POST.get("especificaciones")
        peso_gramos = request.POST.get("peso_gramos")
        if especificaciones or peso_gramos:
            FichaTecnicaProducto.objects.create(
                producto=producto,
                especificaciones=especificaciones or "",
                peso_gramos=peso_gramos or 0.0
            )

        return redirect("utileria:producto_list")

    # Se consultan y envían todas las categorías a la plantilla para popular el desplegable <select>
    categorias = Categoria.objects.all()
    return render(request, "utileria/producto_form.html", {"categorias": categorias})


def producto_update(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.codigo = request.POST.get("codigo")
        producto.nombre = request.POST.get("nombre")
        producto.precio = request.POST.get("precio")
        producto.stock = request.POST.get("stock")
        
        categoria_id = request.POST.get("categoria")
        producto.categoria_id = categoria_id if categoria_id else None
        producto.save()

        # Actualización o creación de la Ficha Técnica asociada
        especificaciones = request.POST.get("especificaciones")
        peso_gramos = request.POST.get("peso_gramos")
        if especificaciones or peso_gramos:
            FichaTecnicaProducto.objects.update_or_create(
                producto=producto,
                defaults={
                    "especificaciones": especificaciones or "",
                    "peso_gramos": peso_gramos or 0.0
                }
            )

        return redirect("utileria:producto_list")

    # Se consultan y envían las categorías junto con el objeto del producto a editar
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

# VISTAS DE PEDIDOS Y DETALLES

def pedido_list(request):
    # Reutilización encadenada del QuerySet personalizado y optimización prefetch/select_related
    pedidos = (
        Pedido.objects.pendientes()
        .del_mes()
        .select_related('cliente', 'proveedor')
        .prefetch_related('detallepedido_set__producto')
    )
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

# VISTA DE REPORTE CON AGGREGATE Y ANNOTATE 

def reporte_view(request):
    # Uso del método personalizado .del_mes() para obtener los pedidos del mes
    pedidos_mes_count = Pedido.objects.del_mes().count()
    # Uso del método personalizado .pendientes() para obtener las órdenes pendientes
    pedidos_pendientes_count = Pedido.objects.pendientes().count()

    # aggregate(): Calcula el total global multiplicando cantidad * precio_unitario en BD
    total_global_dict = DetallePedido.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )
    total_global = total_global_dict['total'] or 0

    # annotate(): Unidades vendidas por producto
    por_producto = Producto.objects.annotate(
        unidades=Sum('detallepedido__cantidad')
    ).order_by('-unidades')

    # values() + annotate(): Agrupamiento de pedidos por estado
    por_estado = (
        Pedido.objects.values('estado')
        .annotate(cantidad=Count('id'))
        .order_by('-cantidad')
    )

    context = {
        'total_global': total_global,
        'por_producto': por_producto,
        'por_estado': por_estado,
        'pedidos_mes_count': pedidos_mes_count,
        'pedidos_pendientes_count': pedidos_pendientes_count,
    }
    return render(request, 'utileria/reporte.html', context)

# VISTA TRANSACCIONAL CON transaction.atomic() Y F() 

def registrar_pedido_transaccion(request):
    """
    Operación transaccional:
    - Usa transaction.atomic() para asegurar atomicidad ("todo o nada").
    - Descuenta stock con F() directamente en la BD evitando race conditions.
    - Si el stock es insuficiente, se genera un raise para provocar el ROLLBACK atómico.
    """
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        try:
            cantidad = int(request.POST.get('cantidad', ''))
        except (TypeError, ValueError):
            messages.error(request, 'Ingrese una cantidad entera válida.')
            return redirect('utileria:registrar_pedido_transaccion')

        if cantidad < 1:
            messages.error(request, 'La cantidad debe ser mayor que cero.')
            return redirect('utileria:registrar_pedido_transaccion')

        try:
            # try/except fuera del bloque atomic() para captura limpia de errores
            with transaction.atomic():
                producto = Producto.objects.select_for_update().get(pk=producto_id)
                stock_actualizado = Producto.objects.filter(
                    pk=producto.pk,
                    stock__gte=cantidad
                ).update(stock=F('stock') - cantidad)

                if not stock_actualizado:
                    raise StockInsuficiente(
                        f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}, Solicitado: {cantidad}.'
                    )

                nuevo_pedido = Pedido.objects.create(estado='Completado')
                DetallePedido.objects.create(
                    pedido=nuevo_pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio
                )

        except StockInsuficiente as error:
            messages.error(request, str(error))
            return redirect('utileria:registrar_pedido_transaccion')
        except (Producto.DoesNotExist, ValueError):
            messages.error(request, 'El producto seleccionado no existe o no es válido.')
            return redirect('utileria:registrar_pedido_transaccion')

        messages.success(request, f'¡Pedido #{nuevo_pedido.id} registrado con éxito!')
        return redirect('utileria:registrar_pedido_transaccion')

    return render(request, 'utileria/registrar_pedido.html', {'productos': productos})