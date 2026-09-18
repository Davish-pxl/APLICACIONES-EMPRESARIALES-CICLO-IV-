from django.db import models

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)

    def __str__(self):
        return self.razon_social


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre

class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    direccion = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.cliente.nombre}"

class Producto(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        null=True,
        blank=True
    )

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
        return f"Ficha de {self.producto.nombre}"

class UbicacionAlmacen(models.Model):
    producto = models.OneToOneField(
        Producto,
        on_delete=models.CASCADE,
        related_name='ubicacion'
    )
    pasillo = models.CharField(max_length=50)
    estante = models.CharField(max_length=50)

    def __str__(self):
        return f"Ubicación de {self.producto.nombre}: Pasillo {self.pasillo}"

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='pedidos',
        null=True,
        blank=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        related_name='pedidos',
        null=True,
        blank=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    productos = models.ManyToManyField(
        Producto,
        through='DetallePedido',
        related_name='pedidos'
    )

    def __str__(self):
        return f"Pedido #{self.id} - Estado: {self.estado}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Pedido #{self.pedido.id}"

class ComprobantePago(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='comprobante'
    )
    tipo_comprobante = models.CharField(max_length=50, default='Boleta') 
    serie_numero = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_comprobante} {self.serie_numero} - Pedido #{self.pedido.id}"