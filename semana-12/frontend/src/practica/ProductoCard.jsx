function ProductoCard({ producto }) {
  return (
    <li className="item-producto">
      <div className="info-producto">
        <strong>{producto.nombre}</strong> ({producto.codigo}) —
        <span> Precio: S/ {Number(producto.precio).toFixed(2)}</span>
      </div>
      <div className="badges-container">
        {producto.stock === 0 ? (
          <span className="badge agotado">Agotado</span>
        ) : (
          <span className="badge disponible">Stock: {producto.stock}</span>
        )}
      </div>
    </li>
  )
}

export default ProductoCard
