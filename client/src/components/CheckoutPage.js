import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

function CheckoutPage() {
  const { cartItems, setCartItems } = useCart();
  const navigate = useNavigate();

  const handleConfirmPurchase = async () => {
    const token = localStorage.getItem('token');
    try {
      // Call the new checkout endpoint on the backend
      const response = await fetch('http://localhost:5000/api/users/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-auth-token': token
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.msg || 'Checkout failed.');
      }

      // Clear the cart in the frontend state
      setCartItems([]);
      alert('Purchase successful! Thank you.');
      // Redirect to the profile page to see the purchased books
      navigate('/profile');

    } catch (error) {
      console.error("Checkout error:", error);
      alert(error.message);
    }
  };

  const validCartItems = cartItems.filter(item => item && item.book);
  const totalPrice = validCartItems.reduce((total, item) => total + item.book.price * item.quantity, 0);

  return (
    <div className="form-container checkout-container">
      <h2>Confirm Your Order</h2>
      {validCartItems.length > 0 ? (
        <>
          <div className="checkout-summary">
            <h3>Order Summary</h3>
            <ul className="checkout-items-list">
              {validCartItems.map(({ book, quantity }) => (
                <li key={book._id} className="checkout-item">
                  <span>{book.title} (x{quantity})</span>
                  <span>₹{(book.price * quantity).toFixed(2)}</span>
                </li>
              ))}
            </ul>
            <div className="checkout-total">
              <strong>Total:</strong>
              <strong>₹{totalPrice.toFixed(2)}</strong>
            </div>
          </div>
          <button onClick={handleConfirmPurchase} className="form-button payment-button">
            Confirm Purchase
          </button>
        </>
      ) : (
        <p>Your cart is empty. There is nothing to check out.</p>
      )}
    </div>
  );
}

export default CheckoutPage;
