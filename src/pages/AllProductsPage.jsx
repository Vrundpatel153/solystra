import React, { useState, useMemo, useEffect } from 'react';
import { PRODUCTS } from '../data/catalog';
import { ProductCard } from '../components/ProductCard';
import { LuxurySortDropdown } from '../components/LuxurySortDropdown';
import {
  Search,
  SlidersHorizontal,
  X,
  ChevronDown,
  ArrowUpDown,
  ArrowLeft,
  RotateCcw,
  Check
} from 'lucide-react';

const CATEGORIES = [
  { id: 'all', label: 'All Designs' },
  { id: 'necklaces', label: 'Necklaces & Lariats' },
  { id: 'rings', label: 'Rings & Bands' },
  { id: 'earrings', label: 'Earrings & Studs' },
  { id: 'bracelets', label: 'Bracelets & Kadas' },
  { id: 'complete_sets', label: 'Gift Sets' },
  { id: 'bestseller', label: 'Bestsellers' }
];

const PRICE_TIERS = [
  { id: 'all', label: 'All Prices', min: 0, max: Infinity },
  { id: 'under-2500', label: 'Under ₹2,500', min: 0, max: 2500 },
  { id: '2500-5000', label: '₹2,500 – ₹5,000', min: 2500, max: 5000 },
  { id: '5000-8000', label: '₹5,000 – ₹8,000', min: 5000, max: 8000 },
  { id: 'above-8000', label: 'Above ₹8,000', min: 8000, max: Infinity }
];

const METALS = [
  { id: 'all', label: 'All Metals' },
  { id: 'silver', label: '925 Sterling Silver' },
  { id: 'gold', label: '18K Gold Vermeil' },
  { id: 'rose', label: 'Rose Gold Plated' }
];

const SORT_OPTIONS = [
  { id: 'featured', label: 'Featured' },
  { id: 'price-low', label: 'Price: Low to High' },
  { id: 'price-high', label: 'Price: High to Low' },
  { id: 'rating', label: 'Highest Rated' },
  { id: 'discount', label: 'Biggest Savings' }
];

