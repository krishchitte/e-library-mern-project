const express = require('express');
const auth = require('../middleware/auth.js');
const Cart = require('../models/Cart.js');
const Book = require('../models/Book.js');
const router = express.Router();

// @route   GET api/cart
// @desc    Get user's shopping cart
// @access  Private
router.get('/', auth, async (req, res) => {
  try {
    const cart = await Cart.findOne({ user: req.user.id }).populate('items.book');
    if (!cart) {
      return res.json({ items: [] });
    }
    res.json(cart);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST api/cart/add/:bookId
// @desc    Add a book to the cart
// @access  Private
router.post('/add/:bookId', auth, async (req, res) => {
  try {
    const bookId = req.params.bookId;
    const userId = req.user.id;

    const book = await Book.findById(bookId);
    if (!book) return res.status(404).json({ msg: 'Book not found' });

    let cart = await Cart.findOne({ user: userId });

    if (!cart) {
      cart = new Cart({ user: userId, items: [] });
    }

    const itemIndex = cart.items.findIndex(item => item.book.toString() === bookId);

    if (itemIndex > -1) {
      cart.items[itemIndex].quantity += 1;
    } else {
      cart.items.push({ book: bookId, quantity: 1 });
    }

    await cart.save();
    const populatedCart = await cart.populate('items.book');
    res.json(populatedCart);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   PUT api/cart/update/:bookId
// @desc    Update quantity of a book in the cart
// @access  Private
router.put('/update/:bookId', auth, async (req, res) => {
  const { quantity } = req.body;
  const { bookId } = req.params;
  const userId = req.user.id;

  try {
    if (!quantity || quantity < 1) {
      return res.status(400).json({ msg: 'Quantity must be at least 1.' });
    }

    const cart = await Cart.findOne({ user: userId });
    if (!cart) {
      return res.status(404).json({ msg: 'Cart not found.' });
    }

    const itemIndex = cart.items.findIndex(item => item.book.toString() === bookId);

    if (itemIndex > -1) {
      cart.items[itemIndex].quantity = Number(quantity);
      await cart.save();
      const populatedCart = await cart.populate('items.book');
      res.json(populatedCart);
    } else {
      res.status(404).json({ msg: 'Book not found in cart.' });
    }
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});


// @route   DELETE api/cart/remove/:bookId
// @desc    Remove an item from the cart
// @access  Private
router.delete('/remove/:bookId', auth, async (req, res) => {
    try {
        const cart = await Cart.findOne({ user: req.user.id });
        if (!cart) return res.status(404).json({ msg: 'Cart not found' });

        cart.items = cart.items.filter(({ book }) => book.toString() !== req.params.bookId);

        await cart.save();
        const populatedCart = await cart.populate('items.book');
        res.json(populatedCart);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

module.exports = router;

