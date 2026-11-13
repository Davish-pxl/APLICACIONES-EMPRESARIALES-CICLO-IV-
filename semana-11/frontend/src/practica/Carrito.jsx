import { useEffect } from 'react'

// Ejercicios 4, 5, 6 y 8 — Hermano de Catalogo: recibe datos (lineas) y avisa con funciones (onQuitar, onVaciar)
function Carrito({ lineas, onQuitar, onVaciar }) {
  // Ejercicio 5 — Datos DERIVADOS: se calculan en cada render a partir de `lineas`, sin useState
  const unidades = lineas.reduce((suma, linea) => suma + linea.cantidad, 0)
  const total = lineas.reduce(
    (suma, linea) => suma + Number(linea.precio) * linea.cantidad,
    0,
  )

  // Ejercicio 8 (NUEVO) — Sincroniza document.title con las unidades del carrito en Utilería
  useEffect(() => {
    console.log('Efecto Carrito ejecutado — unidades:', unidades)
    document.title =
      unidades > 0 ? `Carrito (${unidades}) — Utilería` : 'Práctica S11: Utilería'
  }, [unidades])

  return (
    <aside className="carrito">
      <h3>Carrito</h3>

      {lineas.length === 0 && <p className="alerta-vacio">El carrito está vacío</p>}

      <ul className="lista-productos">
        {lineas.map((linea) => (
          <li key={linea.id} className="item-producto">
            <div className="info-producto">
              <strong>{linea.nombre}</strong> × {linea.cantidad} —
              <span> S/ {(Number(linea.precio) * linea.cantidad).toFixed(2)}</span>
            </div>
            {/* Ejercicio 6 — Botón para quitar 1 unidad de esta línea */}
            <button className="btn-agregar" onClick={() => onQuitar(linea.id)}>
              Quitar
            </button>
          </li>
        ))}
      </ul>

      {/* Ejercicio 5 — Muestra los totales derivados calculados con reduce() */}
      <p><strong>Unidades:</strong> {unidades}</p>
      <p><strong>Total: S/ {total.toFixed(2)}</strong></p>

      {/* Ejercicio 6 — Botón visible solo si hay productos para vaciar el carrito */}
      {lineas.length > 0 && (
        <button className="btn-agregar" onClick={onVaciar}>
          Vaciar carrito
        </button>
      )}
    </aside>
  )
}

export default Carrito