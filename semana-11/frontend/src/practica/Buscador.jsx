// Ejercicio 7 — Hermano de Catalogo: campo controlado que recibe valor y avisa con onCambiar
function Buscador({ valor, onCambiar }) {
  return (
    <div className="buscador">
      <input
        type="text"
        className="campo-busqueda"
        placeholder="Buscar producto..."
        value={valor}
        onChange={(e) => onCambiar(e.target.value)}
      />
    </div>
  )
}

export default Buscador