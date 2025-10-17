import React, { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ReCAPTCHA from 'react-google-recaptcha'; // Import the component

function SignUp() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });
  const [captchaToken, setCaptchaToken] = useState(null);
  const navigate = useNavigate();
  const recaptchaRef = useRef();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCaptchaChange = (token) => {
    setCaptchaToken(token);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!captchaToken) {
      alert('Please complete the CAPTCHA before submitting.');
      return;
    }

    try {
      // Send the form data AND the captcha token to the backend
      const response = await fetch('http://localhost:5000/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, captchaToken }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.msg || 'Failed to sign up');
      }

      alert('Sign up successful! Please log in to continue.');
      navigate('/login');
    } catch (error) {
      alert(`Error: ${error.message}`);
      // Reset the CAPTCHA so the user can try again
      recaptchaRef.current.reset();
      setCaptchaToken(null);
    }
  };

  return (
    <div className="form-container">
      <h2>Create Your Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input type="text" id="name" name="name" onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input type="email" id="email" name="email" onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input type="password" id="password" name="password" onChange={handleChange} required minLength="6" />
        </div>
        
        {/* Add the ReCAPTCHA component here */}
        <div className="recaptcha-container">
          <ReCAPTCHA
            ref={recaptchaRef}
            sitekey={process.env.REACT_APP_RECAPTCHA_SITE_KEY}
            onChange={handleCaptchaChange}
          />
        </div>
        
        <button type="submit" className="form-button">Sign Up</button>
      </form>
      <div className="form-links">
        <span>Already have an account? </span>
        <Link to="/login">Log In</Link>
      </div>
    </div>
  );
}

export default SignUp;