# Sistema de Gestión de Utilería Escolar - Laboratorio 5

Este proyecto corresponde al desarrollo y configuración del panel de administración (**Django Admin**) para el sistema de utilería escolar, gestionando 10 entidades relacionales mediante personalizaciones avanzadas de `ModelAdmin` e `Inlines`.

---

## 1. Modelos Registrados y Personalización en el Admin

A continuación se detalla la configuración y personalización implementada en `utileria/admin.py` para las entidades del proyecto:

### Entidades Personalizadas con `ModelAdmin`

1. **`Producto` (`ProductoAdmin`)**
   - **`list_display`**: `codigo`, `nombre`, `precio`, `stock`, `categoria`
   - **`search_fields`**: `nombre`, `codigo`
   - **`list_filter`**: `categoria`
   - **`inlines`**: `FichaTecnicaInline` (`StackedInline` para la relación 1:1)

2. **`Pedido` (`PedidoAdmin`)**
   - **`list_display`**: `id`, `cliente`, `proveedor`, `fecha`, `estado`
   - **`search_fields`**: `cliente__nombre`, `estado`
   - **`list_filter`**: `estado`, `fecha`
   - **`inlines`**: `DetallePedidoInline` (`TabularInline` para la relación N:M)

3. **`Cliente` (`ClienteAdmin`)**
   - **`list_display`**: `nombre`, `telefono`
   - **`search_fields`**: `nombre`

4. **`Proveedor` (`ProveedorAdmin`)**
   - **`list_display`**: `razon_social`, `ruc`
   - **`search_fields`**: `razon_social`, `ruc`

### Registros Simples
- **`Categoria`**
- **`PerfilCliente`**
- **`UbicacionAlmacen`**
- **`ComprobantePago`**

---

## 2. Inlines Configurados

* **`FichaTecnicaInline` (`admin.StackedInline`)**:
  - **Relación**: 1:1 (`OneToOneField`) entre `Producto` y `FichaTecnicaProducto`.
  - **Uso**: Despliega un formulario vertical apilado dentro de la vista del Producto para gestionar sus especificaciones técnicas de forma unificada.
  - **Configuración**: `extra = 0` para una interfaz limpia.

* **`DetallePedidoInline` (`admin.TabularInline`)**:
  - **Relación**: N:M con modelo intermedio (`DetallePedido`) entre `Pedido` y `Producto`.
  - **Uso**: Despliega una tabla horizontal interactiva dentro de la vista del Pedido, permitiendo registrar la cantidad y precio unitario de los productos asignados.
  - **Configuración**: `extra = 1`.

---

## 3. Requisitos y Ejecución

Las dependencias exactas del proyecto han sido congeladas en `requirements.txt`.

### Pasos para ejecutar el proyecto:
```bash
# 1. Crear e iniciar entorno virtual (opcional)
python -m venv venv
# En Windows:
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py migrate

# 4. Iniciar servidor local
python manage.py runserver

Resultado:
<img width="1242" height="693" alt="image" src="https://github.com/user-attachments/assets/c7adaa67-379e-409c-a21d-65893c663ab3" />
