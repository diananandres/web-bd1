import React, { useState } from 'react';
import './Consulta2.css'; 

function Consulta2() {
  const [data, setData] = useState([]);

  useState(() => {
    const consulta2 = async () => {
      const response = await fetch('http://localhost:8000/etapa-mas-demorada-ultimo-mes');
      const data = await response.json();

      console.log(data);
      setData(data);
    }

    consulta2();
  })
  return (
    <div className="h_container">
      <h1>¿Cuál es la etapa que más ha demorado por cliente en cierto pedido en el último mes?</h1>
      <div className="tabla2">
        <table>
          <thead>
            <tr>
              <th>RIN</th>
              <th>Cliente</th>
              <th>Etapa</th>
              <th>Pedido_po</th>
              <th>Tiempo_Etapa_Dias</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.rin}</td>
                <td>{item.cliente}</td>
                <td>{item.etapa}</td>
                <td>{item.pedipo_po}</td>
                <td>{item.tiempo_etapa_dias}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Consulta2;
