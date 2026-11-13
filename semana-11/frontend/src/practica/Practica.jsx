import { useState } from 'react'
import { productos } from './datos'
import Buscador from './Buscador'
import Catalogo from './Catalogo'
import Carrito from './Carrito'
import Aviso from './Aviso'

function Practica() {
  // Ejercicio 4 — Estado del carrito en el componente padre Practica
  const [lineas, setLineas] = useState([])

  // Ejercicio 7 — Estado del texto del buscador compartido entre Buscador y Catalogo
  const [busqueda, setBusqueda] = useState('')

  // Ejercicio 8 — Estado del mensaje temporal al agregar un producto
  const [aviso, setAviso] = useState('')

  // Ejercicios 4 y 8 — Si ya está en el carrito aumenta cantidad con map(); si no, crea arreglo nuevo (sin push)
  const agregarAlCarrito = (producto) => {
    setLineas((prevLineas) => {
      const existe = prevLineas.find((linea) => linea.id === producto.id)
      if (existe) {
        return prevLineas.map((linea) =>
          linea.id === producto.id
            ? { ...linea, cantidad: linea.cantidad + 1 }
            : linea
        )
      }
      return [
        ...prevLineas,
        {
          id: producto.id,
          nombre: producto.nombre,
          precio: producto.precio,
          cantidad: 1,
        },
      ]
    })
    // Ejercicio 8 — Activa el aviso temporal con el nombre del producto
    setAviso(`Agregado: ${producto.nombre}`)
  }

  // Ejercicio 6 — Resta 1 unidad con map() y elimina la línea si llega a 0 con filter() (inmutable)
  const quitarDelCarrito = (id) => {
    setLineas((prevLineas) =>
      prevLineas
        .map((linea) =>
          linea.id === id ? { ...linea, cantidad: linea.cantidad - 1 } : linea
        )
        .filter((linea) => linea.cantidad > 0)
    )
  }

  // Ejercicio 6 — Vacía el carrito entregando un arreglo nuevo []
  const vaciarCarrito = () => {
    setLineas([])
  }

  // Ejercicio 7 — Filtra productos con filter() e includes() antes de pasarlos a Catalogo
  const productosFiltrados = productos.filter((producto) =>
    producto.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  return (
    <section>
      <h2 className="subtitulo-seccion">Práctica S11: Utilería</h2>
      {/* Ejercicio 8 — Aviso temporal que desaparece a los 3 segundos */}
      <Aviso mensaje={aviso} onCerrar={() => setAviso('')} />
      <div className="panel-practica">
        {/* Ejercicio 7 — Buscador controlado y Catalogo recibiendo productosFiltrados */}
        <Buscador valor={busqueda} onCambiar={setBusqueda} />
        <Catalogo productos={productosFiltrados} onAgregar={agregarAlCarrito} />
        {/* Ejercicio 6 — Se entregan las funciones onQuitar y onVaciar al hermano Carrito */}
        <Carrito
          lineas={lineas}
          onQuitar={quitarDelCarrito}
          onVaciar={vaciarCarrito}
        />
      </div>
    </section>
  )
}

export default Practica