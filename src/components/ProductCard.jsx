import React, { useState } from 'react';
import { useShop } from '../context/ShopContext';
import { Heart, Eye, ShoppingBag } from 'lucide-react';
import { MetalPurityBadge } from './MetalPurityBadge';

export const ProductCard = ({ product, variant = 'default', isSquare = false }) => {
  const isSquareCard = variant === 'square' || isSquare;
  const { addToCart, toggleWishlist, isInWishlist, setQuickViewProduct } = useShop();
  // Accurately determine initial hallmark metal stamp for this specific piece
  const nameLower = (product.name || '').toLowerCase();
  const puritySpec = (product.specs?.['Metal Purity'] || '').toLowerCase();

  const defaultMetal =
    product.metalType === 'gold'
      ? '18K Yellow Gold'
      : product.metalType === 'rose'
      ? 'Rose Gold Plated'
      : product.metalType === 'silver'
      ? 'Pure 925 Silver'
      : product.metals && product.metals.length
      ? product.metals[0]
      : (nameLower.includes('gold') || nameLower.includes('golden') || nameLower.includes('vermeil') || puritySpec.includes('gold'))
      ? '18K Yellow Gold'
      : (nameLower.includes('rose') || puritySpec.includes('rose'))
      ? 'Rose Gold Plated'
      : 'Pure 925 Silver';

  const [selectedMetal, setSelectedMetal] = useState(defaultMetal);
  const [isHovered, setIsHovered] = useState(false);

  React.useEffect(() => {
    setSelectedMetal(defaultMetal);
  }, [product.id, defaultMetal]);

  const isWishlisted = isInWishlist(product.id);
  const primaryImage = product.images[0];
  const hoverImage = product.images.length > 1 ? product.images[1] : product.images[0];

  // Clean title: removes redundant "- 925 sterling silver" from titles since hallmark stamp is displayed right below
  const cleanTitle = (product.shortName || product.name || '')
    .replace(/\s*-\s*(925\s*)?(sterling\s*)?silver/gi, '')
    .replace(/\s*-\s*pure\s*silver/gi, '')
    .trim();

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

        {/* Bottom Content Bar - Compact Minimal Structure */}
        <div className="p-2 sm:p-2.5 bg-white border-t border-[#EAE4DC] shrink-0 flex flex-col justify-between gap-1">
          <div className="flex items-center justify-between gap-1">
            <h3 className="font-serif text-[11px] sm:text-xs font-semibold text-[#231F20] group-hover:text-[#7A152E] transition-colors truncate leading-snug">
              {cleanTitle}
            </h3>
            <div className="flex items-center gap-1 shrink-0">
              <MetalPurityBadge product={product} size="rating" selectedMetal={selectedMetal} />
              {product.discount ? (
                <span className="text-[#7A152E] font-bold text-[8.5px] sm:text-[9.5px] tracking-wide shrink-0">
                  {product.discount}
                </span>
              ) : product.badge ? (
                <span className="text-[#7A152E] font-semibold text-[8px] sm:text-[9px] uppercase tracking-wider shrink-0">
                  {product.badge}
                </span>
              ) : (
                <span className="text-stone-400 font-medium text-[8px] sm:text-[8.5px] uppercase tracking-wider shrink-0">
                  Certified
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center justify-between gap-1 pt-1 border-t border-stone-100">
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

            {/* Action Icons */}
            <div className="flex items-center gap-1 shrink-0">
              <button
                type="button"
                onClick={handleWishlistClick}
                className={`w-6 h-6 rounded-full flex items-center justify-center transition-all duration-200 cursor-pointer active:scale-90 border ${
                  isWishlisted
                    ? 'bg-rose-50 text-[#7A152E] border-[#7A152E]/30 ring-1 ring-[#7A152E]/20'
                    : 'bg-white text-stone-600 hover:text-[#7A152E] border-stone-200'
                }`}
                title={isWishlisted ? "In your Wishlist" : "Add to Wishlist"}
              >
                <Heart className={`w-3 h-3 ${isWishlisted ? 'fill-[#7A152E] stroke-[#7A152E]' : 'stroke-current fill-transparent'}`} />
              </button>
              <button
                type="button"
                onClick={handleAddToCart}
                className="w-6 h-6 rounded-full bg-[#7A152E] hover:bg-[#590D1E] text-white flex items-center justify-center shadow-2xs transition-all active:scale-90 cursor-pointer"
                title="Add to Bag"
              >
                <ShoppingBag className="w-3 h-3 text-white" strokeWidth={2} />
              </button>
            </div>
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
      {/* Visual Image Viewport - Grand Aspect 4:5 for Larger, Taller Showcase */}
      <div className="relative w-full aspect-[4/5] bg-[#FAF8F5] overflow-hidden">
        <img
          src={isHovered && hoverImage ? hoverImage : primaryImage}
          alt={product.name}
          className="w-full h-full object-cover object-center transition-all duration-500 group-hover:scale-105"
          loading="lazy"
        />

        {/* Subtle Quick View Overlay Pill on Desktop */}
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

      {/* Content - Precision Minimalist Container */}
      <div className="p-2.5 sm:p-3 flex flex-col justify-between gap-1.5 sm:gap-2 flex-1">
        {/* Title */}
        <h3 className="font-serif text-xs sm:text-[13.5px] font-semibold text-[#231F20] group-hover:text-[#7A152E] transition-colors truncate leading-snug">
          {cleanTitle}
        </h3>

        {/* Rating & Hallmark & Offer Badges Row */}
        <div className="flex items-center justify-between gap-1 sm:gap-1.5 w-full">
          <div className="flex items-center gap-1 sm:gap-1.5 shrink-0">
            {/* Rating Tag */}
            <div className="inline-flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] shadow-2xs shrink-0">
              <svg className="w-3 h-3 sm:w-3.5 sm:h-3.5 fill-[#C5A059] text-[#C5A059] shrink-0 drop-shadow-2xs" viewBox="0 0 24 24">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              <span className="font-sans font-bold text-[10.5px] sm:text-xs text-stone-900 leading-none">
                {product.rating}
              </span>
            </div>

            {/* Metal Purity Hallmark Badge */}
            <MetalPurityBadge product={product} size="rating" selectedMetal={selectedMetal} />
          </div>

          {/* Offer Tag */}
          {product.discount ? (
            <div className="inline-flex items-center justify-center text-center px-1.5 sm:px-2 py-0.5 rounded-lg bg-[#FAF0F2] border border-[#EAD5DA] text-[#7A152E] shadow-2xs shrink-0">
              <span className="font-sans font-bold text-[9.5px] sm:text-[10px] uppercase tracking-wide leading-none whitespace-nowrap">
                {product.discount}
              </span>
            </div>
          ) : product.badge ? (
            <div className="inline-flex items-center justify-center text-center px-1.5 sm:px-2 py-0.5 rounded-lg bg-[#FAF0F2] border border-[#EAD5DA] text-[#7A152E] shadow-2xs shrink-0">
              <span className="font-sans font-bold text-[9.5px] sm:text-[10px] uppercase tracking-wide leading-none whitespace-nowrap">
                {product.badge}
              </span>
            </div>
          ) : (
            <div className="inline-flex items-center justify-center text-center px-1.5 sm:px-2 py-0.5 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] text-stone-600 shadow-2xs shrink-0">
              <span className="font-sans font-medium text-[9px] sm:text-[9.5px] uppercase tracking-wide leading-none whitespace-nowrap">
                Certified
              </span>
            </div>
          )}
        </div>

        {/* Price & Action Icons Row */}
        <div className="pt-1.5 border-t border-[#EAE4DC]/80 flex items-center justify-between gap-1 mt-auto">
          {/* Price & Metal Swatches */}
          <div className="flex items-center gap-1.5 min-w-0">
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

            {/* Metal Swatches (only rendered when piece has multiple metal variants) */}
            {product.metals && product.metals.length > 1 && (
              <div className="hidden xs:flex items-center gap-1 shrink-0 ml-1">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedMetal('Pure 925 Silver');
                  }}
                  title="Pure 925 Sterling Silver"
                  className={`w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-slate-400 via-slate-100 to-slate-300 border shadow-2xs transition-all hover:scale-125 cursor-pointer ${
                    selectedMetal.toLowerCase().includes('silver')
                      ? 'ring-1.5 ring-slate-600 scale-115 border-slate-500'
                      : 'border-slate-400 opacity-70 hover:opacity-100'
                  }`}
                />
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedMetal('Rose Gold Plated');
                  }}
                  title="Rose Gold Plated"
                  className={`w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-[#B76E79] via-[#F5D8DE] to-[#D99BA5] border shadow-2xs transition-all hover:scale-125 cursor-pointer ${
                    selectedMetal.toLowerCase().includes('rose')
                      ? 'ring-1.5 ring-[#7A152E] scale-115 border-[#B76E79]'
                      : 'border-[#B76E79]/40 opacity-70 hover:opacity-100'
                  }`}
                />
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedMetal('18K Yellow Gold');
                  }}
                  title="18K Gold Vermeil"
                  className={`w-2.5 h-2.5 rounded-full bg-gradient-to-tr from-[#946A1E] via-[#F4E3BF] to-[#C99D46] border shadow-2xs transition-all hover:scale-125 cursor-pointer ${
                    selectedMetal.toLowerCase().includes('gold') && !selectedMetal.toLowerCase().includes('rose')
                      ? 'ring-1.5 ring-[#946A1E] scale-115 border-[#946A1E]'
                      : 'border-[#946A1E]/50 opacity-70 hover:opacity-100'
                  }`}
                />
              </div>
            )}
          </div>

          {/* Action Icons: Wishlist & Add to Bag side-by-side */}
          <div className="flex items-center gap-1.5 shrink-0">
            {/* Wishlist Button */}
            <button
              type="button"
              onClick={handleWishlistClick}
              className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center transition-all duration-200 cursor-pointer active:scale-90 border shadow-2xs hover:shadow-xs ${
                isWishlisted
                  ? 'bg-rose-50 text-[#7A152E] border-[#7A152E]/30 ring-1 ring-[#7A152E]/20'
                  : 'bg-white text-stone-600 hover:text-[#7A152E] hover:border-[#7A152E]/40 border-stone-200'
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

            {/* Add to Bag Icon Button */}
            <button
              type="button"
              onClick={handleAddToCart}
              className="w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center bg-[#7A152E] hover:bg-[#590D1E] text-white transition-all duration-200 cursor-pointer active:scale-90 shadow-2xs hover:shadow-xs group/cart"
              aria-label="Add to Bag"
              title="Add to Bag"
            >
              <ShoppingBag className="w-3.5 h-3.5 text-white/95 group-hover/cart:scale-110 transition-transform duration-200" strokeWidth={2} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
