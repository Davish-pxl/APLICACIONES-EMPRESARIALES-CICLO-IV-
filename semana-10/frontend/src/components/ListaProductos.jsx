import { useState } from 'react';
import TarjetaProducto from './TarjetaProducto';

function ListaProductos({ productos, limiteUltimas, mensajeVacio = "No hay registros de productos disponibles." }) {
  const [busqueda, setBusqueda] = useState('');

  if (productos.length === 0) {
    return <p className="alerta-vacio">{mensajeVacio}</p>;
  }

  const texto = busqueda.trim().toLowerCase();
  const filtrados = productos.filter((prod) =>
    prod.nombre.toLowerCase().includes(texto)
  );

  return (
    <div className="contenedor-lista">
      <div className="buscador">
        <input
          type="search"
          className="campo-busqueda"
          placeholder="Buscar producto por nombre..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <span className="conteo-busqueda">
          Mostrando {filtrados.length} de {productos.length}
        </span>
      </div>

      {filtrados.length === 0 ? (
        <p className="alerta-vacio">Ningún producto coincide con "{busqueda}".</p>
      ) : (
        <ul className="lista-productos">
          {filtrados.map((prod) => (
            <TarjetaProducto
              key={prod.id}
              nombre={prod.nombre}
              codigo={prod.codigo}
              precio={prod.precio}
              stock={prod.stock}
              limiteUltimas={limiteUltimas}
            />
          ))}
        </ul>
      )}
    </div>
  );
}

export default ListaProductos;
