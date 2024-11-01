// app.js
import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

function App() {
  const [accessLogs, setAccessLogs] = useState([]);

  useEffect(() => {
    // Simulando una llamada a API para obtener datos de acceso
    setAccessLogs([
      { id: 1, user: "Juan Pérez", zone: "Lobby", accessDate: "2024-10-10", status: "Permitido" },
      { id: 2, user: "Maria García", zone: "Gimnasio", accessDate: "2024-10-11", status: "Denegado" },
      { id: 3, user: "Luis Díaz", zone: "Piscina", accessDate: "2024-10-12", status: "Permitido" },
    ]);
  }, []);

  return (
    <div className="container">
      <Header />
      <AccessLogs logs={accessLogs} />
    </div>
  );
}

function Header() {
  return (
    <header className="header">
      <h1>Control de Acceso Inteligente</h1>
      <nav className="menu">
        <a href="#">Dashboard</a>
        <a href="#">Usuarios</a>
        <a href="#">Zonas</a>
        <a href="#">Historial de Accesos</a>
      </nav>
    </header>
  );
}

function AccessLogs({ logs }) {
  return (
    <div className="card">
      <h2>Historial de Accesos</h2>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Usuario</th>
            <th>Zona</th>
            <th>Fecha</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.user}</td>
              <td>{log.zone}</td>
              <td>{log.accessDate}</td>
              <td>{log.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));