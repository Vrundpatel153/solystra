import React, { useState, useMemo } from 'react';
import { useShop } from '../context/ShopContext';
import { Search, X, ArrowUpRight } from 'lucide-react';

export const SearchModal = () => {
  const { isSearchOpen, setIsSearchOpen, PRODUCTS } = useShop();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredProducts = useMemo(() => {
    if (!searchTerm.trim() && selectedCategory === 'all') {
      return PRODUCTS.slice(0, 6);
    }

    return PRODUCTS.filter(product => {
      const matchesText = !searchTerm.trim() || 
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.desc.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.categoryName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (product.sku && product.sku.toLowerCase().includes(searchTerm.toLowerCase()));

      const matchesCat = selectedCategory === 'all' || product.category === selectedCategory;

      return matchesText && matchesCat;
    });
  }, [searchTerm, selectedCategory, PRODUCTS]);

  if (!isSearchOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/70 backdrop-blur-sm flex items-start justify-center pt-12 sm:pt-20 px-4 font-sans">
      <div className="bg-white w-full max-w-3xl rounded-2xl shadow-2xl border border-[#E8E5DF] overflow-hidden animate-slide-up">
        
        {/* Search Header Bar */}
        <div className="p-4 sm:p-6 border-b border-[#E8E5DF] flex items-center gap-3 bg-[#FAF8F5]">
          <Search className="w-5 h-5 text-[#7A152E] shrink-0" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search necklaces, solitaire rings, tennis bracelets, earrings..."
            className="flex-1 text-base sm:text-lg bg-transparent text-[#111111] placeholder-[#717171] focus:outline-none"
            autoFocus
          />
          {searchTerm && (
            <button
              onClick={() => setSearchTerm('')}
              className="p-1 rounded-full text-[#717171] hover:text-[#111111]"
            >
              <X className="w-5 h-5" />
            </button>
          )}
          <button
            onClick={() => setIsSearchOpen(false)}
            className="px-3 py-1.5 rounded-lg border border-[#E8E5DF] text-xs uppercase tracking-wider font-semibold text-[#111111] hover:bg-[#7A152E] hover:text-white transition-all"
          >
            ESC
          </button>
        </div>

        {/* Category Filter Pills */}
        <div className="px-6 py-3 border-b border-[#E8E5DF] flex items-center gap-2 overflow-x-auto text-xs">
          <span className="text-[#717171] uppercase tracking-wider shrink-0 font-medium">Filter:</span>
          {['all', 'necklaces', 'bracelets', 'earrings', 'rings', 'anklets'].map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-lg capitalize shrink-0 transition-all ${
                selectedCategory === cat
                  ? 'bg-[#7A152E] text-white font-bold shadow-sm'
                  : 'bg-[#FAF8F5] text-[#111111] border border-[#E8E5DF] hover:bg-[#7A152E]/10'
              }`}
            >
              {cat === 'all' ? 'All Catalog' : cat}
            </button>
          ))}
        </div>

        {/* Results */}
        <div className="max-h-[60vh] overflow-y-auto p-6 divide-y divide-[#E8E5DF]">
          <div className="text-xs uppercase tracking-widest text-[#7A152E] font-bold mb-3 flex items-center justify-between">
            <span>
              {searchTerm ? `Search Results (${filteredProducts.length})` : 'Curated Highlights'}
            </span>
            <span className="text-[#717171] font-normal">Instant Search</span>
          </div>

          {filteredProducts.length === 0 ? (
            <div className="py-12 text-center text-[#717171] space-y-2">
              <p className="font-serif text-lg text-[#111111]">No jewelry matches found</p>
              <p className="text-xs">Try searching for "Solitaire", "Bloom", "Tennis", or "Rings"</p>
            </div>
          ) : (
            filteredProducts.map(product => (
              <div
                key={product.id}
                onClick={() => {
                  setIsSearchOpen(false);
                  window.location.hash = `#/product/${product.id}`;
                }}
                className="py-3.5 flex items-center justify-between group cursor-pointer hover:bg-[#FAF8F5] -mx-3 px-3 rounded-xl transition-all"
              >
                <div className="flex items-center gap-4">
                  <div className="w-14 h-14 rounded-lg overflow-hidden bg-[#FAF8F5] border border-[#E8E5DF] shrink-0">
                    <img
                      src={product.images[0]}
                      alt={product.name}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform"
                    />
                  </div>
                  <div>
                    <div className="font-serif text-sm font-semibold text-[#111111] group-hover:text-[#7A152E] transition-colors">
                      {product.name}
                    </div>
                    <div className="flex items-center gap-2 mt-0.5 text-xs text-[#717171]">
                      <span className="capitalize">{product.categoryName}</span>
                      <span>•</span>
                      <span className="text-[#7A152E] font-bold">Rated {product.rating}</span>
                      <span>•</span>
                      <span className="text-[#111111] font-semibold">925 Silver</span>
                    </div>
                  </div>
                </div>

                <div className="text-right flex items-center gap-4">
                  <div>
                    <div className="font-serif text-sm font-bold text-[#7A152E]">
                      ₹{product.price.toLocaleString('en-IN')}
                    </div>
                    {product.mrp && product.mrp > product.price && (
                      <div className="text-[11px] text-[#717171] line-through">
                        ₹{product.mrp.toLocaleString('en-IN')}
                      </div>
                    )}
                  </div>
                  <div className="w-8 h-8 rounded-full bg-[#FAF8F5] border border-[#E8E5DF] flex items-center justify-center text-[#111111] group-hover:bg-[#7A152E] group-hover:text-white transition-all">
                    <ArrowUpRight className="w-4 h-4" />
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
