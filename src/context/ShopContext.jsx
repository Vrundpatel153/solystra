import React, { createContext, useContext, useState, useEffect } from 'react';
import { PRODUCTS, PROMO_CODES } from '../data/catalog';

const ShopContext = createContext();

export const useShop = () => {
  const context = useContext(ShopContext);
  if (!context) {
    throw new Error('useShop must be used within a ShopProvider');
  }
  return context;
};

export const ShopProvider = ({ children }) => {
  // Cart state persisted to localStorage
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('aurelia_cart');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  // Wishlist state persisted to localStorage
  const [wishlist, setWishlist] = useState(() => {
    try {
      const saved = localStorage.getItem('aurelia_wishlist');
      return saved ? JSON.parse(saved) : [];
    } catch (e) {
      return [];
    }
  });

  // Drawers & Modals
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isWishlistOpen, setIsWishlistOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [quickViewProduct, setQuickViewProduct] = useState(null);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [isOrderSuccessOpen, setIsOrderSuccessOpen] = useState(false);
  const [lastOrder, setLastOrder] = useState(null);
  const [isGiftPackagingAdded, setIsGiftPackagingAdded] = useState(true);

  // Promo Code
  const [appliedCoupon, setAppliedCoupon] = useState(null);

  // Toasts
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    try {
      localStorage.setItem('aurelia_cart', JSON.stringify(cart));
    } catch (e) {}
  }, [cart]);

  useEffect(() => {
    try {
      localStorage.setItem('aurelia_wishlist', JSON.stringify(wishlist));
    } catch (e) {}
  }, [wishlist]);

  // Toast dispatcher
  const showToast = (message, type = 'success') => {
    const id = Date.now() + Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3500);
  };

  const removeToast = (id) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  // Cart operations
  const addToCart = (product, metal = 'Pure 925 Silver', size = null, engraving = '', quantity = 1) => {
    const variantKey = `${product.id}__${metal}__${size || 'std'}__${engraving || 'none'}`;
    
    setCart(prev => {
      const existing = prev.find(item => item.variantKey === variantKey);
      if (existing) {
        return prev.map(item => 
          item.variantKey === variantKey
            ? { ...item, quantity: item.quantity + quantity }
            : item
        );
      }
      return [
        ...prev,
        {
          variantKey,
          id: product.id,
          name: product.name,
          shortName: product.shortName || product.name,
          sku: product.sku,
          price: product.price,
          mrp: product.mrp,
          image: product.images[0],
          metal,
          size,
          engraving,
          quantity
        }
      ];
    });

    showToast(`Added "${product.shortName || product.name}" to your luxury shopping bag!`);
    setIsCartOpen(true);
  };

  const removeFromCart = (variantKey) => {
    setCart(prev => prev.filter(item => item.variantKey !== variantKey));
    showToast('Item removed from shopping bag', 'info');
  };

  const updateQuantity = (variantKey, delta) => {
    setCart(prev => prev.map(item => {
      if (item.variantKey === variantKey) {
        const newQty = item.quantity + delta;
        return newQty > 0 ? { ...item, quantity: newQty } : null;
      }
      return item;
    }).filter(Boolean));
  };

  const clearCart = () => {
    setCart([]);
  };

  // Wishlist operations
  const toggleWishlist = (productId) => {
    setWishlist(prev => {
      const exists = prev.includes(productId);
      if (exists) {
        showToast('Removed from your wishlist', 'info');
        return prev.filter(id => id !== productId);
      } else {
        const prod = PRODUCTS.find(p => p.id === productId);
        showToast(`Saved "${prod ? prod.shortName : 'Piece'}" to your wishlist!`);
        return [...prev, productId];
      }
    });
  };

  const isInWishlist = (productId) => wishlist.includes(productId);

  // Coupon code
  const applyCoupon = (code) => {
    const cleanCode = (code || '').trim().toUpperCase();
    if (PROMO_CODES[cleanCode]) {
      setAppliedCoupon({ code: cleanCode, ...PROMO_CODES[cleanCode] });
      showToast(`Promo "${cleanCode}" applied! ${PROMO_CODES[cleanCode].label}`);
      return { success: true };
    } else {
      showToast('Invalid promotional code. Try AUR10 or GOLD500', 'info');
      return { success: false, error: 'Invalid coupon code' };
    }
  };

  const removeCoupon = () => {
    setAppliedCoupon(null);
    showToast('Promo code removed', 'info');
  };

  // Calculations
  const cartItemCount = cart.reduce((total, item) => total + item.quantity, 0);
  const cartSubtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
  const cartMrpTotal = cart.reduce((total, item) => total + (item.mrp * item.quantity), 0);
  const totalSavings = cartMrpTotal - cartSubtotal;

  let discountAmount = 0;
  if (appliedCoupon) {
    if (appliedCoupon.discountPercent) {
      discountAmount = Math.round((cartSubtotal * appliedCoupon.discountPercent) / 100);
    } else if (appliedCoupon.discountAmount) {
      discountAmount = Math.min(appliedCoupon.discountAmount, cartSubtotal);
    }
  }

  const freeShippingThreshold = 999;
  const isFreeShipping = cartSubtotal >= freeShippingThreshold || cartSubtotal === 0;
  const shippingFee = isFreeShipping ? 0 : 150;
  const cartTotal = Math.max(0, cartSubtotal - discountAmount + shippingFee);

  const startCheckout = () => {
    if (cart.length === 0) {
      showToast('Your luxury shopping bag is currently empty', 'info');
      return;
    }
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
    if (window.location.hash !== '#/checkout') {
      window.location.hash = '#/checkout';
    }
  };

  return (
    <ShopContext.Provider value={{
      PRODUCTS,
      cart,
      wishlist,
      cartItemCount,
      cartSubtotal,
      cartMrpTotal,
      totalSavings,
      discountAmount,
      appliedCoupon,
      shippingFee,
      cartTotal,
      freeShippingThreshold,
      isFreeShipping,
      isCartOpen,
      setIsCartOpen,
      isWishlistOpen,
      setIsWishlistOpen,
      isSearchOpen,
      setIsSearchOpen,
      quickViewProduct,
      setQuickViewProduct,
      isCheckoutOpen,
      setIsCheckoutOpen,
      isOrderSuccessOpen,
      setIsOrderSuccessOpen,
      lastOrder,
      setLastOrder,
      isGiftPackagingAdded,
      setIsGiftPackagingAdded,
      startCheckout,
      toasts,
      showToast,
      removeToast,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      toggleWishlist,
      isInWishlist,
      applyCoupon,
      removeCoupon
    }}>
      {children}
    </ShopContext.Provider>
  );
};
