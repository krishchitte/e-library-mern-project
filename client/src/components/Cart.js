import React from 'react';
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom'; // 1. Import useNavigate

function Cart({ isOpen, onClose }) {
  const { cartItems, setCartItems } = useCart();
  const navigate = useNavigate(); // 2. Initialize useNavigate

  const handleUpdateQuantity = async (bookId, newQuantity) => {
    const quantity = Number(newQuantity);
    if (isNaN(quantity) || quantity < 1) return;

    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:5000/api/cart/update/${bookId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-auth-token': token
        },
        body: JSON.stringify({ quantity }),
      });
      const data = await response.json();
      if (response.ok) {
        setCartItems(data.items);
      } else {
        throw new Error(data.msg || 'Failed to update quantity');
      }
    } catch (error) {
      console.error("Failed to update quantity:", error);
      alert(error.message);
    }
  };

  const handleRemove = async (bookId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:5000/api/cart/remove/${bookId}`, {
        method: 'DELETE',
        headers: { 'x-auth-token': token },
      });
      const data = await response.json();
      if (response.ok) {
        setCartItems(data.items);
      }
    } catch (error) {
      console.error("Failed to remove item:", error);
    }
  };

  // 3. Create a handler for the checkout button
  const handleCheckout = () => {
    onClose(); // Close the cart modal first
    navigate('/checkout'); // Then navigate to the new checkout page
  };

  if (!isOpen) return null;

  const validCartItems = cartItems.filter(item => item && item.book);
  const totalPrice = validCartItems.reduce((total, item) => total + (item.book.price || 0) * item.quantity, 0);

  return (
    <div className="cart-overlay" onClick={onClose}>
      <div className="cart-modal" onClick={(e) => e.stopPropagation()}>
        <div className="cart-header">
          <h2>Your Shopping Cart</h2>
          <button className="cart-close-btn" onClick={onClose}>&times;</button>
        </div>
        <div className="cart-body">
          {validCartItems.length === 0 ? (
            <p className="empty-cart-message">Your cart is empty.</p>
          ) : (
            <ul className="cart-items-list">
              {validCartItems.map(({ book, quantity }) => (
                <li key={book._id} className="cart-item">
                  <img src={book.coverUrl} alt={book.title} className="cart-item-img" />
                  <div className="cart-item-details">
                    <h4>{book.title}</h4>
                    <p>Price: ₹{book.price ? book.price.toFixed(2) : 'N/A'}</p>
                    <div className="quantity-control">
                      <label htmlFor={`quantity-${book._id}`}>Qty:</label>
                      <input
                        type="number"
                        id={`quantity-${book._id}`}
                        className="quantity-input"
                        value={quantity}
                        onChange={(e) => handleUpdateQuantity(book._id, e.target.value)}
                        min="1"
                      />
                    </div>
                  </div>
                  <button onClick={() => handleRemove(book._id)} className="cart-remove-btn">Remove</button>
                </li>
              ))}
            </ul>
          )}
        </div>
        {validCartItems.length > 0 && (
          <div className="cart-footer">
            <h3>Total: ₹{totalPrice.toFixed(2)}</h3>
            {/* 4. Update the button's onClick handler */}
            <button className="checkout-btn" onClick={handleCheckout}>Proceed to Checkout</button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Cart;

