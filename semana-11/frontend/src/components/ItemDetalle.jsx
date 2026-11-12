function ItemDetalle({ nombreProducto, cantidad, precioUnitario }) {
  const subtotal = cantidad * Number(precioUnitario);

  return (
    <li>
      {nombreProducto} x {cantidad} {cantidad === 1 ? 'unidad' : 'unidades'} — S/ {Number(precioUnitario).toFixed(2)} c/u
      {' '}= <strong>S/ {subtotal.toFixed(2)}</strong>
    </li>
  );
}

export default ItemDetalle;
