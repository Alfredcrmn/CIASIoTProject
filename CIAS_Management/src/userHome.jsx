// src/UserHome.jsx
import React, { useState } from "react";
import "./styles/userHome.css";

function UserHome() {
  const [username, setUsername] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleRegister = async () => {
    if (!username || !selectedFile) {
      setMessage("Please enter a username and select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("username", username);

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`Success: ${result.message}`);
        console.log("Face registered successfully.");
      } else {
        setMessage(`Error: ${result.message}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleLogin = async () => {
    if (!username || !selectedFile) {
      setMessage("Please enter a username and select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("username", username);

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`Success: ${result.message}`);
        console.log("Login successful.");
      } else {
        setMessage(`Error: ${result.message}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  return (
    <div className="user-home">
      <h1>Facial Recognition App</h1>
      <div className="form">
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <label htmlFor="file">Upload an Image:</label>
        <input
          type="file"
          id="file"
          accept="image/*"
          onChange={handleFileChange}
        />

        <div className="buttons">
          <button onClick={handleRegister}>Register Face</button>
          <button onClick={handleLogin}>Login</button>
        </div>

        {message && <p className="message">{message}</p>}
      </div>
    </div>
  );
}

export default UserHome;