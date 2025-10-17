const express = require('express');
// Ensure all local require statements have the .js extension
const auth = require('../middleware/auth.js');
const User = require('../models/User.js');
const Book = require('../models/Book.js');
const Cart = require('../models/Cart.js'); 
const router = express.Router();

// @route   GET api/users/profile
// @desc    Get logged in user profile
// @access  Private
router.get('/profile', auth, async (req, res) => {
  try {
    const user = await User.findById(req.user.id).select('-password').populate('purchasedBooks');
    if (!user) {
      return res.status(404).json({ msg: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST api/users/purchase/:bookId
// @desc    Purchase a single book (for "Buy Now")
// @access  Private
router.post('/purchase/:bookId', auth, async (req, res) => {
  try {
    const book = await Book.findById(req.params.bookId);
    if (!book) return res.status(404).json({ msg: 'Book not found' });

    const user = await User.findById(req.user.id);
    if (!user) return res.status(404).json({ msg: 'User not found' });
    
    if (user.purchasedBooks.includes(req.params.bookId)) {
      return res.json(user.purchasedBooks);
    }

    user.purchasedBooks.push(req.params.bookId);
    await user.save();

    res.json(user.purchasedBooks);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST api/users/checkout
// @desc    Purchase all items in the cart
// @access  Private
router.post('/checkout', auth, async (req, res) => {
  try {
    const userId = req.user.id;
    const user = await User.findById(userId);
    if (!user) return res.status(404).json({ msg: 'User not found' });
    
    const cart = await Cart.findOne({ user: userId });

    if (!cart || cart.items.length === 0) {
      return res.status(400).json({ msg: 'Your cart is empty.' });
    }

    cart.items.forEach(item => {
      if (!user.purchasedBooks.includes(item.book)) {
        user.purchasedBooks.push(item.book);
      }
    });

    cart.items = [];

    await user.save();
    await cart.save();

    const updatedUser = await User.findById(userId).select('-password').populate('purchasedBooks');
    res.json(updatedUser);

  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;

