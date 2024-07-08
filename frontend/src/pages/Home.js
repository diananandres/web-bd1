import React from 'react';
import { useNavigate } from 'react-router-dom';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './Home.css'; 

function Home() {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/menu');
  };

  return (
    <div className="h_container">
      <p>PuntoZip</p>
      <button className="circle_button" onClick={handleButtonClick}>
        <i className="bi bi-arrow-right-circle-fill"></i>
      </button>
    </div>
  );
}

export default Home;
