import Tarjeta from './Tarjeta';
import ItemDetalle from './ItemDetalle';

function DetallePedido({ pedido }) {
  const total = pedido.detalles.reduce(
    (acc, det) => acc + det.cantidad * Number(det.precio_unitario),
    0
  );

  return (
    <Tarjeta titulo={`Pedido #${pedido.id} — Cliente: ${pedido.cliente}`}>
      <p>Fecha: {pedido.fecha} | Estado: <strong>{pedido.estado}</strong></p>

      <h4>Detalles de Items ({pedido.detalles.length}):</h4>
      <ul className="lista-detalles">
        {pedido.detalles.map((det) => (
          <ItemDetalle
            key={det.id}
            nombreProducto={det.producto_nombre}
            cantidad={det.cantidad}
            precioUnitario={det.precio_unitario}
          />
        ))}
      </ul>

      <p className="total-calculado">Total calculado: S/ {total.toFixed(2)}</p>
    </Tarjeta>
  );
}

export default DetallePedido;
