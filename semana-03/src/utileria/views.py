from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto

def producto_list(request):
    productos = Producto.objects.all()
    return render(request, "utileria/producto_list.html", {"productos": productos})

def producto_create(request):
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        nombre = request.POST.get("nombre")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")

        Producto.objects.create(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            stock=stock
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

        producto.save()
        return redirect("utileria:producto_list")

    return render(request, "utileria/producto_form.html", {"producto": producto})

def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.delete()
        return redirect("utileria:producto_list")

    return render(request, "utileria/producto_confirm_delete.html", {"producto": producto})