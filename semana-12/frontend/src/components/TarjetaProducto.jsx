import { useState } from 'react';

function TarjetaProducto({ nombre, codigo, precio, stock = 0, limiteUltimas = 3 }) {
  const [cantidad, setCantidad] = useState(0);

  const sinStock = stock === 0;
  const limiteAlcanzado = cantidad >= stock;

  function agregar() {
    setCantidad(cantidad + 1);
  }

  return (
    <li className="item-producto">
      <div className="info-producto">
        <strong>{nombre}</strong> ({codigo}) —
        <span> Precio: S/ {Number(precio).toFixed(2)}</span>
      </div>

      <div className="badges-container">
        {sinStock ? (
          <span className="badge agotado">Agotado</span>
        ) : (
          <span className="badge disponible">Stock: {stock}</span>
        )}

        {stock > 0 && stock <= limiteUltimas && (
          <span className="badge ultima-unidades">¡Últimas unidades!</span>
        )}

        {cantidad > 0 && (
          <span className="contador-seleccion">Seleccionados: {cantidad}</span>
        )}

        <button
          type="button"
          className="btn-agregar"
          onClick={agregar}
          disabled={sinStock || limiteAlcanzado}
        >
          {sinStock ? 'Sin stock' : limiteAlcanzado ? 'Máximo' : '+ Agregar'}
        </button>
      </div>
    </li>
  );
}

export default TarjetaProducto;
