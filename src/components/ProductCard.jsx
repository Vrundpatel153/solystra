import React, { useState } from 'react';
import { useShop } from '../context/ShopContext';
import { Heart, Eye } from 'lucide-react';

export const ProductCard = ({ product, variant = 'default', isSquare = false }) => {
  const isSquareCard = variant === 'square' || isSquare;
  const { addToCart, toggleWishlist, isInWishlist, setQuickViewProduct } = useShop();
  const [selectedMetal, setSelectedMetal] = useState('Pure 925 Silver');
  const [isHovered, setIsHovered] = useState(false);

  const isWishlisted = isInWishlist(product.id);
  const primaryImage = product.images[0];
  const hoverImage = product.images.length > 1 ? product.images[1] : product.images[0];

  // Clean title: removes redundant "- 925 sterling silver" from titles since hallmark stamp is displayed right below
  const cleanTitle = (product.shortName || product.name || '')
    .replace(/\s*-\s*(925\s*)?(sterling\s*)?silver/gi, '')
    .replace(/\s*-\s*pure\s*silver/gi, '')
    .trim();

  // Accurately determine hallmark metal stamp for this specific piece
  const nameLower = product.name?.toLowerCase() || '';
  const puritySpec = product.specs?.['Metal Purity']?.toLowerCase() || '';

  const metalStamp =
    nameLower.includes('rose') || puritySpec.includes('rose')
      ? 'Rose Gold'
      : (nameLower.includes('gold') || nameLower.includes('vermeil') || puritySpec.includes('gold') || puritySpec.includes('vermeil'))
      ? '18K Vermeil'
      : '925 Silver';

  const handleCardClick = (e) => {
    if (e.target.closest('button')) return;
    window.location.hash = `#/product/${product.id}`;
  };

  const handleAddToCart = (e) => {
    e.stopPropagation();
    addToCart(product, selectedMetal, product.category === 'rings' ? '12' : null, '', 1);
  };

  const handleQuickView = (e) => {
    e.stopPropagation();
    setQuickViewProduct(product);
  };

  const handleWishlistClick = (e) => {
    e.stopPropagation();
    toggleWishlist(product.id);
  };

  if (isSquareCard) {
    return (
      <div
        onClick={handleCardClick}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        className="group bg-white rounded-2xl border border-[#EAE4DC] overflow-hidden shadow-xs hover:shadow-xl hover:border-[#7A152E]/60 transition-all duration-300 flex flex-col cursor-pointer aspect-square relative w-full h-full"
      >
        {/* Visual Image Viewport - Flex 1 */}
        <div className="relative w-full flex-1 min-h-0 bg-[#FAF8F5] overflow-hidden">
          <img
            src={isHovered && hoverImage ? hoverImage : primaryImage}
            alt={product.name}
            className="w-full h-full object-cover object-center transition-all duration-500 group-hover:scale-105"
            loading="lazy"
          />

          {/* Clean Modern Luxury Badge */}
          <div className="absolute top-2 left-2 pointer-events-none z-10">
            {product.discount ? (
              <span className="px-1.5 sm:px-2 py-0.5 bg-[#7A152E] text-white font-sans text-[8.5px] sm:text-[9.5px] font-bold tracking-wide rounded-full shadow-xs">
                {product.discount}
              </span>
            ) : product.badge ? (
              <span className="px-1.5 sm:px-2 py-0.5 bg-white/95 backdrop-blur-xs text-[#7A152E] border border-[#7A152E]/30 font-sans text-[8.5px] sm:text-[9px] uppercase tracking-wider font-semibold rounded-full shadow-xs">
                {product.badge}
              </span>
            ) : null}
          </div>

          {/* Wishlist Heart Icon */}
          <button
            type="button"
            onClick={handleWishlistClick}
            className={`absolute top-2 right-2 w-6 h-6 sm:w-7 sm:h-7 rounded-full flex items-center justify-center transition-all duration-200 z-20 shadow-sm cursor-pointer active:scale-90 ${
              isWishlisted
                ? 'bg-white text-[#7A152E] ring-2 ring-[#7A152E]/30'
                : 'bg-white/95 text-stone-700 hover:text-[#7A152E] hover:bg-white border border-stone-200/70'
            }`}
            aria-label={isWishlisted ? "Remove from Wishlist" : "Add to Wishlist"}
            title={isWishlisted ? "In your Wishlist" : "Add to Wishlist"}
          >
            <Heart
              className={`w-3 h-3 sm:w-3.5 sm:h-3.5 transition-all duration-200 ${
                isWishlisted
                  ? 'fill-[#7A152E] stroke-[#7A152E] stroke-[2] scale-110'
                  : 'stroke-current stroke-[1.75] fill-transparent'
              }`}
            />
          </button>

          {/* Quick View Overlay Pill on Desktop */}
          <div className="absolute inset-x-0 bottom-2 hidden sm:flex justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 pointer-events-none z-10">
            <button
              type="button"
              onClick={handleQuickView}
              className="pointer-events-auto py-0.5 px-2.5 bg-white/95 hover:bg-[#7A152E] text-[#231F20] hover:text-white text-[10px] font-sans font-semibold rounded-full shadow-md flex items-center gap-1 border border-[#EAE4DC] transition-all cursor-pointer"
            >
              <Eye className="w-2.5 h-2.5" />
              <span>Quick View</span>
            </button>
          </div>
        </div>

        {/* Bottom Content Bar - Compact & Square Aligned */}
        <div className="p-2 sm:p-2.5 bg-white border-t border-[#EAE4DC] shrink-0 flex flex-col justify-between">
          <div className="flex items-center justify-between gap-1">
            <h3 className="font-serif text-[11px] sm:text-xs font-semibold text-[#231F20] group-hover:text-[#7A152E] transition-colors truncate leading-snug">
              {cleanTitle}
            </h3>
            <span className="text-[#7A152E] font-semibold text-[8.5px] sm:text-[9.5px] uppercase tracking-wider shrink-0">
              {metalStamp}
            </span>
          </div>

          <div className="mt-1 flex items-center justify-between gap-1 pt-1 border-t border-stone-100">
            <div className="flex items-baseline gap-1">
              <span className="font-serif text-xs sm:text-sm font-bold text-[#231F20]">
                ₹{product.price.toLocaleString('en-IN')}
              </span>
              {product.mrp && product.mrp > product.price && (
                <span className="text-[9px] sm:text-[10px] text-stone-400 line-through">
                  ₹{product.mrp.toLocaleString('en-IN')}
                </span>
              )}
            </div>

            <button
              type="button"
              onClick={handleAddToCart}
              className="px-2 sm:px-2.5 py-1 rounded-lg bg-[#7A152E] hover:bg-[#590D1E] text-white text-[10px] sm:text-[11px] font-medium flex items-center gap-1 shadow-xs transition-all active:scale-95 cursor-pointer shrink-0"
              title="Add to Bag"
            >
              <svg className="w-3 h-3 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <path d="M16 10a4 4 0 0 1-8 0" />
              </svg>
              <span>Add</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      onClick={handleCardClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="group bg-white rounded-2xl border border-[#EAE4DC] overflow-hidden shadow-xs hover:shadow-xl hover:border-[#7A152E]/60 transition-all duration-300 flex flex-col cursor-pointer h-full"
    >
      {/* Visual Image Viewport */}
      <div className="relative w-full aspect-square bg-[#FAF8F5] overflow-hidden">
        <img
          src={isHovered && hoverImage ? hoverImage : primaryImage}
          alt={product.name}
          className="w-full h-full object-cover object-center transition-all duration-500 group-hover:scale-105"
          loading="lazy"
        />

        {/* Clean Modern Luxury Badge - Single Minimal Pill */}
        <div className="absolute top-2 left-2 sm:top-2.5 sm:left-2.5 pointer-events-none z-10">
          {product.discount ? (
            <span className="px-2 py-0.5 bg-[#7A152E] text-white font-sans text-[9px] sm:text-[10px] font-bold tracking-wide rounded-full shadow-xs">
              {product.discount}
            </span>
          ) : product.badge ? (
            <span className="px-2 py-0.5 bg-white/95 backdrop-blur-xs text-[#7A152E] border border-[#7A152E]/30 font-sans text-[9px] sm:text-[9.5px] uppercase tracking-wider font-semibold rounded-full shadow-xs">
              {product.badge}
            </span>
          ) : null}
        </div>

        {/* Luxury Floating Wishlist Heart Icon */}
        <button
          type="button"
          onClick={handleWishlistClick}
          className={`absolute top-2 right-2 sm:top-2.5 sm:right-2.5 w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center transition-all duration-200 z-20 shadow-md cursor-pointer active:scale-90 ${
            isWishlisted
              ? 'bg-white text-[#7A152E] ring-2 ring-[#7A152E]/30 shadow-[#7A152E]/15'
              : 'bg-white/95 text-stone-700 hover:text-[#7A152E] hover:bg-white hover:shadow-lg hover:scale-105 border border-stone-200/70'
          }`}
          aria-label={isWishlisted ? "Remove from Wishlist" : "Add to Wishlist"}
          title={isWishlisted ? "In your Wishlist" : "Add to Wishlist"}
        >
          <Heart
            className={`w-3.5 h-3.5 transition-all duration-200 ${
              isWishlisted
                ? 'fill-[#7A152E] stroke-[#7A152E] stroke-[2] scale-110'
                : 'stroke-current stroke-[1.75] fill-transparent'
            }`}
          />
        </button>

        {/* Subtle Quick View Overlay Pill */}
        <div className="absolute inset-x-0 bottom-2.5 hidden sm:flex justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 pointer-events-none z-10">
          <button
            type="button"
            onClick={handleQuickView}
            className="pointer-events-auto py-1 px-3 bg-white/95 hover:bg-[#7A152E] text-[#231F20] hover:text-white text-[11px] font-sans font-semibold rounded-full shadow-md flex items-center gap-1.5 border border-[#EAE4DC] transition-all cursor-pointer transform translate-y-1 group-hover:translate-y-0"
          >
            <Eye className="w-3 h-3 stroke-[1.75]" />
            <span>Quick View</span>
          </button>
        </div>
      </div>

      {/* Content - Precision Aligned Flex Container */}
      <div className="p-2.5 sm:p-3.5 flex-1 flex flex-col justify-between">
        <div>
          {/* Title: Fixed height for 100% horizontal alignment across grid cards */}
          <div className="h-[2.5em] flex items-center">
            <h3 className="font-serif text-xs sm:text-sm font-semibold text-[#231F20] group-hover:text-[#7A152E] transition-colors line-clamp-2 leading-snug">
              {cleanTitle}
            </h3>
          </div>

          {/* Rating + Accurate Hallmark Metal Stamp (No Category text, No Review Count) */}
          <div className="flex items-center gap-1.5 mt-1.5 h-5 text-stone-600 font-sans">
            <div className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded bg-stone-100/90 text-stone-900 text-[10px] sm:text-[11px] font-bold">
              <span className="text-[#C5A059] text-[9px] leading-none">★</span>
              <span>{product.rating}</span>
            </div>
            <span className="text-stone-300">&bull;</span>
            <span className="text-[#7A152E] font-semibold text-[9.5px] sm:text-[11px] uppercase tracking-wider truncate">
              {metalStamp}
            </span>
          </div>
        </div>

        <div className="mt-2.5">
          {/* Price Row: Fixed height for perfect alignment across columns */}
          <div className="pt-1.5 border-t border-[#EAE4DC] flex items-center justify-between h-7">
            <div className="flex items-baseline gap-1">
              <span className="font-serif text-xs xs:text-sm sm:text-base font-bold text-[#231F20]">
                ₹{product.price.toLocaleString('en-IN')}
              </span>
              {product.mrp && product.mrp > product.price && (
                <span className="text-[9.5px] sm:text-[11px] text-[#766D6F] line-through">
                  ₹{product.mrp.toLocaleString('en-IN')}
                </span>
              )}
            </div>

            {/* Metal Swatches (Silver, Rose Gold, 18K Gold) */}
            <div className="hidden xs:flex items-center gap-1 sm:gap-1.5 shrink-0">
              <span title="Pure 925 Sterling Silver" className="w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-slate-400 via-slate-100 to-slate-300 border border-slate-400 shadow-2xs" />
              <span title="Rose Gold Plated" className="w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-[#B76E79] via-[#F5D8DE] to-[#D99BA5] border border-[#B76E79]/40 shadow-2xs" />
              <span title="18K Gold Vermeil" className="w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-[#946A1E] via-[#F4E3BF] to-[#C99D46] border border-[#946A1E]/50 shadow-2xs" />
            </div>
          </div>

          {/* Action Button: Single Full-Width Button without Ellipsis */}
          <div className="pt-1.5 mt-1 border-t border-[#EAE4DC]/80">
            <button
              type="button"
              onClick={handleAddToCart}
              className="w-full py-1.5 sm:py-2 px-2 sm:px-3 rounded-xl bg-[#7A152E] hover:bg-[#590D1E] text-white font-sans text-[11px] sm:text-xs font-semibold flex items-center justify-center gap-1.5 transition-all duration-200 cursor-pointer active:scale-[0.98] shadow-xs hover:shadow-md group/cart"
              title="Add to Cart"
            >
              <svg className="w-3.5 h-3.5 shrink-0 text-white/90 transition-transform duration-200 group-hover/cart:-translate-y-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" />
                <line x1="3" y1="6" x2="21" y2="6" />
                <path d="M16 10a4 4 0 0 1-8 0" />
              </svg>
              {/* Clean text: "Add" on mobile to guarantee ZERO ellipsis / truncation */}
              <span className="whitespace-nowrap font-medium tracking-wide">
                <span className="sm:hidden">Add</span>
                <span className="hidden sm:inline">Add to Bag</span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
