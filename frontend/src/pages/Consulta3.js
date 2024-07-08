import React, { useState, useEffect } from 'react';
import ReactPaginate from 'react-paginate';
import './Consulta3.css'; 

function Consulta3() {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const itemsPerPage = 7;

  useEffect(() => {
    const consulta3 = async () => {
      const response = await fetch('http://localhost:8000/categorias-mas-solicitadas');
      const data = await response.json();

      console.log(data);
      setData(data);
    }

    consulta3();
  }, []);

  const handlePageClick = (event) => {
    setCurrentPage(event.selected);
  };

  const offset = currentPage * itemsPerPage;
  const currentData = data.slice(offset, offset + itemsPerPage);
  const pageCount = Math.ceil(data.length / itemsPerPage);

  return (
    <div className="h_container">
      <h1>¿Cuáles son las categorías más solicitadas por cada cliente?</h1>
      <div className="tabla3">
        <table>
          <thead>
            <tr>
              <th>RIN</th>
              <th>Cliente_Nombre</th>
              <th>Categoría</th>
              <th>Frecuencia</th>
            </tr>
          </thead>
          <tbody>
            {currentData.map((item, index) => (
              <tr key={index}>
                <td>{item.rin}</td>
                <td>{item.cliente_nombre}</td>
                <td>{item.categoria}</td>
                <td>{item.frecuencia}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <ReactPaginate
          previousLabel={"← Anterior"}
          nextLabel={"Siguiente →"}
          pageCount={pageCount}
          onPageChange={handlePageClick}
          containerClassName={"pagination"}
          previousLinkClassName={"pagination__link"}
          nextLinkClassName={"pagination__link"}
          disabledClassName={"pagination__link--disabled"}
          activeClassName={"pagination__link--active"}
        />
      </div>
    </div>
  );
}

export default Consulta3;
