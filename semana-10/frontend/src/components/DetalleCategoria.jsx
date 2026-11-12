import ItemProductoCategoria from './ItemProductoCategoria';

function DetalleCategoria({ productos = [] }) {
  const cantidad = productos.length;
  const valorTotal = productos.reduce(
    (acc, prod) => acc + prod.stock * Number(prod.precio),
    0
  );

  if (cantidad === 0) {
    return <p className="categoria-vacia">Esta categoría todavía no tiene productos.</p>;
  }

  return (
    <>
      <h4>
        Productos pertenecientes a esta categoría ({cantidad} {cantidad === 1 ? 'producto' : 'productos'}):
      </h4>

      <ul className="lista-detalles">
        {productos.map((prod) => (
          <ItemProductoCategoria
            key={prod.id}
            nombreProducto={prod.nombre}
            codigo={prod.codigo}
            precio={prod.precio}
            stock={prod.stock}
          />
        ))}
      </ul>

      <p className="total-categoria">
        Valor Total del Stock en Categoría: S/ {valorTotal.toFixed(2)}
      </p>
    </>
  );
}

export default DetalleCategoria;
