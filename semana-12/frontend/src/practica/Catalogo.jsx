import ProductoCard from './ProductoCard'

function Catalogo({ productos }) {
  return (
    <ul className="lista-productos">
      {productos.map((producto) => (
        <ProductoCard key={producto.id} producto={producto} />
      ))}
    </ul>
  )
}

export default Catalogo
