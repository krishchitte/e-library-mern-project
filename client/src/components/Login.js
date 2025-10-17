import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate

function Login() {
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const navigate = useNavigate(); // Hook for navigation

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.msg || 'Login failed');
      }
      // Save the token from the server
      localStorage.setItem('token', data.token);
      alert('Login successful!');
      window.location = '/profile'; // Force a reload to update auth state
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  return (
    <div className="form-container">
      <h2>Log In to Your Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input type="email" id="email" name="email" value={credentials.email} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" value={credentials.password} onChange={handleChange} required />
        </div>
        <button type="submit" className="form-button">Log In</button>
      </form>
      <div className="form-links">
        <a href="#">Forgot Password?</a>
        <span>|</span>
        {/* Update this line */}
        <Link to="/signup">Don't have an account? Sign Up</Link>
      </div>
    </div>
  );
}

export default Login;
