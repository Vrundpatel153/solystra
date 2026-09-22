import React, { useState } from 'react';
import { useShop } from '../context/ShopContext';
import { X, Heart, ShoppingBag, ArrowRight } from 'lucide-react';
import { MetalPurityBadge } from './MetalPurityBadge';
import { GoldShoppingBag } from './GoldShoppingBag';

export const QuickViewModal = () => {
  const { quickViewProduct, setQuickViewProduct, addToCart, toggleWishlist, isInWishlist } = useShop();
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [selectedMetal, setSelectedMetal] = useState('Pure 925 Silver');
  const [selectedSize, setSelectedSize] = useState('12');

  if (!quickViewProduct) return null;

  const product = quickViewProduct;
  const isWishlisted = isInWishlist(product.id);
  const isRing = product.category === 'rings';
  const sizes = ['10', '12', '14', '16', '18'];

  const handleAddToCart = () => {
    addToCart(product, selectedMetal, isRing ? selectedSize : null, '', 1);
    setQuickViewProduct(null);
  };

  const handleNavigateToPdp = () => {
    setQuickViewProduct(null);
    window.location.hash = `#/product/${product.id}`;
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-4xl rounded-2xl shadow-2xl border border-[#E8E5DF] overflow-hidden animate-slide-up relative">
        
        <button
          onClick={() => setQuickViewProduct(null)}
          className="absolute top-4 right-4 z-10 p-2 rounded-full bg-white/90 hover:bg-[#7A152E] text-[#111111] hover:text-white transition-all shadow-md"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2">
          {/* Gallery */}
          <div className="p-6 bg-[#FAF8F5] flex flex-col items-center justify-center border-b md:border-b-0 md:border-r border-[#E8E5DF]">
            <div className="w-full aspect-square rounded-xl overflow-hidden bg-white border border-[#E8E5DF] shadow-sm relative group mb-4">
              <img
                src={product.images[selectedImageIndex] || product.images[0]}
                alt={product.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              {/* Atelier Hallmark Seal */}
              <div className="absolute top-3 left-3 pointer-events-none z-10">
                <MetalPurityBadge product={product} size="md" />
              </div>
            </div>

            {product.images.length > 1 && (
              <div className="flex gap-2 overflow-x-auto max-w-full pb-1">
                {product.images.map((img, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedImageIndex(idx)}
                    className={`w-14 h-14 rounded-lg overflow-hidden border-2 transition-all ${
                      selectedImageIndex === idx ? 'border-[#7A152E] shadow-sm' : 'border-[#E8E5DF] opacity-70 hover:opacity-100'
                    }`}
                  >
                    <img src={img} alt="Angle" className="w-full h-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Details */}
          <div className="p-6 sm:p-8 flex flex-col justify-between space-y-5">
            <div>
              <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-[#7A152E] font-bold">
                <span>{product.categoryName}</span>
                <span>•</span>
                <span className="text-[#717171]">SKU: {product.sku}</span>
              </div>

              <h2 className="font-serif text-2xl font-bold text-[#111111] mt-1">
                {product.name}
              </h2>

              {/* Rating - NO STAR ICON */}
              <div className="flex items-center gap-2 mt-2 text-xs font-sans text-[#717171]">
                <span className="font-bold text-[#7A152E]">Rated {product.rating}</span>
                <span>•</span>
                <span>{product.reviewsCount} verified reviews</span>
              </div>

              {/* Pricing */}
              <div className="flex items-baseline gap-3 mt-4">
                <span className="font-serif text-3xl font-bold text-[#7A152E]">
                  ₹{product.price.toLocaleString('en-IN')}
                </span>
                {product.mrp && product.mrp > product.price && (
                  <>
                    <span className="text-sm text-[#717171] line-through">
                      ₹{product.mrp.toLocaleString('en-IN')}
                    </span>
                    <span className="px-2 py-0.5 bg-[#7A152E] text-white text-xs font-bold rounded">
                      {product.discount}
                    </span>
                  </>
                )}
              </div>

              {/* Color Selection */}
              <div className="mt-5">
                <label className="block text-xs uppercase tracking-wider font-semibold text-[#111111] mb-2">
                  Select Color: <span className="text-[#7A152E] font-bold">{selectedMetal}</span>
                </label>
                <div className="flex gap-2">
                  {['Pure 925 Silver', 'Rose Gold Plated', '18K Gold Vermeil'].map(metal => (
                    <button
                      key={metal}
                      onClick={() => setSelectedMetal(metal)}
                      className={`flex-1 py-2 px-2 text-xs rounded-xl border transition-all text-center cursor-pointer ${
                        selectedMetal === metal
                          ? 'border-[#7A152E] bg-[#FDF2F4] text-[#7A152E] font-bold shadow-2xs'
                          : 'border-[#E8E5DF] hover:border-[#7A152E]/50 text-[#111111]'
                      }`}
                    >
                      {metal.replace('Pure ', '').replace(' Plated', '').replace(' Vermeil', '')}
                    </button>
                  ))}
                </div>
              </div>

              {/* Size Picker (Responsive Row) */}
              {isRing && (
                <div className="mt-4">
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-xs uppercase tracking-wider font-semibold text-[#111111]">
                      Select Ring Size:
                    </label>
                    <span className="text-xs font-bold text-[#7A152E]">
                      Size {selectedSize}
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {sizes.map(size => (
                      <button
                        key={size}
                        onClick={() => setSelectedSize(size)}
                        className={`w-9 h-9 rounded-xl border text-xs font-bold transition-all cursor-pointer flex items-center justify-center active:scale-95 ${
                          selectedSize === size
                            ? 'bg-[#7A152E] text-white border-[#7A152E] shadow-2xs'
                            : 'border-[#E8E5DF] hover:border-[#7A152E] text-[#111111]'
                        }`}
                      >
                        {size}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="space-y-3 pt-4 border-t border-[#E8E5DF]">
              <div className="flex gap-3">
                <button
                  onClick={handleAddToCart}
                  className="flex-1 py-3.5 bg-[#7A152E] text-white font-serif text-xs uppercase tracking-widest font-bold rounded-xl hover:bg-[#590D1E] transition-all shadow-md flex items-center justify-center gap-2 group"
                >
                  <GoldShoppingBag className="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" />
                  <span className="leading-none">Add to Bag</span>
                </button>
                <button
                  onClick={() => toggleWishlist(product.id)}
                  className={`p-3.5 rounded-xl border transition-all ${
                    isWishlisted
                      ? 'bg-white border-[#7A152E] text-[#7A152E]'
                      : 'border-[#E8E5DF] hover:border-[#7A152E] text-[#111111]'
                  }`}
                  aria-label="Wishlist"
                >
                  <Heart className={`w-5 h-5 ${isWishlisted ? 'fill-[#7A152E]' : ''}`} />
                </button>
              </div>

              <button
                onClick={handleNavigateToPdp}
                className="w-full text-center text-xs uppercase tracking-widest font-semibold text-[#111111] hover:text-[#7A152E] transition-colors flex items-center justify-center gap-1.5 pt-1"
              >
                <span>View Full Product Details &amp; Specs</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
