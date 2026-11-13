// Ejercicios 1 y 3 — Muestra UN producto y avisa al padre con onAgregar
function ProductoCard({ producto, onAgregar }) {
  const agotado = producto.stock === 0

  return (
    <li className="item-producto">
      <div className="info-producto">
        <strong>{producto.nombre}</strong> ({producto.codigo}) —
        <span> Precio: S/ {Number(producto.precio).toFixed(2)}</span>
      </div>
      <div className="badges-container">
        {agotado ? (
          <span className="badge agotado">Agotado</span>
        ) : (
          <span className="badge disponible">Stock: {producto.stock}</span>
        )}
        {/* Se pasa una FUNCIÓN (flecha), no el resultado de llamarla */}
        <button
          className="btn-agregar"
          disabled={agotado}
          onClick={() => onAgregar(producto)}
        >
          Agregar
        </button>
      </div>
    </li>
  )
}

export default ProductoCard

