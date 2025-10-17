import React, { useState, useEffect } from 'react';
import Gallery from './Gallery';

function Home() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        // Fetch books from your backend API
        const response = await fetch('http://localhost:5000/api/books');
        const data = await response.json();
        setBooks(data);
      } catch (error) {
        console.error("Failed to fetch books:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []); // The empty array ensures this runs only once when the component mounts

  return (
    <>
      <div className="hero-section">
        <div className="hero-content">
          <h1>Welcome to Your E-Library</h1>
          <p>Discover your next favorite book from our vast collection.</p>
        </div>
      </div>
      <div className="main-content">
        <h2 id="bookTitle">Our Collection</h2>
        <div className='books'>
          {loading ? (
            <p className="loading-container">Loading books...</p>
          ) : (
            <Gallery books={books} />
          )}
        </div>
      </div>
      <footer className="footer">
        <p>&copy; 2025 E-Library. All Rights Reserved.</p>
      </footer>
    </>
  );
}

export default Home;