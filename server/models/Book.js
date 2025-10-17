const mongoose = require('mongoose');

const BookSchema = new mongoose.Schema({
  title: { type: String, required: true },
  author: { type: String, required: true },
  description: { type: String, required: true },
  summary: { type: String, required: true },
  coverUrl: { type: String, required: true },
  price: { type: Number, required: true },
});

module.exports = mongoose.model('Book', BookSchema);