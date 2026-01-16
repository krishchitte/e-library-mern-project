const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const { connectDB, importData } = require('./seeder');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json()); // Allows us to accept JSON data in the body

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI)
  .then(async () => {
    console.log('MongoDB Connected to elibrary');

    await seedUser();
    await seedBooks();

    app.listen(PORT, () =>
      console.log(`Server running on port ${PORT}`)
    );
  })

// Define Routes
app.use('/api/auth', require('./routes/auth.js'));
app.use('/api/books', require('./routes/books.js'));
app.use('/api/users', require('./routes/users.js'));
app.use('/api/cart', require('./routes/cart.js'));

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server started on port ${PORT}`));

const startServer = async () => {
  await connectDB();
  await importData(); // ✅ always seed on startup

  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
};

startServer();