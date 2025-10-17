const express = require('express');
const Book = require('../models/Book');
const router = express.Router();

// @route   GET api/books
// @desc    Get all books
router.get('/', async (req, res) => {
  try {
    const books = await Book.find();
    res.json(books);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;