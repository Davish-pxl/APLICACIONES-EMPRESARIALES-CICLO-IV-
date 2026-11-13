// frontend/src/datos.js
// Datos escritos a mano (Semana 9) separados de App.jsx.
// En la Semana 10 los componentes los recibirán mediante props.

// ===== PARTE GUIADA =====

// Entidad principal (Productos)
export const productos = [
  { id: 1, codigo: "PROD001", nombre: "Cuaderno A4 Anillado", precio: "12.50", stock: 15 },
  { id: 2, codigo: "PROD002", nombre: "Bolígrafo Azul 0.7mm", precio: "2.80", stock: 3 },
  { id: 3, codigo: "PROD003", nombre: "Resaltador Amarillo", precio: "4.20", stock: 0 },
  { id: 4, codigo: "PROD004", nombre: "Archivador Palanca Lomo Ancho", precio: "18.00", stock: 8 },
  { id: 5, codigo: "PROD005", nombre: "Engrapadora Mediana Metal", precio: "25.00", stock: 2 }
];

// Relación 1:N (Pedidos con detalles anidados)
export const pedidos = [
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

// ===== INVESTIGACIÓN PROPIA =====

// Entidad 1 — Catálogo General de Productos Independientes
export const productosIndependientes = [
  { id: 201, codigo: "PROD-101", nombre: "Impresora Multifuncional Láser", precio: "1450.00", stock: 4 },
  { id: 202, codigo: "PROD-102", nombre: "Disco Duro Externo 2TB", precio: "280.00", stock: 15 },
  { id: 203, codigo: "PROD-103", nombre: "Cable HDMI 2.1 4K", precio: "45.00", stock: 0 }
];

// Entidad 2 — Categorías con relación 1:N a Productos
export const categorias = [
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
  },
  {
    id: 3,
    nombre: "Papelería Escolar",
    descripcion: null,
    productos: []
  }
];
