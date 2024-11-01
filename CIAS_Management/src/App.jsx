import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [step, setStep] = useState(0);
  const [role, setRole] = useState(null);

  return (
    <h1>
      Hello, world!
    </h1>
  );
}

export default App;