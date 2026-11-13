function Tarjeta({ titulo, children }) {
  return (
    <div className="card-pedido">
      {titulo && <h3>{titulo}</h3>}
      {children}
    </div>
  );
}

export default Tarjeta;
