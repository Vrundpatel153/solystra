import React from 'react';
import { useShop } from '../context/ShopContext';
import { X, Heart, ShoppingBag, Trash2 } from 'lucide-react';

export const WishlistDrawer = () => {
  const {
    wishlist,
    isWishlistOpen,
    setIsWishlistOpen,
    PRODUCTS,
    toggleWishlist,
    addToCart
  } = useShop();

  if (!isWishlistOpen) return null;

  const wishlistProducts = PRODUCTS.filter(p => wishlist.includes(p.id));

  return (
    <div className="fixed inset-0 z-50 overflow-hidden font-sans">
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
        onClick={() => setIsWishlistOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-white shadow-2xl flex flex-col border-l border-[#E8E5DF]">
          
          <div className="p-5 border-b border-[#E8E5DF] flex items-center justify-between bg-[#FAF8F5]">
            <div className="flex items-center gap-2">
              <Heart className="w-5 h-5 text-[#7A152E] fill-[#7A152E]" />
              <h2 className="font-serif text-lg font-bold text-[#111111] tracking-wide">
                Your Wishlist ({wishlist.length})
              </h2>
            </div>
            <button
              onClick={() => setIsWishlistOpen(false)}
              className="p-1.5 rounded-full hover:bg-black/5 text-[#717171] hover:text-[#111111] transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-5 divide-y divide-[#E8E5DF]">
            {wishlistProducts.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 text-[#717171] space-y-4">
                <div className="w-16 h-16 rounded-full bg-[#FAF8F5] flex items-center justify-center text-[#7A152E] border border-[#E8E5DF]">
                  <Heart className="w-8 h-8 opacity-70" />
                </div>
                <div className="font-serif text-lg font-semibold text-[#111111]">No Favorites Saved Yet</div>
                <p className="text-xs text-[#717171] max-w-xs">
                  Tap the heart icon on any jewelry piece to save it to your wishlist.
                </p>
                <button
                  onClick={() => setIsWishlistOpen(false)}
                  className="px-6 py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-widest font-semibold rounded-lg hover:bg-[#590D1E] transition-all shadow-sm"
                >
                  Discover Pieces
                </button>
              </div>
            ) : (
              wishlistProducts.map(product => (
                <div key={product.id} className="py-4 flex gap-4 items-center">
                  <div
                    className="w-20 h-20 rounded-lg overflow-hidden bg-[#FAF8F5] border border-[#E8E5DF] shrink-0 cursor-pointer"
                    onClick={() => {
                      setIsWishlistOpen(false);
                      window.location.hash = `#/product/${product.id}`;
                    }}
                  >
                    <img
                      src={product.images[0]}
                      alt={product.name}
                      className="w-full h-full object-cover hover:scale-105 transition-transform"
                    />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div
                      className="font-serif text-sm font-semibold text-[#111111] truncate cursor-pointer hover:text-[#7A152E] transition-colors"
                      onClick={() => {
                        setIsWishlistOpen(false);
                        window.location.hash = `#/product/${product.id}`;
                      }}
                    >
                      {product.shortName || product.name}
                    </div>

                    <div className="font-serif text-sm font-bold text-[#7A152E] mt-1">
                      ₹{product.price.toLocaleString('en-IN')}
                    </div>

                    <div className="flex items-center gap-2 mt-2">
                      <button
                        onClick={() => {
                          addToCart(product);
                          toggleWishlist(product.id);
                        }}
                        className="px-3 py-1 bg-[#7A152E] text-white text-[11px] uppercase tracking-wider font-semibold rounded hover:bg-[#590D1E] transition-colors flex items-center gap-1 shadow-sm"
                      >
                        <ShoppingBag className="w-3 h-3" /> Move to Bag
                      </button>

                      <button
                        onClick={() => toggleWishlist(product.id)}
                        className="p-1 text-[#717171] hover:text-[#7A152E] transition-colors"
                        aria-label="Remove from wishlist"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
