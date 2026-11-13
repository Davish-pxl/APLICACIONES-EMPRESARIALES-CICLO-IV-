from rest_framework import serializers
from .models import Producto, Categoria, Pedido, DetallePedido, Proveedor, Cliente

# 1. SERIALIZERS - RECURSOS DE INVESTIGACIÓN PROPIA

# Recurso 1: CategoriaSerializer con validación propia
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

    # Regla de negocio: El nombre de la categoría debe tener al menos 3 caracteres
    def validate_nombre(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El nombre de la categoría debe tener al menos 3 caracteres.")
        return value

# Recurso 2: ProveedorSerializer
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'razon_social', 'ruc']

# Recurso 3: ClienteSerializer
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono']

# 2. SERIALIZERS - RECURSO SIMPLE

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'precio', 'stock', 'categoria']

    # Regla de negocio: El precio debe ser estrictamente mayor que 0
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value

# 3. SERIALIZERS - RECURSO CON RELACIONES

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField()

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    proveedor = serializers.StringRelatedField()
    # Relación anidada de solo lectura para los detalles del pedido
    detalles = DetallePedidoSerializer(source='detallepedido_set', many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'proveedor', 'fecha', 'estado', 'detalles']

# 4. SERIALIZERS - RECURSO DE SOLO LECTURA CON RELACIONES ANIDADAS

class DetallePedidoReadSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto_nombre', 'cantidad', 'precio_unitario']

class PedidoRelacionadoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre')
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.razon_social')
    # Relación anidada de solo lectura para listar todos los items del detalle
    detalles = DetallePedidoReadSerializer(source='detallepedido_set', many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente_nombre', 'proveedor_nombre', 'fecha', 'estado', 'detalles']