import { productos } from './datos'
import Catalogo from './Catalogo'

function Practica() {
  return (
    <section>
      <h2 className="subtitulo-seccion">Práctica S11: Utilería</h2>
      <Catalogo productos={productos} />
    </section>
  )
}

export default Practica
