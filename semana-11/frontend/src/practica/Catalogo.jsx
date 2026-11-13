import ProductoCard from './ProductoCard'

function Catalogo({ productos, onAgregar }) {
  // Ejercicio 7 — Muestra mensaje cuando ningún producto coincide con la búsqueda
  if (productos.length === 0) {
    return <p className="alerta-vacio">No hay productos que coincidan</p>
  }

  return (
    // map para recorrer el arreglo de productos y renderizar un ProductoCard por cada producto
    <ul className="lista-productos">
      {productos.map((producto) => (
        // key y la entrega de producto (y la función onAgregar) a ProductoCard:
        <ProductoCard key={producto.id} producto={producto} onAgregar={onAgregar} />
      ))}
    </ul>
  )
}

export default Catalogo