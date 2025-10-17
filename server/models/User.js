const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  email: {
    type: String,
    required: true,
    unique: true,
  },
  password: {
    type: String,
    required: true,
  },
  purchasedBooks: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Book', // This creates a relationship with the Book model
  }],
});

module.exports = mongoose.model('User', UserSchema);