export const AllProductsPage = ({ onBackToStore }) => {
  // Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPriceTier, setSelectedPriceTier] = useState('all');
  const [maxPriceSlider, setMaxPriceSlider] = useState(15000);
  const [selectedMetal, setSelectedMetal] = useState('all');
  const [sortBy, setSortBy] = useState('featured');
  const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);

  // Sync scroll to top on mount
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  // Lock body scroll when mobile filter drawer is open
  useEffect(() => {
    if (isMobileFilterOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isMobileFilterOpen]);

  // Active filter count
  const activeFilterCount = useMemo(() => {
    let count = 0;
    if (searchQuery.trim()) count++;
    if (selectedCategory !== 'all') count++;
    if (selectedPriceTier !== 'all') count++;
    if (maxPriceSlider < 15000) count++;
    if (selectedMetal !== 'all') count++;
    return count;
  }, [searchQuery, selectedCategory, selectedPriceTier, maxPriceSlider, selectedMetal]);

  // Reset all filters
  const handleResetFilters = () => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedPriceTier('all');
    setMaxPriceSlider(15000);
    setSelectedMetal('all');
    setSortBy('featured');
  };

  // Filter & Sort Logic
  const filteredProducts = useMemo(() => {
    return PRODUCTS.filter((product) => {
      // 1. Search filter
      if (searchQuery.trim()) {
        const query = searchQuery.toLowerCase().trim();
        const matchesName = product.name?.toLowerCase().includes(query);
        const matchesCategory = product.category?.toLowerCase().includes(query);
        const matchesDesc = product.desc?.toLowerCase().includes(query);
        const matchesSku = product.sku?.toLowerCase().includes(query);
        if (!matchesName && !matchesCategory && !matchesDesc && !matchesSku) {
          return false;
        }
      }

      // 2. Category filter
      if (selectedCategory !== 'all') {
        if (selectedCategory === 'bestseller') {
          if (product.badge?.toLowerCase() !== 'bestseller') return false;
        } else if (product.category !== selectedCategory) {
          return false;
        }
      }

      // 3. Quick Price Tier filter
      if (selectedPriceTier !== 'all') {
        const tier = PRICE_TIERS.find((t) => t.id === selectedPriceTier);
        if (tier) {
          if (product.price < tier.min || product.price > tier.max) {
            return false;
          }
        }
      }

      // 4. Slider max price filter
      if (maxPriceSlider < 15000 && product.price > maxPriceSlider) {
        return false;
      }

      // 5. Metal / Finish filter
      if (selectedMetal !== 'all') {
        if (selectedMetal === 'gold') {
          const hasGold = product.metals?.some((m) => m.toLowerCase().includes('gold'));
          if (!hasGold) return false;
        } else if (selectedMetal === 'rose') {
          const hasRose = product.metals?.some((m) => m.toLowerCase().includes('rose'));
          if (!hasRose) return false;
        } else if (selectedMetal === 'silver') {
          const hasSilver = product.metals?.some((m) => m.toLowerCase().includes('silver'));
          if (!hasSilver) return false;
        }
      }

      return true;
    }).sort((a, b) => {
      if (sortBy === 'price-low') return a.price - b.price;
      if (sortBy === 'price-high') return b.price - a.price;
      if (sortBy === 'rating') return (b.rating || 4.5) - (a.rating || 4.5);
      if (sortBy === 'discount') {
        const discountA = a.mrp && a.price ? (a.mrp - a.price) / a.mrp : 0;
        const discountB = b.mrp && b.price ? (b.mrp - b.price) / b.mrp : 0;
        return discountB - discountA;
      }
      // 'featured': maintain default catalog order
      return 0;
    });
  }, [searchQuery, selectedCategory, selectedPriceTier, maxPriceSlider, selectedMetal, sortBy]);

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] font-sans pb-20 lg:pb-14">
      
      {/* ========================================================
          1. EDITORIAL HEADER & SEARCH HERO
          ======================================================== */}
      <section className="bg-white border-b border-[#EAE4DC] pt-5 sm:pt-7 pb-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Top Breadcrumb & Purity Badge (Desktop Only, Hidden on Mobile) */}
          <div className="hidden sm:flex items-center justify-between pb-3 mb-4 border-b border-[#EAE4DC]">
            <button
              onClick={() => {
                if (onBackToStore) onBackToStore();
                else window.location.hash = '#/';
              }}
              className="inline-flex items-center gap-1.5 text-xs text-stone-500 hover:text-[#7A152E] font-medium transition-colors cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5 text-[#7A152E]" />
              <span>Back to Home</span>
            </button>

            <span className="text-[11px] uppercase tracking-wider text-[#7A152E] font-semibold">
              Certified 925 Silver &amp; 18K Gold
            </span>
          </div>

          <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h1 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal tracking-tight">
                All Handcrafted Creations
              </h1>
              <p className="text-xs sm:text-sm text-stone-500 mt-1 font-light">
                Filter by price, metal finish, or category with instant live search.
              </p>
            </div>

            {/* Live Search Input Bar */}
            <div className="relative w-full md:w-80 shrink-0">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-stone-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search rings, necklaces, 18K gold..."
                className="w-full pl-9 pr-9 py-2 sm:py-2.5 bg-[#FAF8F5] border border-[#EAE4DC] focus:border-[#7A152E] focus:bg-white rounded-xl text-xs sm:text-sm text-stone-900 placeholder:text-stone-400 outline-none transition-all shadow-2xs"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-700 cursor-pointer p-0.5"
                  aria-label="Clear search"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
          </div>

          {/* Category Pills Bar (Horizontal Swipeable on Mobile) */}
          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-2 mt-4 -mx-1 px-1">
            {CATEGORIES.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all cursor-pointer active:scale-95 ${
                  selectedCategory === cat.id
                    ? 'bg-[#7A152E] text-white shadow-xs font-semibold'
                    : 'bg-stone-100 hover:bg-stone-200/80 text-stone-700'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

        </div>
      </section>

      {/* ========================================================
          2. FILTER & SORT TOOLBAR (Sticky on Mobile)
          ======================================================== */}
      <section className="bg-white/95 backdrop-blur-md border-b border-[#EAE4DC] sticky top-[52px] sm:top-[62px] z-30 shadow-[0_2px_10px_rgba(0,0,0,0.02)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2.5">
          {/* Mobile & Tablet Toolbar: Premium 50/50 Symmetrical Action Bar */}
          <div className="grid grid-cols-2 gap-2.5 lg:hidden">
            {/* Filter Drawer Trigger */}
            <button
              onClick={() => setIsMobileFilterOpen(true)}
              className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl border border-[#EAE4DC] bg-[#FAF8F5] hover:bg-[#F5F0EA] active:scale-[0.98] text-xs font-semibold text-stone-800 shadow-2xs transition-all cursor-pointer"
            >
              <SlidersHorizontal className="w-3.5 h-3.5 text-[#7A152E]" />
              <span>Filters</span>
              {activeFilterCount > 0 && (
                <span className="w-4 h-4 rounded-full bg-[#7A152E] text-white text-[10px] font-bold flex items-center justify-center ml-0.5">
                  {activeFilterCount}
                </span>
              )}
            </button>

            {/* Sort Selector */}
            <LuxurySortDropdown
              value={sortBy}
              onChange={setSortBy}
              options={SORT_OPTIONS}
              isMobile={true}
            />
          </div>

          {/* Desktop Toolbar: Luxury Status Bar + Quick Price Pills & Sort Dropdown */}
          <div className="hidden lg:flex items-center justify-between gap-4">
            {/* Left: Luxury Collection Descriptor */}
            <div className="flex items-center gap-2 text-xs font-medium text-stone-600">
              <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
              <span className="tracking-wide">Curated Handcrafted Collection</span>
            </div>

            {/* Right: Quick Price Tier Pills + Sort Dropdown */}
            <div className="flex items-center gap-4">
              {/* Quick Price Tier Pills */}
              <div className="flex items-center gap-1.5">
                {PRICE_TIERS.map((tier) => (
                  <button
                    key={tier.id}
                    onClick={() => setSelectedPriceTier(tier.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs transition-all cursor-pointer ${
                      selectedPriceTier === tier.id
                        ? 'bg-[#7A152E] text-white font-semibold shadow-2xs'
                        : 'bg-stone-100/80 hover:bg-stone-200 text-stone-600'
                    }`}
                  >
                    {tier.label}
                  </button>
                ))}
              </div>

              {/* Sort Dropdown */}
              <div className="flex items-center gap-2 text-xs text-stone-600">
                <span className="text-stone-400 font-light">Sort:</span>
                <LuxurySortDropdown
                  value={sortBy}
                  onChange={setSortBy}
                  options={SORT_OPTIONS}
                  isMobile={false}
                />
              </div>
            </div>
          </div>

          {/* Active Filters Tag Strip */}
          {activeFilterCount > 0 && (
            <div className="flex flex-wrap items-center gap-1.5 pt-2.5 mt-2 border-t border-[#EAE4DC]/60">
              <span className="text-[11px] text-stone-400 mr-1">Active:</span>

              {searchQuery && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] bg-[#7A152E]/10 text-[#7A152E] border border-[#7A152E]/20">
                  Search: "{searchQuery}"
                  <button onClick={() => setSearchQuery('')} className="cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {selectedCategory !== 'all' && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] bg-[#7A152E]/10 text-[#7A152E] border border-[#7A152E]/20">
                  Category: {CATEGORIES.find((c) => c.id === selectedCategory)?.label}
                  <button onClick={() => setSelectedCategory('all')} className="cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {selectedPriceTier !== 'all' && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] bg-[#7A152E]/10 text-[#7A152E] border border-[#7A152E]/20">
                  Price: {PRICE_TIERS.find((t) => t.id === selectedPriceTier)?.label}
                  <button onClick={() => setSelectedPriceTier('all')} className="cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {maxPriceSlider < 15000 && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] bg-[#7A152E]/10 text-[#7A152E] border border-[#7A152E]/20">
                  Under ₹{maxPriceSlider.toLocaleString('en-IN')}
                  <button onClick={() => setMaxPriceSlider(15000)} className="cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              {selectedMetal !== 'all' && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] bg-[#7A152E]/10 text-[#7A152E] border border-[#7A152E]/20">
                  Metal: {METALS.find((m) => m.id === selectedMetal)?.label}
                  <button onClick={() => setSelectedMetal('all')} className="cursor-pointer">
                    <X className="w-3 h-3" />
                  </button>
                </span>
              )}

              <button
                onClick={handleResetFilters}
                className="text-[11px] text-[#7A152E] hover:underline font-semibold ml-auto cursor-pointer"
              >
                Clear All
              </button>
            </div>
          )}

        </div>
      </section>

      {/* ========================================================
          3. MAIN CONTENT: DESKTOP SIDEBAR + RESPONSIVE GRID
          ======================================================== */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8">
        <div className="flex gap-8 items-start">
          
          {/* Desktop Left Filter Sidebar (Hidden on mobile/tablet) */}
          <aside className="hidden lg:block w-64 shrink-0 space-y-6 bg-white p-5 rounded-2xl border border-[#EAE4DC] shadow-xs sticky top-[130px]">
            <div className="flex items-center justify-between pb-3 border-b border-[#EAE4DC]">
              <span className="font-serif text-base font-semibold text-stone-900 flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-[#7A152E]" />
                Filter Jewelry
              </span>
              {activeFilterCount > 0 && (
                <button
                  onClick={handleResetFilters}
                  className="text-xs text-[#7A152E] hover:underline font-medium cursor-pointer"
                >
                  Reset
                </button>
              )}
            </div>

            {/* Filter Group: Price Range Slider */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold uppercase tracking-wider text-stone-800">
                  Max Budget
                </span>
                <span className="text-xs font-bold text-[#7A152E]">
                  ₹{maxPriceSlider.toLocaleString('en-IN')}
                </span>
              </div>
              <input
                type="range"
                min="1500"
                max="15000"
                step="500"
                value={maxPriceSlider}
                onChange={(e) => setMaxPriceSlider(Number(e.target.value))}
                className="w-full accent-[#7A152E] cursor-pointer"
              />
              <div className="flex justify-between text-[10.5px] text-stone-400 mt-1">
                <span>₹1,500</span>
                <span>₹15,000+</span>
              </div>
            </div>

            {/* Filter Group: Metal Purity */}
            <div className="pt-4 border-t border-[#EAE4DC]">
              <span className="text-xs font-bold uppercase tracking-wider text-stone-800 block mb-2.5">
                Metal / Polish
              </span>
              <div className="space-y-1.5">
                {METALS.map((metal) => (
                  <button
                    key={metal.id}
                    onClick={() => setSelectedMetal(metal.id)}
                    className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer ${
                      selectedMetal === metal.id
                        ? 'bg-[#7A152E]/10 text-[#7A152E] font-semibold'
                        : 'text-stone-600 hover:bg-stone-50'
                    }`}
                  >
                    <span>{metal.label}</span>
                    {selectedMetal === metal.id && (
                      <Check className="w-3.5 h-3.5 text-[#7A152E]" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Filter Group: Categories */}
            <div className="pt-4 border-t border-[#EAE4DC]">
              <span className="text-xs font-bold uppercase tracking-wider text-stone-800 block mb-2.5">
                Categories
              </span>
              <div className="space-y-1.5">
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => setSelectedCategory(cat.id)}
                    className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer ${
                      selectedCategory === cat.id
                        ? 'bg-[#7A152E]/10 text-[#7A152E] font-semibold'
                        : 'text-stone-600 hover:bg-stone-50'
                    }`}
                  >
                    <span>{cat.label}</span>
                    {selectedCategory === cat.id && (
                      <Check className="w-3.5 h-3.5 text-[#7A152E]" />
                    )}
                  </button>
                ))}
              </div>
            </div>

          </aside>

          {/* Right Product Grid */}
          <main className="flex-1 min-w-0">
            {filteredProducts.length > 0 ? (
              <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-5">
                {filteredProducts.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <div className="bg-white rounded-2xl border border-[#EAE4DC] p-10 sm:p-14 text-center max-w-md mx-auto my-8 shadow-xs">
                <div className="w-14 h-14 mx-auto rounded-full bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mb-4">
                  <Search className="w-6 h-6" />
                </div>
                <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-normal">
                  No Matching Jewels Found
                </h3>
                <p className="text-xs sm:text-sm text-stone-500 mt-2 font-light leading-relaxed">
                  We couldn't find pieces matching your exact combination of search and filters.
                </p>
                <button
                  onClick={handleResetFilters}
                  className="mt-5 px-5 py-2.5 bg-[#7A152E] text-white text-xs font-semibold rounded-xl hover:bg-[#590D1E] transition-colors cursor-pointer shadow-xs"
                >
                  Reset All Filters
                </button>
              </div>
            )}
          </main>

        </div>
      </div>

      {/* ========================================================
          4. MOBILE SLIDE-OVER FILTER DRAWER
          ======================================================== */}
      {isMobileFilterOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex flex-col justify-end">
          {/* Backdrop */}
          <div
            onClick={() => setIsMobileFilterOpen(false)}
            className="absolute inset-0 bg-black/60 backdrop-blur-xs transition-opacity"
          />

          {/* Drawer Sheet */}
          <div className="relative bg-white rounded-t-3xl max-h-[85vh] flex flex-col shadow-2xl z-10 overflow-hidden">
            {/* Drawer Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-[#EAE4DC]">
              <div className="flex items-center gap-2">
                <SlidersHorizontal className="w-4 h-4 text-[#7A152E]" />
                <span className="font-serif text-lg font-semibold text-stone-900">
                  Filters &amp; Refine
                </span>
                {activeFilterCount > 0 && (
                  <span className="px-2 py-0.5 rounded-full bg-[#7A152E] text-white text-[10px] font-bold">
                    {activeFilterCount} Active
                  </span>
                )}
              </div>
              <button
                onClick={() => setIsMobileFilterOpen(false)}
                className="w-8 h-8 rounded-full bg-stone-100 flex items-center justify-center text-stone-600 hover:text-stone-900 cursor-pointer"
                aria-label="Close filters"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Drawer Scrollable Content */}
            <div className="p-5 space-y-6 overflow-y-auto flex-1">
              
              {/* Budget Range */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold uppercase tracking-wider text-stone-800">
                    Max Price
                  </span>
                  <span className="text-xs font-bold text-[#7A152E]">
                    Up to ₹{maxPriceSlider.toLocaleString('en-IN')}
                  </span>
                </div>
                <input
                  type="range"
                  min="1500"
                  max="15000"
                  step="500"
                  value={maxPriceSlider}
                  onChange={(e) => setMaxPriceSlider(Number(e.target.value))}
                  className="w-full accent-[#7A152E]"
                />
                <div className="flex justify-between text-[11px] text-stone-400 mt-1">
                  <span>₹1,500</span>
                  <span>₹15,000+</span>
                </div>
              </div>

              {/* Price Tiers */}
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-stone-800 block mb-2.5">
                  Quick Price Buckets
                </span>
                <div className="grid grid-cols-2 gap-2">
                  {PRICE_TIERS.map((tier) => (
                    <button
                      key={tier.id}
                      onClick={() => setSelectedPriceTier(tier.id)}
                      className={`px-3 py-2 rounded-xl text-xs font-medium text-center border transition-all cursor-pointer ${
                        selectedPriceTier === tier.id
                          ? 'border-[#7A152E] bg-[#7A152E]/10 text-[#7A152E] font-semibold'
                          : 'border-stone-200 bg-stone-50 text-stone-700'
                      }`}
                    >
                      {tier.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Metal Filter */}
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-stone-800 block mb-2.5">
                  Metal Purity &amp; Polish
                </span>
                <div className="grid grid-cols-2 gap-2">
                  {METALS.map((metal) => (
                    <button
                      key={metal.id}
                      onClick={() => setSelectedMetal(metal.id)}
                      className={`px-3 py-2 rounded-xl text-xs font-medium text-center border transition-all cursor-pointer ${
                        selectedMetal === metal.id
                          ? 'border-[#7A152E] bg-[#7A152E]/10 text-[#7A152E] font-semibold'
                          : 'border-stone-200 bg-stone-50 text-stone-700'
                      }`}
                    >
                      {metal.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Category Filter */}
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-stone-800 block mb-2.5">
                  Category
                </span>
                <div className="grid grid-cols-2 gap-2">
                  {CATEGORIES.map((cat) => (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`px-3 py-2 rounded-xl text-xs font-medium text-center border transition-all cursor-pointer ${
                        selectedCategory === cat.id
                          ? 'border-[#7A152E] bg-[#7A152E]/10 text-[#7A152E] font-semibold'
                          : 'border-stone-200 bg-stone-50 text-stone-700'
                      }`}
                    >
                      {cat.label}
                    </button>
                  ))}
                </div>
              </div>

            </div>

            {/* Drawer Bottom Actions */}
            <div className="p-4 border-t border-[#EAE4DC] bg-stone-50 flex items-center gap-3">
              <button
                onClick={handleResetFilters}
                className="flex-1 py-3 text-xs font-semibold text-stone-700 bg-white border border-stone-300 rounded-xl hover:bg-stone-100 transition-colors cursor-pointer"
              >
                Reset All
              </button>
              <button
                onClick={() => setIsMobileFilterOpen(false)}
                className="flex-1 py-3 text-xs font-semibold text-white bg-[#7A152E] hover:bg-[#590D1E] rounded-xl transition-colors cursor-pointer shadow-md"
              >
                Apply Filters
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
