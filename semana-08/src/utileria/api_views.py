from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Producto, Pedido, Categoria
from .serializers import (
    ProductoSerializer,
    PedidoSerializer,
    PedidoRelacionadoSerializer,
    CategoriaSerializer
)

# 1. VISTAS GENÉRICAS 
# Vista genérica para listar todos los productos (GET) y crear uno nuevo (POST)
class ProductoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Vista genérica para consultar (GET), actualizar (PUT/PATCH) y eliminar (DELETE) un producto por su ID
class ProductoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# 2. VIEWSET RECURSO SIMPLE (Producto) CON BÚSQUEDA Y ORDENAMIENTO

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    # Habilitar filtros de búsqueda y ordenamiento
    filter_backends = [SearchFilter, OrderingFilter]

    # Campos sobre los que se puede realizar la búsqueda
    search_fields = ['nombre', 'codigo']

    # Campos permitidos para ordenar los resultados
    ordering_fields = ['precio', 'stock', 'nombre']

# 3. VIEWSET RECURSO RELACIONADO (Pedido) CON FILTRO Y ACCIÓN PROPIA

class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        # Optimización N+1 con select_related y prefetch_related
        qs = (
            Pedido.objects
            .select_related('cliente', 'proveedor')
            .prefetch_related('detallepedido_set__producto')
        )

        # Filtro por parámetro URL: ?estado=PAGADO (o ?estado=pendiente)
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado.upper())

        return qs

    # Acción personalizada: GET /api/pedidos/pagados/
    @action(detail=False, methods=['get'])
    def pagados(self, request):
        qs_pagados = self.get_queryset().pagados()
        serializer = self.get_serializer(qs_pagados, many=True)
        return Response(serializer.data)

# 4. RECURSO DE SOLO LECTURA CON RELACIONES ANIDADAS Y OPTIMIZACIÓN

class PedidoReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoRelacionadoSerializer

    def get_queryset(self):
        return (
            Pedido.objects
            .select_related('cliente', 'proveedor')
            .prefetch_related('detallepedido_set__producto')
        )

# 5. VIEWSET INVESTIGACIÓN PROPIA CON FILTROS Y @ACTION 

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer

    # 1. Habilitar filtros de Búsqueda y Ordenamiento
    filter_backends = [SearchFilter, OrderingFilter]

    # Campos sobre los que se aplica la búsqueda (?search=)
    search_fields = ['nombre', 'descripcion']

    # Campos permitidos para ordenar los resultados (?ordering=)
    ordering_fields = ['nombre', 'id']

    # 2. Filtro dinámico por parámetro URL (?nombre=) en get_queryset()
    def get_queryset(self):
        qs = Categoria.objects.all()
        nombre_param = self.request.query_params.get('nombre')
        if nombre_param:
            qs = qs.filter(nombre__icontains=nombre_param)
        return qs

    # 3. Acción propia que filtra categorías con productos asociados
    # Ruta automática: GET /api/categorias/con-productos/
    @action(detail=False, methods=['get'])
    def con_productos(self, request):
        qs_con_prod = self.get_queryset().filter(productos__isnull=False).distinct()
        serializer = self.get_serializer(qs_con_prod, many=True)
        return Response(serializer.data)