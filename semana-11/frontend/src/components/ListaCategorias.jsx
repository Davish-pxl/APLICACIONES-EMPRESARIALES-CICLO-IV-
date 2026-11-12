import { useState } from 'react';
import TarjetaCategoria from './TarjetaCategoria';

function ListaCategorias({ categorias, mensajeVacio = 'No hay categorías registradas en el sistema.' }) {
  const [busqueda, setBusqueda] = useState('');

  if (categorias.length === 0) {
    return <p className="alerta-vacio">{mensajeVacio}</p>;
  }

  const texto = busqueda.trim().toLowerCase();
  const filtradas = categorias.filter((cat) =>
    cat.nombre.toLowerCase().includes(texto) ||
    (cat.descripcion ?? '').toLowerCase().includes(texto)
  );

  return (
    <div className="lista-categorias">
      <div className="buscador">
        <input
          type="search"
          className="campo-busqueda"
          placeholder="Buscar categoría por nombre o descripción..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <span className="conteo-busqueda">
          Mostrando {filtradas.length} de {categorias.length}
        </span>
      </div>

      {filtradas.length === 0 ? (
        <p className="alerta-vacio">Ninguna categoría coincide con "{busqueda}".</p>
      ) : (
        filtradas.map((cat) => (
          <TarjetaCategoria
            key={cat.id}
            id={cat.id}
            nombre={cat.nombre}
            descripcion={cat.descripcion ?? undefined}
            productos={cat.productos}
          />
        ))
      )}
    </div>
  );
}

export default ListaCategorias;
