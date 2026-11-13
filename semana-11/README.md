# Semana 11 — Estado y efectos en React

**Repositorio:** <https://github.com/Davish-pxl/APLICACIONES-EMPRESARIALES-CICLO-IV->
**Carpeta:** <https://github.com/Davish-pxl/APLICACIONES-EMPRESARIALES-CICLO-IV-/tree/main/semana-11>

Mini catálogo de utilería con carrito, hecho en `frontend/src/practica/` y mostrado en `App.jsx` con `<Practica />`.

## Cómo ejecutar

```powershell
cd semana-11/frontend
npm install
npm run dev
```

Abrir `http://localhost:5173/`. Requiere Node.js 20.19+ o 22.12+.

## Componentes

| Componente | Qué hace |
|---|---|
| `Practica` | Padre: guarda el estado del carrito, la búsqueda y el aviso |
| `Buscador` | Campo controlado que filtra los productos |
| `Catalogo` | Lista los productos con `map` y `key` |
| `ProductoCard` | Muestra un producto y avisa con `onAgregar` |
| `Carrito` | Muestra líneas, unidades y total (`reduce`); permite quitar y vaciar |
| `Aviso` | Mensaje "Agregado: …" que desaparece a los 3 s (`useEffect` + `setTimeout`) |

## Conceptos aplicados

- Estado levantado al componente padre y comunicación entre hermanos con props y funciones.
- Actualización inmutable del estado (`map`, `filter`, spread; sin `push`).
- Datos derivados (unidades y total) calculados sin `useState`.
- `useEffect` con función de limpieza (`Aviso`) y para actualizar `document.title` (`Carrito`).

Los datos de ejemplo están en `practica/datos.js`.