from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# CONFIGURACIÓN DEL ROUTER
# Instanciamos el DefaultRouter y registramos los ViewSets de la aplicación
router = DefaultRouter()
router.register('productos', api_views.ProductoViewSet, basename='producto')
router.register('pedidos', api_views.PedidoViewSet, basename='pedido')
router.register('pedidos-relacionados', api_views.PedidoReadOnlyViewSet, basename='pedido-relacionado')

# Registrar el recurso de la investigación propia
router.register('categorias', api_views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    # RUTAS DE VISTAS GENÉRICAS 
    # Ruta para listar y crear productos
    path('generic/productos/', api_views.ProductoListCreateAPIView.as_view(), name='producto-list-create'),
    
    # Ruta para obtener, actualizar o eliminar un producto específico
    path('generic/productos/<int:pk>/', api_views.ProductoRetrieveUpdateDestroyAPIView.as_view(), name='producto-detail-generic'),
  
    path('', include(router.urls)),
]