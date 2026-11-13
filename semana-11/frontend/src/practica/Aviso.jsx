import { useEffect } from 'react'

// Ejercicio 8 — Muestra "Agregado: <nombre>" y desaparece a los 3 segundos limpiando el setTimeout
function Aviso({ mensaje, onCerrar }) {
  useEffect(() => {
    if (!mensaje) return

    console.log('Efecto Aviso ejecutado:', mensaje)

    const idTemporizador = setTimeout(() => {
      onCerrar()
    }, 3000)

    // Función de limpieza: cancela el temporizador si el componente se desmonta o cambia el mensaje
    return () => clearTimeout(idTemporizador)
  }, [mensaje, onCerrar])

  if (!mensaje) return null

  return <p className="alerta-vacio">{mensaje}</p>
}

export default Aviso