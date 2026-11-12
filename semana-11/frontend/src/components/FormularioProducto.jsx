import { useState } from 'react';

const formularioVacio = { codigo: '', nombre: '', precio: '', stock: '' };

function validar(datos) {
  const errores = {};

  if (datos.codigo.trim() === '') {
    errores.codigo = 'El código es obligatorio.';
  } else if (datos.codigo.trim().length > 20) {
    errores.codigo = 'El código no puede tener más de 20 caracteres.';
  }

  if (datos.nombre.trim() === '') {
    errores.nombre = 'El nombre es obligatorio.';
  } else if (datos.nombre.trim().length > 100) {
    errores.nombre = 'El nombre no puede tener más de 100 caracteres.';
  }

  if (datos.precio === '' || Number(datos.precio) <= 0) {
    errores.precio = 'El precio debe ser mayor que cero.';
  }

  if (datos.stock === '' || !Number.isInteger(Number(datos.stock)) || Number(datos.stock) < 0) {
    errores.stock = 'El stock debe ser un número entero mayor o igual a cero.';
  }

  return errores;
}

function FormularioProducto({ onAgregar }) {
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

    onAgregar({
      codigo: datos.codigo.trim(),
      nombre: datos.nombre.trim(),
      precio: Number(datos.precio).toFixed(2),
      stock: Number(datos.stock),
    });

    setMensajeExito(`Producto "${datos.nombre.trim()}" agregado a la lista.`);
    setDatos(formularioVacio);
  }

  return (
    <form className="form-producto" onSubmit={manejarEnvio} noValidate>
      <div className="form-grid">
        <label className="form-campo">
          Código
          <input name="codigo" value={datos.codigo} onChange={manejarCambio} placeholder="Ej.: PROD006" />
          {errores.codigo && <span className="form-error">{errores.codigo}</span>}
        </label>

        <label className="form-campo">
          Nombre
          <input name="nombre" value={datos.nombre} onChange={manejarCambio} placeholder="Ej.: Tijera Escolar" />
          {errores.nombre && <span className="form-error">{errores.nombre}</span>}
        </label>

        <label className="form-campo">
          Precio (S/)
          <input name="precio" type="number" step="0.01" value={datos.precio} onChange={manejarCambio} placeholder="Ej.: 5.50" />
          {errores.precio && <span className="form-error">{errores.precio}</span>}
        </label>

        <label className="form-campo">
          Stock
          <input name="stock" type="number" step="1" value={datos.stock} onChange={manejarCambio} placeholder="Ej.: 10" />
          {errores.stock && <span className="form-error">{errores.stock}</span>}
        </label>
      </div>

      <button type="submit" className="btn-guardar">Agregar producto</button>
      {mensajeExito && <p className="form-exito">{mensajeExito}</p>}
    </form>
  );
}

export default FormularioProducto;
