E-Library: A Full-Stack MERN Application

A complete e-commerce bookstore application built from the ground up using the MERN (MongoDB, Express.js, React, Node.js) stack. This project simulates a real-world online store with features like secure user authentication, a dynamic shopping cart, and a full checkout process.

Features

Secure User Authentication: Full sign-up and login flow with password hashing (bcryptjs) and JWT for session management.

Bot Protection: Google reCAPTCHA v2 integrated into the sign-up form to prevent spam.

Dynamic Book Catalog: Browse and search a curated collection of books stored in a MongoDB database.

Persistent Shopping Cart: Add books to a cart, edit quantities, and remove items. The cart state is saved to the user's account.

Complete Checkout Flow: A "Buy Now" option for single items and a "Proceed to Checkout" for the entire cart, which adds purchased books to the user's permanent profile.

User Profile: A private page where users can view their information and a list of all books they have purchased.

Tech Stack

Frontend: React, React Router, CSS3

Backend: Node.js, Express.js

Database: MongoDB with Mongoose

Authentication: JSON Web Tokens (JWT), bcryptjs

Security: Google reCAPTCHA

Setup and Installation

To run this project locally, you will need to create two .env files (one for the client and one for the server) and run npm install in both directories.

Prerequisites

Node.js

npm

MongoDB (local or a cloud instance like MongoDB Atlas)

Backend Setup (server folder)

Navigate to the server directory: cd server

Install dependencies: npm install

Create a .env file in the server root and add the following variables:

MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret_key
RECAPTCHA_SECRET_KEY=your_google_recaptcha_secret_key


Start the server: npm start

Frontend Setup (client folder)

Navigate to the client directory: cd client

Install dependencies: npm install

Create a .env file in the client root and add your reCAPTCHA Site Key:

REACT_APP_RECAPTCHA_SITE_KEY=your_google_recaptcha_site_key


Start the client: npm start