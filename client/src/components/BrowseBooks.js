import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Gallery from './Gallery';

function BrowseBooks() {
  const [searchParams, setSearchParams] = useSearchParams();
  const query = searchParams.get('q') || '';

  // State to hold the complete list of books from the server
  const [allBooks, setAllBooks] = useState([]);
  // State for the search input field
  const [inputValue, setInputValue] = useState(query);
  // State for loading status
  const [loading, setLoading] = useState(true);

  // Effect to fetch all books from the API when the component first loads
  useEffect(() => {
    const fetchAllBooks = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/books');
        const data = await response.json();
        setAllBooks(data);
      } catch (error) {
        console.error("Failed to fetch books:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAllBooks();
  }, []); // Empty dependency array means this runs only once on mount

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchParams({ q: inputValue });
  };

  // Filter the live data from the server, not the old local file
  const filteredBooks = query
    ? allBooks.filter(book =>
        book.title.toLowerCase().includes(query.toLowerCase()) ||
        book.author.toLowerCase().includes(query.toLowerCase())
      )
    : []; // Show nothing if there is no search query

  return (
    <>
      <div className="main-content">
        <h2 id="bookTitle">Search Our Collection</h2>

        <form className="search-container" onSubmit={handleSearch}>
          <input 
            type="text" 
            className="search-input" 
            placeholder="Search for a book, author, or genre..." 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
          <button type="submit" className="search-button">Search</button>
        </form>

        {/* Conditionally render based on loading and search query */}
        <div className='books'>
          {loading ? (
            <p className="loading-container">Loading...</p>
          ) : (
            query && <Gallery books={filteredBooks} />
          )}
        </div>
      </div>

      <footer className="footer">
        <p>&copy; 2025 E-Library. All Rights Reserved.</p>
      </footer>
    </>
  );
}

export default BrowseBooks;
