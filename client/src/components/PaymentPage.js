import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function PaymentPage() {
  const location = useLocation();
  const navigate = useNavigate();
  // Get book data passed from the "Buy Now" button click
  const { book } = location.state || {}; 

  if (!book) {
    return (
      <div className="form-container">
        <h2>Error</h2>
        <p>No book selected for payment. Please go back and try again.</p>
      </div>
    );
  }

  const handlePayment = async () => {
    // In a real app, you would integrate a payment gateway here.
    // For now, we just simulate success.
    alert('Payment Successful! Thank you for your purchase.');
    
    // After payment, add the book to the user's purchased list via the API
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:5000/api/users/purchase/${book._id}`, {
        method: 'POST',
        headers: { 'x-auth-token': token },
      });

      if (!response.ok) {
        throw new Error('Failed to update your purchase history.');
      }

      // Redirect to the profile page to see the newly purchased book
      navigate('/profile');
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  return (
    <div className="form-container">
      <h2>Complete Your Purchase</h2>
      <div className="payment-summary">
        <img src={book.coverUrl} alt={book.title} className="payment-summary-img" />
        <div className="payment-summary-details">
          <h3>{book.title}</h3>
          <p>by {book.author}</p>
          <p className="price">Price: ₹{book.price.toFixed(2)}</p>
        </div>
      </div>
      <button onClick={handlePayment} className="form-button payment-button">
        Pay Now (₹{book.price.toFixed(2)})
      </button>
    </div>
  );
}

export default PaymentPage;