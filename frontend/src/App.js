import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './pages/Home';
import Menu from './pages/Menu';
import Consulta1 from './pages/Consulta1';
import Consulta2 from './pages/Consulta2';
import Consulta3 from './pages/Consulta3';
import Consulta4 from './pages/Consulta4';
import Consulta5 from './pages/Consulta5';
import './App.css';

function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/menu" element={<Menu />} />
          <Route path="/consulta1" element={<Consulta1 />} />
          <Route path="/consulta2" element={<Consulta2 />} />
          <Route path="/consulta3" element={<Consulta3 />} />
          <Route path="/consulta4" element={<Consulta4 />} />
          <Route path="/consulta5" element={<Consulta5 />} />
        </Routes>
    </Router>
  );
}

export default App;
