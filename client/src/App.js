import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import { CartProvider, useCart } from './context/CartContext';
import "./App.css";

// Import all necessary components
import Home from "./components/Home";
import BrowseBooks from "./components/BrowseBooks";
import Profile from "./components/Profile";
import ContactUs from "./components/ContactUs";
import Login from "./components/Login";
import SignUp from "./components/SignUp";
import PaymentPage from "./components/PaymentPage";
import CheckoutPage from "./components/CheckoutPage"; // 1. Import the new component
import Cart from "./components/Cart";

function Navigation() {
  const [isCartOpen, setIsCartOpen] = useState(false);
  const { cartItems, setCartItems } = useCart(); // Added setCartItems for cart fetch
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const navigate = useNavigate();

  // Effect to fetch the cart from the server when a user logs in
  useEffect(() => {
    const fetchCart = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        setIsLoggedIn(true);
        try {
          const response = await fetch('http://localhost:5000/api/cart', {
            headers: { 'x-auth-token': token },
          });
          const data = await response.json();
          if (response.ok && data.items) {
            setCartItems(data.items);
          }
        } catch (error) {
          console.error("Failed to fetch cart:", error);
        }
      } else {
        setIsLoggedIn(false);
        setCartItems([]); // Clear cart on logout
      }
    };

    fetchCart();

    // Listen for storage changes to update login status across tabs/windows
    const handleStorageChange = () => {
      fetchCart(); // Re-fetch cart and update login status
    };
    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
    };
  }, [isLoggedIn, setCartItems]);


  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false); // Update state immediately
    alert('You have been logged out.');
    navigate('/login');
  };

  return (
    <>
      <nav className="navbar">
        <div className="nav-left">
          <img src="/logo.svg" alt="logo" className="logo" />
          <h1 className="title">E-LIBRARY</h1>
        </div>
        <div className="nav-right">
          <ul className="links">
            <li><Link to="/" className="link">Home</Link></li>
            <li><Link to="/browse" className="link">Browse Books</Link></li>
            <li><Link to="/contact" className="link">Contact Us</Link></li>
            {isLoggedIn ? (
              <>
                <li><Link to="/profile" className="link">Profile</Link></li>
                <li><button onClick={handleLogout} className="link logout-btn">Logout</button></li>
              </>
            ) : (
              <>
                <li><Link to="/login" className="link">Log In</Link></li>
                <li><Link to="/signup" className="link">Sign Up</Link></li>
              </>
            )}
          </ul>
          {isLoggedIn && (
            <button className="cart-icon-btn" onClick={() => setIsCartOpen(true)}>
              🛒
              {cartItems.length > 0 && <span className="cart-count">{cartItems.length}</span>}
            </button>
          )}
        </div>
      </nav>
      <Cart isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </>
  );
}

function AppContent() {
    return (
        <div className="App">
            <Navigation />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/browse" element={<BrowseBooks />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/contact" element={<ContactUs />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/payment" element={<PaymentPage />} />
                <Route path="/checkout" element={<CheckoutPage />} /> {/* 2. Add this route */}
            </Routes>
        </div>
    );
}

function App() {
  return (
    <Router>
      <CartProvider>
        <AppContent />
      </CartProvider>
    </Router>
  );
}

export default App;

