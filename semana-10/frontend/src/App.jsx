// frontend/src/App.jsx
import { useState } from 'react'
import './App.css'
// Datos escritos a mano movidos a src/datos.js (Ejercicio 1 — Semana 10)
import { productos, pedidos, productosIndependientes, categorias } from './datos'
// Ejercicio 2 — Primer componente funcional (import por defecto)
import TarjetaProducto from './components/TarjetaProducto'
// Ejercicio 3 — Lista que recibe el arreglo y usa map() + key
import ListaProductos from './components/ListaProductos'
// Ejercicio 4 — Contenedor con titulo y children
import Tarjeta from './components/Tarjeta'
// Ejercicio 5 — Relación 1:N con componentes anidados
import DetallePedido from './components/DetallePedido'
// Ejercicio 8 — Formulario controlado con onSubmit y validación
import FormularioProducto from './components/FormularioProducto'
// Ejercicio 10 — Componentes de la investigación propia (Categorías)
import ListaCategorias from './components/ListaCategorias'
// Ejercicio 12 — Formulario de la investigación propia
import FormularioCategoria from './components/FormularioCategoria'

function App() {

  // Ejercicio 8 — La lista de productos ahora vive en el estado
  const [listaProductos, setListaProductos] = useState(productos);

  // Crea un arreglo NUEVO con el producto agregado (sin push)
  const agregarProducto = (nuevo) => {
    const siguienteId = Math.max(0, ...listaProductos.map((p) => p.id)) + 1;
    setListaProductos([...listaProductos, { id: siguienteId, ...nuevo }]);
  };

  // Ejercicio 12 — Las categorías (investigación propia) también viven en el estado
  const [listaCategorias, setListaCategorias] = useState(categorias);

  const agregarCategoria = (nueva) => {
    const siguienteId = Math.max(0, ...listaCategorias.map((c) => c.id)) + 1;
    setListaCategorias([...listaCategorias, { id: siguienteId, ...nueva, productos: [] }]);
  };

  // Variables y expresiones JSX (Parte Guiada)
  const nombreAppGuiada = "Sistema de Gestión Empresarial - Utilería";
  const precioBase = 45.50;
  const porcentajeIGV = 0.18;

  // Función auxiliar para cálculo con decimales
  const calcularPrecioConIGV = (precio, igv) => {
    return (precio * (1 + igv)).toFixed(2);
  };

  // Variables y expresiones JSX para investigación propia
  const nombreAppInvestigacion = "Sistema de Gestión de Inventario — Investigación Propia";
  const igvAplicado = 0.18;
  const presupuestoBase = 12500.00;

  // Función auxiliar para cálculos de investigación
  const calcularMontoIGV = (monto, igv) => {
    return (monto * igv).toFixed(2);
  };

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

      {/* Ejercicio 2 — El mismo componente usado dos veces */}
      <h2 className="subtitulo-seccion">Componente TarjetaProducto</h2>
      <ul className="lista-productos">
        {/* Ejercicio 3 — ahora cada tarjeta recibe sus datos por props */}
        <TarjetaProducto nombre="Cuaderno A4 Anillado" codigo="PROD001" precio="12.50" stock={15} />
        {/* Sin la prop stock → se usa el valor por defecto (stock = 0) */}
        <TarjetaProducto nombre="Corrector Líquido" codigo="PROD006" precio="3.50" />
      </ul>

      <hr className="linea-separadora" />

      {/* Ejercicio 3 — ListaProductos recibe el arreglo completo */}
      <h2 className="subtitulo-seccion">Listado de Productos</h2>

      {/* Ejercicio 8 — Formulario que agrega un producto al estado */}
      <Tarjeta titulo="Registrar nuevo producto">
        <FormularioProducto onAgregar={agregarProducto} />
      </Tarjeta>

      <ListaProductos productos={listaProductos} />

      <hr className="linea-separadora" />

      {/* CANDIDATO 3 → <DetallePedido pedido={...} /> (detalle de la relación 1:N) */}
      {/* Pedidos y Detalles (1:N) */}
      <h2 className="subtitulo-seccion">Listado de Pedidos y Detalles</h2>
      {/* Ejercicio 5 — DetallePedido usa ItemDetalle por cada detalle */}
      {pedidos.map((pedido) => (
        <DetallePedido key={pedido.id} pedido={pedido} />
      ))}

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

      {/* Mismo componente reutilizado, con su propio límite y mensaje */}
      <ListaProductos
        productos={productosIndependientes}
        limiteUltimas={4}
        mensajeVacio="No hay registros de productos independientes en el sistema."
      />

      <hr className="linea-separadora" />

      {/*Entidad 2 con Relación 1:N, Conteo y Total Calculado en JS */}
      <h2 className="subtitulo-seccion" style={{ borderLeftColor: '#10b981' }}>
        Entidad 2: Categorías de Inventario
      </h2>

      {/* Ejercicio 12 — Formulario que agrega una categoría al estado */}
      <Tarjeta titulo="Registrar nueva categoría">
        <FormularioCategoria onAgregar={agregarCategoria} />
      </Tarjeta>

      {/* Ejercicio 10 — Investigación propia con componentes y props */}
      <ListaCategorias categorias={listaCategorias} />
    </div>
  )
}

export default App
