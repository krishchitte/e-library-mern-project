import { useState } from "react";
import { useCart } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

export default function Gallery({ books }) {
  const [expandedIndex, setExpandedIndex] = useState(null);
  const { setCartItems } = useCart();
  const navigate = useNavigate();

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const handleAddToCart = async (e, bookId) => {
    e.stopPropagation();
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in to add items to your cart.');
      navigate('/login');
      return;
    }
    try {
      const response = await fetch(`http://localhost:5000/api/cart/add/${bookId}`, {
        method: 'POST',
        headers: { 'x-auth-token': token },
      });
      const data = await response.json();
      if (response.ok) {
        setCartItems(data.items);
        alert('Book added to cart!');
      } else {
        throw new Error(data.msg || 'Failed to add to cart');
      }
    } catch (error) {
      console.error("Error adding to cart:", error);
      alert(error.message);
    }
  };
  
  const handleBuyNow = (e, book) => {
    e.stopPropagation();
    const token = localStorage.getItem('token');
    if (!token) {
      alert('Please log in to purchase a book.');
      navigate('/login');
    } else {
      navigate('/payment', { state: { book } });
    }
  };

  if (!books || books.length === 0) {
    return <p className="no-results">No books found.</p>;
  }

  return (
    <div className="gallery-wrapper">
      {/* Overlay for expanded card */}
      {expandedIndex !== null && books[expandedIndex] && (
        <div className="overlay" onClick={() => setExpandedIndex(null)}>
          <div className="book-card expanded" onClick={(e) => e.stopPropagation()}>
            <div className="book-inner">
              <img src={books[expandedIndex].coverUrl} alt={books[expandedIndex].title} className="book-cover" />
              <div className="book-details">
                <h3>{books[expandedIndex].title}</h3>
                <p className="author">by {books[expandedIndex].author}</p>
                {/* Defensive check for price */}
                <p className="book-price-expanded">
                  {books[expandedIndex].price ? `Price: ₹${books[expandedIndex].price.toFixed(2)}` : 'Price not available'}
                </p>
                <p className="description">{books[expandedIndex].description}</p>
                <button onClick={() => setExpandedIndex(null)}>Close</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Gallery grid */}
      <div className="gallery">
        {books.map((book, idx) => (
          <div className="book-card" key={book._id || idx} onClick={() => toggleExpand(idx)}>
            <div className="book-inner">
              <img src={book.coverUrl} alt={book.title} className="book-cover" />
              <div className="book-details">
                <h3>{book.title}</h3>
                <p className="author">by {book.author}</p>
                {/* Defensive check for price */}
                <p className="book-price">
                  {book.price ? `₹${book.price.toFixed(2)}` : 'Price N/A'}
                </p>
                <div className="book-actions">
                  <button onClick={(e) => handleAddToCart(e, book._id)}>Add to Cart</button>
                  <button className="buy-now-btn" onClick={(e) => handleBuyNow(e, book)}>Buy Now</button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}