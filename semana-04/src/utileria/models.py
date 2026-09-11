from django.db import models

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)

    def __str__(self):
        return self.razon_social

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

class FichaTecnicaProducto(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='ficha_tecnica'
    )
    especificaciones = models.TextField()
    dimensiones = models.CharField(max_length=100)
    peso_gramos = models.DecimalField(max_digits=6, decimal_places=2)
    es_toxico = models.BooleanField(default=False)

    def __str__(self):
        return "Ficha de " + self.producto.nombre

class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.producto.nombre}"