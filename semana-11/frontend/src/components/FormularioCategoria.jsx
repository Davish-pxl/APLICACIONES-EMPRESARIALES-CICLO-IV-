import { useState } from 'react';

const formularioVacio = { nombre: '', descripcion: '' };

function validar(datos) {
  const errores = {};
  const nombre = datos.nombre.trim();

  if (nombre.length < 3) {
    errores.nombre = 'El nombre de la categoría debe tener al menos 3 caracteres.';
  } else if (nombre.length > 100) {
    errores.nombre = 'El nombre no puede tener más de 100 caracteres.';
  }

  return errores;
}

function FormularioCategoria({ onAgregar }) {
  const [datos, setDatos] = useState(formularioVacio);
  const [errores, setErrores] = useState({});
  const [mensajeExito, setMensajeExito] = useState('');

  function manejarCambio(e) {
    const { name, value } = e.target;
    setDatos({ ...datos, [name]: value });
    setMensajeExito('');
  }

  function manejarEnvio(e) {
    e.preventDefault();

    const nuevosErrores = validar(datos);
    setErrores(nuevosErrores);

    if (Object.keys(nuevosErrores).length > 0) {
      setMensajeExito('');
      return;
    }

    const descripcion = datos.descripcion.trim();

    onAgregar({
      nombre: datos.nombre.trim(),
      descripcion: descripcion === '' ? null : descripcion,
    });

    setMensajeExito(`Categoría "${datos.nombre.trim()}" agregada a la lista.`);
    setDatos(formularioVacio);
  }

  return (
    <form className="form-categoria" onSubmit={manejarEnvio} noValidate>
      <div className="form-grid">
        <label className="form-campo form-campo-ancho">
          Nombre
          <input
            name="nombre"
            value={datos.nombre}
            onChange={manejarCambio}
            placeholder="Ej.: Útiles de Arte"
          />
          {errores.nombre && <span className="form-error">{errores.nombre}</span>}
        </label>

        <label className="form-campo form-campo-ancho">
          Descripción (opcional)
          <textarea
            name="descripcion"
            rows="2"
            value={datos.descripcion}
            onChange={manejarCambio}
            placeholder="Ej.: Témperas, pinceles y lienzos"
          />
        </label>
      </div>

      <button type="submit" className="btn-guardar">Agregar categoría</button>
      {mensajeExito && <p className="form-exito">{mensajeExito}</p>}
    </form>
  );
}

export default FormularioCategoria;
