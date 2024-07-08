import React from 'react';
import Select from 'react-select';
import { useNavigate } from 'react-router-dom';
import './Menu.css';

function Menu() {
  const navigate = useNavigate();

  const options = [
    { value: 'consulta1', label: 'Consulta 1' },
    { value: 'consulta2', label: 'Consulta 2' },
    { value: 'consulta3', label: 'Consulta 3' },
  ];

  const handleSelectChange = (selectedOption) => {
    navigate(`/${selectedOption.value}`);
  };

  return (
    <div className="menu-container">
      <h1>Aquí puedes realizar tus consultas</h1>
      <Select 
        options={options} 
        placeholder="Selecciona una opción" 
        onChange={handleSelectChange}
        classNamePrefix="custom-select"
      />
    </div>
  );
}

export default Menu;
