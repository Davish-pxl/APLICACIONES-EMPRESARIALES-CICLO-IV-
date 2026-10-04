from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Pedido, DetallePedido, Categoria, FichaTecnicaProducto

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
    pedidos = Pedido.objects.prefetch_related('detallepedido_set__producto').all()
    return render(request, "utileria/pedido_list.html", {"pedidos": pedidos})

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