import React, { useState } from 'react';
import './Consulta1.css'; 

function Consulta1() {
  const [data, setData] = useState([]);

  useState(() => {
    const consulta1 = async () => {
      const response = await fetch('http://localhost:8000/costos-laborales-ultimo-mes');
      const data = await response.json();

      console.log(data);
      setData(data);
    }

    consulta1();
  })
  return (
    <div className="h_container">
      <h1>¿Cuáles son los costos laborales por pedido en el último mes?</h1>
      <div className="tabla1">
        <table>
          <thead>
            <tr>
              <th>Cliente RIN</th>
              <th>Costo Laboral</th>
              <th>Pedido PO</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.cliente_rin}</td>
                <td>{item.costo_laboral}</td>
                <td>{item.pedido_po}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Consulta1;
