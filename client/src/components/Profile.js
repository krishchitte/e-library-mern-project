import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Profile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/users/profile', {
          headers: { 'x-auth-token': token },
        });
        if (!response.ok) throw new Error('Failed to fetch profile');
        const data = await response.json();
        setUser(data);
      } catch (error) {
        console.error(error);
        // Handle token expiration or invalid token case
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]);

  if (loading) {
    return <div className="loading-container">Loading Profile...</div>;
  }

  if (!user) {
    return (
      <div className="form-container">
        <h2>Access Denied</h2>
        <p>Please log in to view your profile.</p>
        <Link to="/login" className="form-button" style={{ textDecoration: 'none' }}>Go to Login</Link>
      </div>
    );
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <img src=".\images\user.png" alt="User Avatar" className="profile-avatar" />
        <div className="profile-details">
          <h2>{user.name}</h2>
          <p><strong>Email:</strong> {user.email}</p>
        </div>
      </div>

      <div className="rented-books-section">
        <h3>My Purchased Books</h3>
        {user.purchasedBooks && user.purchasedBooks.length > 0 ? (
          <ul className="rented-books-list">
            {user.purchasedBooks.map(book => (
              <li key={book._id}>
                <div className="book-info">
                  <strong>{book.title}</strong> by {book.author}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>You have not purchased any books yet.</p>
        )}
      </div>
    </div>
  );
}

export default Profile;