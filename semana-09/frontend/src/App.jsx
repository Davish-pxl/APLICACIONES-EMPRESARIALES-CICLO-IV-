// frontend/src/App.jsx
import './App.css'

function App() {

  // Variables y expresiones JSX (Parte Guiada)
  const nombreAppGuiada = "Sistema de Gestión Empresarial - Utilería";
  const precioBase = 45.50;
  const porcentajeIGV = 0.18;

  // Función auxiliar para cálculo con decimales
  const calcularPrecioConIGV = (precio, igv) => {
    return (precio * (1 + igv)).toFixed(2);
  };

  // Arreglo de la entidad principal (Productos)
  const productos = [
    { id: 1, codigo: "PROD001", nombre: "Cuaderno A4 Anillado", precio: "12.50", stock: 15 },
    { id: 2, codigo: "PROD002", nombre: "Bolígrafo Azul 0.7mm", precio: "2.80", stock: 3 },
    { id: 3, codigo: "PROD003", nombre: "Resaltador Amarillo", precio: "4.20", stock: 0 },
    { id: 4, codigo: "PROD004", nombre: "Archivador Palanca Lomo Ancho", precio: "18.00", stock: 8 },
    { id: 5, codigo: "PROD005", nombre: "Engrapadora Mediana Metal", precio: "25.00", stock: 2 }
  ];

  // Arreglo relación 1:N (Pedidos con detalles anidados)
  const pedidos = [
    {
      id: 101,
      cliente: "Juan Pérez",
      fecha: "2026-04-10",
      estado: "PAGADO",
      detalles: [
        { id: 1, producto_nombre: "Cuaderno A4 Anillado", cantidad: 2, precio_unitario: "12.50" },
        { id: 2, producto_nombre: "Bolígrafo Azul 0.7mm", cantidad: 5, precio_unitario: "2.80" }
      ]
    },
    {
      id: 102,
      cliente: "María Gómez",
      fecha: "2026-04-12",
      estado: "PENDIENTE",
      detalles: [
        { id: 3, producto_nombre: "Archivador Palanca Lomo Ancho", cantidad: 1, precio_unitario: "18.00" },
        { id: 4, producto_nombre: "Engrapadora Mediana Metal", cantidad: 1, precio_unitario: "25.00" }
      ]
    }
  ];

  // Variables y expresiones JSX para investigación propia
  const nombreAppInvestigacion = "Sistema de Gestión de Inventario — Investigación Propia";
  const igvAplicado = 0.18;
  const presupuestoBase = 12500.00;

  // Función auxiliar para cálculos de investigación
  const calcularMontoIGV = (monto, igv) => {
    return (monto * igv).toFixed(2);
  };

  // Entidad 1 — Catálogo General de Productos Independientes
  const productosIndependientes = [
    { id: 201, codigo: "PROD-101", nombre: "Impresora Multifuncional Láser", precio: "1450.00", stock: 4 },
    { id: 202, codigo: "PROD-102", nombre: "Disco Duro Externo 2TB", precio: "280.00", stock: 15 },
    { id: 203, codigo: "PROD-103", nombre: "Cable HDMI 2.1 4K", precio: "45.00", stock: 0 }
  ];

  // Entidad 2 — Categorías con relación 1:N a Productos
  const categorias = [
    {
      id: 1,
      nombre: "Tecnología y Equipos de Oficina",
      descripcion: "Dispositivos electrónicos, periféricos y accesorios",
      productos: [
        { id: 101, codigo: "TEC-01", nombre: "Monitor IPS 27 Pulgadas 4K", precio: "1250.00", stock: 8 },
        { id: 102, codigo: "TEC-02", nombre: "Teclado Mecánico Inalámbrico", precio: "320.00", stock: 2 },
        { id: 103, codigo: "TEC-03", nombre: "Mouse Ergonómico Vertical", precio: "150.00", stock: 0 }
      ]
    },
    {
      id: 2,
      nombre: "Mobiliario Ergonómico",
      descripcion: "Escritorios ajustables y sillas de oficina",
      productos: [
        { id: 104, codigo: "MOB-01", nombre: "Silla Ejecutiva Malla Transpirable", precio: "680.00", stock: 5 },
        { id: 105, codigo: "MOB-02", nombre: "Escritorio Eléctrico Standing Desk", precio: "1850.00", stock: 1 }
      ]
    }
  ];

  return (
    <div className="container">
      {/* VISTA GUIADA */}
      <div className="app-header">
        <h1 style={{ 
          color: '#1e293b', 
          fontSize: '1.8rem', 
          lineHeight: '1.3', 
          borderBottom: '3px solid #3498db', 
          paddingBottom: '12px' 
        }}>
          {nombreAppGuiada}
        </h1>
      </div>

      {/* Cálculos y expresiones */}
      <div className="card-calculo">
        <p><strong>Precio base del producto:</strong> S/ {precioBase.toFixed(2)}</p>
        <p><strong>Precio total con IGV (18%):</strong> S/ {calcularPrecioConIGV(precioBase, porcentajeIGV)}</p>
      </div>

      <hr className="linea-separadora" />

      {/* Listas con map(), key y condicionales */}
      <h2 className="subtitulo-seccion">Listado de Productos</h2>
      {productos.length === 0 ? (
        <p className="alerta-vacio">No hay registros de productos disponibles.</p>
      ) : (
        <ul className="lista-productos">
          {productos.map((prod) => (
            <li key={prod.id} className="item-producto">
              <div className="info-producto">
                <strong>{prod.nombre}</strong> ({prod.codigo}) — 
                <span> Precio: S/ {Number(prod.precio).toFixed(2)}</span>
              </div>

              <div className="badges-container">
                {prod.stock === 0 ? (
                  <span className="badge agotado">Agotado</span>
                ) : (
                  <span className="badge disponible">Stock: {prod.stock}</span>
                )}

                {prod.stock > 0 && prod.stock <= 3 && (
                  <span className="badge ultima-unidades">¡Últimas unidades!</span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      <hr className="linea-separadora" />

      {/* Pedidos y Detalles (1:N) */}
      <h2 className="subtitulo-seccion">Listado de Pedidos y Detalles</h2>
      {pedidos.map((pedido) => {
        const totalPedido = pedido.detalles.reduce(
          (acc, item) => acc + item.cantidad * Number(item.precio_unitario),
          0
        );

        return (
          <div key={pedido.id} className="card-pedido">
            <h3>Pedido #{pedido.id} — Cliente: {pedido.cliente}</h3>
            <p>Fecha: {pedido.fecha} | Estado: <strong>{pedido.estado}</strong></p>

            <h4>Detalles de Items:</h4>
            <ul className="lista-detalles">
              {pedido.detalles.map((det) => (
                <li key={det.id}>
                  {det.producto_nombre} x {det.cantidad} unidades — S/ {Number(det.precio_unitario).toFixed(2)} c/u
                </li>
              ))}
            </ul>

            <p style={{ color: '#16a34a', fontSize: '1.05rem', fontWeight: 'bold', marginTop: '10px' }}>
              Total calculado: S/ {totalPedido.toFixed(2)}
            </p>
          </div>
        );
      })}

      {/* INVESTIGACIÓN PROPIA */}
      <div className="app-header" style={{ marginTop: '50px' }}>
        <h1 style={{ 
          color: '#0f172a', 
          fontSize: '1.8rem', 
          lineHeight: '1.3', 
          borderBottom: '3px solid #10b981', 
          paddingBottom: '12px' 
        }}>
          {nombreAppInvestigacion}
        </h1>
      </div>

      {/* Expresiones JSX con estilo en línea style={{ }} */}
      <div className="card-calculo" style={{ backgroundColor: '#f0fdf4', borderColor: '#bbf7d0' }}>
        <p><strong>Presupuesto asignado al área:</strong> S/ {presupuestoBase.toFixed(2)}</p>
        <p><strong>Monto estimado por IGV (18%):</strong> S/ {calcularMontoIGV(presupuestoBase, igvAplicado)}</p>
      </div>

      <hr className="linea-separadora" />

      {/* Entidad 1 con renderizado condicional (Ternario, && y Lista Vacía) */}
      <h2 className="subtitulo-seccion" style={{ borderLeftColor: '#10b981' }}>
        Entidad 1: Catálogo General de Productos
      </h2>

      {productosIndependientes.length === 0 ? (
        <p className="alerta-vacio">No hay registros de productos independientes en el sistema.</p>
      ) : (
        <ul className="lista-productos">
          {productosIndependientes.map((prod) => (
            <li key={prod.id} className="item-producto">
              <div className="info-producto">
                <strong>{prod.nombre}</strong> ({prod.codigo}) — 
                <span> Precio: S/ {Number(prod.precio).toFixed(2)}</span>
              </div>

              <div className="badges-container">
                {/* Ternario para validar disponibilidad */}
                {prod.stock === 0 ? (
                  <span className="badge agotado">Agotado</span>
                ) : (
                  <span className="badge disponible">Stock: {prod.stock}</span>
                )}

                {/* Operador Lógico && para alerta de pocas unidades */}
                {prod.stock > 0 && prod.stock <= 4 && (
                  <span className="badge ultima-unidades">¡Últimas unidades!</span>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}

      <hr className="linea-separadora" />

      {/*Entidad 2 con Relación 1:N, Conteo y Total Calculado en JS */}
      <h2 className="subtitulo-seccion" style={{ borderLeftColor: '#10b981' }}>
        Entidad 2: Categorías de Inventario
      </h2>

      {categorias.length === 0 ? (
        <p className="alerta-vacio">No hay categorías registradas en el sistema.</p>
      ) : (
        categorias.map((cat) => {
          // 1. Conteo por registro calculado con JavaScript
          const cantidadProductos = cat.productos.length;

          // 2. Total por registro calculado con JavaScript (.reduce)
          const totalValorCategoria = cat.productos.reduce(
            (acc, p) => acc + p.stock * Number(p.precio),
            0
          );

          return (
            <div key={cat.id} className="card-pedido">
              <h3>Categoría #{cat.id}: {cat.nombre}</h3>
              <p>{cat.descripcion}</p>

              {/* Muestra del Conteo Calculado */}
              <h4>
                Productos pertenecientes a esta categoría ({cantidadProductos} {cantidadProductos === 1 ? 'producto' : 'productos'}):
              </h4>

              <ul className="lista-detalles">
                {cat.productos.map((prod) => (
                  <li key={prod.id} style={{ marginBottom: '8px' }}>
                    <strong>{prod.nombre}</strong> ({prod.codigo}) — S/ {Number(prod.precio).toFixed(2)} c/u — 

                    {/* Ternario en la lista anidada */}
                    {prod.stock === 0 ? (
                      <span className="badge agotado"> Agotado</span>
                    ) : (
                      <span className="badge disponible"> Stock: {prod.stock}</span>
                    )}

                    {/* Operador && en la lista anidada */}
                    {prod.stock > 0 && prod.stock <= 3 && (
                      <span className="badge ultima-unidades"> ¡Últimas unidades!</span>
                    )}
                  </li>
                ))}
              </ul>

              {/* Muestra del Total Calculado con style={{ }} */}
              <p style={{ color: '#059669', fontSize: '1.05rem', fontWeight: 'bold', marginTop: '10px' }}>
                Valor Total del Stock en Categoría: S/ {totalValorCategoria.toFixed(2)}
              </p>
            </div>
          );
        })
      )}
    </div>
  )
}

export default App