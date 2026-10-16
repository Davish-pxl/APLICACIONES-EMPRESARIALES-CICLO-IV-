from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

# MODELOS DE ENTIDADES SECUNDARIAS / RELACIONADAS

# Entidad Proveedor: Relación ForeignKey (1:N) opcional con Pedido.
class Proveedor(models.Model):
    razon_social = models.CharField(max_length=100)
    ruc = models.CharField(max_length=11)

    def __str__(self):
        return self.razon_social


# Entidad Categoria: Relación ForeignKey (1:N) con Producto.
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# Entidad Cliente: Relación ForeignKey (1:N) con Pedido.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


# Relación OneToOneField (1:1) con Cliente.
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

# ENTIDAD PRINCIPAL Y SUS RELACIONES DIRECTAS

# Modelo Producto: Entidad principal.
class Producto(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()  # Campo entero que se descuenta con F()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"


# Relación OneToOneField (1:1) con Producto.
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


# Segunda relación OneToOneField (1:1) con Producto.
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

# QUERYSET PERSONALIZADO Y MODELO PEDIDO

class PedidoQuerySet(models.QuerySet):
    # Método para filtrar pedidos pagados 
    def pagados(self):
        return self.filter(estado__iexact='PAGADO')

    # Método para filtrar pedidos pendientes
    def pendientes(self):
        return self.filter(estado__iexact='PENDIENTE')

    # Método para filtrar pedidos del mes actual
    def del_mes(self):
        hoy = timezone.now()
        return self.filter(fecha__year=hoy.year, fecha__month=hoy.month)

    # Conteo agrupado por estado normalizado
    def conteo_por_estado(self):
        return self.annotate(
            estado_normalizado=Lower('estado')
        ).values('estado_normalizado').annotate(
            total=models.Count('id')
        ).order_by('estado_normalizado')


# Modelo Pedido
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

    # Asignación del QuerySet personalizado mediante as_manager()
    objects = PedidoQuerySet.as_manager()

    def __str__(self):
        return f"Pedido #{self.id} - Estado: {self.estado}"

# MODELO INTERMEDIO (N:M) Y COMPROBANTE

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} en Pedido #{self.pedido.id}"


# Relación OneToOneField (1:1) con Pedido.
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