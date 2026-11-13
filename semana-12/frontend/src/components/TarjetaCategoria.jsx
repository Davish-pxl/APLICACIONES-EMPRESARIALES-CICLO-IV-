import { useState } from 'react';
import Tarjeta from './Tarjeta';
import DetalleCategoria from './DetalleCategoria';

function TarjetaCategoria({ id, nombre, descripcion = 'Sin descripción', productos = [] }) {
  const [abierta, setAbierta] = useState(false);

  const sinProductos = productos.length === 0;

  function alternar() {
    setAbierta(!abierta);
  }

  return (
    <Tarjeta titulo={`Categoría #${id}: ${nombre}`}>
      <p>{descripcion}</p>

      <button
        type="button"
        className="btn-agregar btn-ver-productos"
        onClick={alternar}
        disabled={sinProductos}
      >
        {sinProductos
          ? 'Sin productos'
          : abierta
            ? 'Ocultar productos'
            : `Ver productos (${productos.length})`}
      </button>

      {abierta && <DetalleCategoria productos={productos} />}
    </Tarjeta>
  );
}

export default TarjetaCategoria;
