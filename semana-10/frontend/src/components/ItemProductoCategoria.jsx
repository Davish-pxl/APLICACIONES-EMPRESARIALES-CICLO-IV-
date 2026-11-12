function ItemProductoCategoria({ nombreProducto, codigo, precio, stock = 0, limiteUltimas = 3 }) {
  return (
    <li className="item-producto-categoria">
      <strong>{nombreProducto}</strong> ({codigo}) — S/ {Number(precio).toFixed(2)} c/u —{' '}
      {stock === 0 ? (
        <span className="badge agotado">Agotado</span>
      ) : (
        <span className="badge disponible">Stock: {stock}</span>
      )}
      {stock > 0 && stock <= limiteUltimas && (
        <span className="badge ultima-unidades">¡Últimas unidades!</span>
      )}
    </li>
  );
}

export default ItemProductoCategoria;
