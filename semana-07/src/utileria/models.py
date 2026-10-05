from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone


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


class Producto(models.Model):  # ENTIDAD PRINCIPAL
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


# 1. QuerySet personalizado para Pedido
class PedidoQuerySet(models.QuerySet):
    def pendientes(self):
        return self.filter(estado__iexact='Pendiente')

    def del_mes(self):
        hoy = timezone.now()
        return self.filter(fecha__year=hoy.year, fecha__month=hoy.month)

    def conteo_por_estado(self):
        return self.annotate(
            estado_normalizado=Lower('estado')
        ).values('estado_normalizado').annotate(
            total=models.Count('id')
        ).order_by('estado_normalizado')


PedidoManager = models.Manager.from_queryset(PedidoQuerySet)


# 2. Modelo Pedido completo (con Manager y todos sus campos)
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

    # MODIFICADO: Manager.from_queryset expone los métodos del QuerySet en Pedido.objects.
    objects = PedidoManager()

    def __str__(self):
        return f"Pedido #{self.id} - Estado: {self.estado}"


class DetallePedido(models.Model):  # MODELO INTERMEDIO
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