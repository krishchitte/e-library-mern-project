import React, { createContext, useState, useContext } from 'react';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);

  // In a full app, you would fetch/update cart from your API here
  // For simplicity, we manage it in state for now.
  // We'll connect it to the API in the components themselves.

  const value = {
    cartItems,
    setCartItems,
  };

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
};