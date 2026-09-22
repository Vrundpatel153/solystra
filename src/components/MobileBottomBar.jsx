import React, { useState, useEffect } from 'react';
import { useShop } from '../context/ShopContext';
import { Compass, Tag, Heart, ShoppingBag, MapPin } from 'lucide-react';

export const MobileBottomBar = ({ onOpenBoutique }) => {
  const { cartItemCount, wishlist, setIsWishlistOpen, setIsCartOpen } = useShop();
  const [currentHash, setCurrentHash] = useState(() => window.location.hash || '');

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentHash(window.location.hash || '');
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const isExploreActive = currentHash === '#/products' || currentHash === '#/catalog' || currentHash === '#/explore';
  const isOffersActive = currentHash === '#/offers';
  const isProductDetailPage = currentHash.startsWith('#/product/') || window.location.pathname.startsWith('/product/');

  // Hide bottom navigation bar on product detail page to allow sticky Buy Now / Add to Cart CTA popup
  if (isProductDetailPage) {
    return null;
  }

  return (
    <div className="fixed bottom-3 left-3 right-3 sm:left-6 sm:right-6 max-w-md mx-auto z-40 lg:hidden">
      <nav
        aria-label="Mobile Navigation Bar"
        className="backdrop-blur-2xl bg-[#FAF8F5]/90 supports-[backdrop-filter]:bg-[#FAF8F5]/82 border border-white/80 shadow-[0_12px_36px_rgba(0,0,0,0.14)] rounded-full px-2 py-1.5 flex items-center justify-around transition-all"
      >
        {/* Tab 1: Explore / All Products Catalog */}
        <button
          onClick={() => {
            window.location.hash = '#/products';
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
          className={`flex flex-col items-center justify-center py-1 px-2.5 active:scale-95 transition-all group cursor-pointer ${
            isExploreActive ? 'text-[#7A152E]' : 'text-stone-700 hover:text-[#7A152E]'
          }`}
        >
          <Compass className={`w-5 h-5 transition-colors ${
            isExploreActive ? 'stroke-[#7A152E] stroke-[2.2]' : 'stroke-[1.75] group-hover:stroke-[#7A152E]'
          }`} />
          <span className={`text-[10.5px] tracking-tight mt-0.5 ${
            isExploreActive ? 'font-bold text-[#7A152E]' : 'font-medium text-stone-600 group-hover:text-[#7A152E]'
          }`}>
            Explore
          </span>
        </button>

        {/* Tab 2: Dedicated Offers Vault */}
        <button
          onClick={() => {
            window.location.hash = '#/offers';
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}
          className={`relative flex flex-col items-center justify-center py-1 px-2.5 active:scale-95 transition-all group cursor-pointer ${
            isOffersActive ? 'text-[#7A152E]' : 'text-stone-700 hover:text-[#7A152E]'
          }`}
        >
          <Tag className={`w-5 h-5 transition-colors ${
            isOffersActive ? 'stroke-[#7A152E] stroke-[2.2]' : 'stroke-[1.75] group-hover:stroke-[#7A152E]'
          }`} />
          <span className={`text-[10.5px] tracking-tight mt-0.5 ${
            isOffersActive ? 'font-bold text-[#7A152E]' : 'font-medium text-stone-600 group-hover:text-[#7A152E]'
          }`}>
            Offers
          </span>
        </button>

        {/* Tab 3: Wishlist */}
        <button
          onClick={() => setIsWishlistOpen(true)}
          className="relative flex flex-col items-center justify-center py-1 px-2.5 text-stone-700 hover:text-[#7A152E] active:scale-95 transition-all group cursor-pointer"
        >
          <div className="relative">
            <Heart className="w-5 h-5 stroke-[1.75] group-hover:stroke-[#7A152E] transition-colors" />
            {wishlist.length > 0 && (
              <span className="absolute -top-1 -right-2 bg-[#7A152E] text-white text-[9px] font-bold w-3.5 h-3.5 rounded-full flex items-center justify-center shadow-xs">
                {wishlist.length}
              </span>
            )}
          </div>
          <span className="text-[10px] font-medium tracking-tight mt-0.5 text-stone-600 group-hover:text-[#7A152E]">
            Wishlist
          </span>
        </button>

        {/* Tab 4: Cart / Bag */}
        <button
          onClick={() => setIsCartOpen(true)}
          className="relative flex flex-col items-center justify-center py-1 px-2.5 text-stone-700 hover:text-[#7A152E] active:scale-95 transition-all group cursor-pointer"
        >
          <div className="relative">
            <ShoppingBag className="w-5 h-5 stroke-[1.75] group-hover:stroke-[#7A152E] transition-colors" />
            {cartItemCount > 0 && (
              <span className="absolute -top-1 -right-2 bg-[#7A152E] text-white text-[9px] font-bold w-3.5 h-3.5 rounded-full flex items-center justify-center shadow-xs">
                {cartItemCount}
              </span>
            )}
          </div>
          <span className="text-[10px] font-medium tracking-tight mt-0.5 text-stone-600 group-hover:text-[#7A152E]">
            Bag {cartItemCount > 0 ? `(${cartItemCount})` : ''}
          </span>
        </button>

        {/* Tab 5: Boutiques */}
        <button
          onClick={onOpenBoutique}
          className="flex flex-col items-center justify-center py-1 px-2.5 text-stone-700 hover:text-[#7A152E] active:scale-95 transition-all group cursor-pointer"
        >
          <MapPin className="w-5 h-5 stroke-[1.75] group-hover:stroke-[#7A152E] transition-colors" />
          <span className="text-[10px] font-medium tracking-tight mt-0.5 text-stone-600 group-hover:text-[#7A152E]">
            Ateliers
          </span>
        </button>
      </nav>
    </div>
  );
};
