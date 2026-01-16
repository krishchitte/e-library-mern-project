const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const client = require('prom-client');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// =====================
// Middleware
// =====================
app.use(cors());
app.use(express.json());

// =====================
// Prometheus Metrics
// =====================
const register = new client.Registry();

// Collect default Node.js metrics
client.collectDefaultMetrics({
  register,
  prefix: 'elibrary_',
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.setHeader('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err.message);
  }
});

// =====================
// API Routes
// =====================
app.use('/api/auth', require('./routes/auth'));
app.use('/api/books', require('./routes/books'));
app.use('/api/users', require('./routes/users'));
app.use('/api/cart', require('./routes/cart'));

// =====================
// MongoDB Connection
// =====================
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    console.log('MongoDB Connected');
    app.listen(PORT, () =>
      console.log(`Server running on port ${PORT}`)
    );
  })
  .catch((err) => {
    console.error('Mongo connection error:', err.message);
    process.exit(1);
  });