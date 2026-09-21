import React, { useState, useEffect, useRef } from 'react';
import { useShop } from '../context/ShopContext';
import { Search, Heart, ShoppingBag, ChevronDown, MapPin } from 'lucide-react';

const FEATURED_COLLECTIONS = [
  { label: 'New Arrivals', category: 'all' },
  { label: 'The 18K Gold Suite', category: 'bracelets' },
  { label: 'Blush Tones Collection', category: 'necklaces' },
  { label: 'Modern Classics', category: 'rings' },
  { label: 'Bestsellers', category: 'bestseller' }
];

const CATEGORY_GROUPS = [
  {
    title: 'Necklaces',
    category: 'necklaces',
    items: ['Chokers', 'Solitaires', 'Lariats', 'Layering Chains', 'Pendants']
  },
  {
    title: 'Earrings & Rings',
    category: 'earrings',
    items: ['Studs', 'Huggies', 'Drops', 'Solitaire Bands', 'Cocktail Rings']
  },
  {
    title: 'Bracelets & Suites',
    category: 'bracelets',
    items: ['Tennis Links', 'Kada Cuffs', 'Charms', 'Complete Suites', 'Gift Vault']
  }
];

const TONE_SWATCHES = [
  {
    name: 'SILVER 925',
    dots: ['#F8FAFC', '#CBD5E1', '#64748B'],
    category: 'all'
  },
  {
    name: '18K GOLD',
    dots: ['#F3DFB0', '#C5A059', '#8C6118'],
    category: 'bracelets'
  },
  {
    name: 'ROSE GOLD',
    dots: ['#F8BBD0', '#E89895', '#D47B78'],
    category: 'necklaces'
  },
  {
    name: 'OXIDIZED',
    dots: ['#757575', '#424242', '#212121'],
    category: 'rings'
  }
];

// Reusable Mathematically Synchronized Menu Toggle Button with Identical Lines
const MenuToggleButton = ({ isOpen, onClick, className = '' }) => (
  <button
    type="button"
    onClick={onClick}
    className={`w-8 h-8 sm:w-9 sm:h-9 rounded-full flex items-center justify-center transition-all duration-500 cursor-pointer active:scale-95 group ${
      isOpen
        ? 'bg-[#7A152E]/10 text-[#7A152E]'
        : 'bg-stone-200/50 hover:bg-stone-200/80 text-[#231F20]'
    } ${className}`}
    aria-label={isOpen ? "Close menu" : "Open menu"}
    title={isOpen ? "Close" : "Menu"}
  >
    <div className="relative w-5 h-5 flex items-center justify-center">
      {/* Top Bar: Exactly 18px width, centered. In closed: top: 6px. In open: centered at top: 50%, rotated +45deg */}
      <span
        className={`absolute left-1/2 -translate-x-1/2 w-[18px] h-[2px] rounded-full transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] origin-center ${
          isOpen
            ? 'top-1/2 -translate-y-1/2 rotate-45 bg-[#7A152E]'
            : 'top-[6px] -translate-y-0 rotate-0 bg-[#231F20] group-hover:bg-[#7A152E]'
        }`}
      />
      {/* Bottom Bar: EXACT SAME 18px width, centered. In closed: top: 13px. In open: centered at top: 50%, rotated -45deg */}
      <span
        className={`absolute left-1/2 -translate-x-1/2 w-[18px] h-[2px] rounded-full transition-all duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] origin-center ${
          isOpen
            ? 'top-1/2 -translate-y-1/2 -rotate-45 bg-[#7A152E]'
            : 'top-[13px] -translate-y-0 rotate-0 bg-[#231F20] group-hover:bg-[#7A152E]'
        }`}
      />
    </div>
  </button>
);

export const Navbar = ({ activeCategory, onSelectCategory, onOpenBoutique }) => {
  const { cartItemCount, wishlist, setIsCartOpen, setIsWishlistOpen, setIsSearchOpen } = useShop();

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuContainerRef = useRef(null);

  const handleNavClick = (cat) => {
    if (onSelectCategory) {
      onSelectCategory(cat);
    }
    if (window.location.hash.startsWith('#/product/')) {
      window.location.hash = '#/';
    }
    setIsMenuOpen(false);
  };

  // Close on Escape key or outside click
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isMenuOpen) {
        setIsMenuOpen(false);
      }
    };

    const handleClickOutside = (e) => {
      if (menuContainerRef.current && !menuContainerRef.current.contains(e.target)) {
        setIsMenuOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    document.addEventListener('mousedown', handleClickOutside);

    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = '';
    };
  }, [isMenuOpen]);

  return (
    <div ref={menuContainerRef} className="relative z-40 font-sans">
      
      {/* ============================================================ */}
      {/* 1. TOP NAVBAR HEADER                                         */}
      {/* ============================================================ */}
      <header className="sticky top-0 z-50 bg-[#FAF8F5]/96 backdrop-blur-xl border-b border-[#EAE4DC] shadow-[0_2px_15px_rgba(0,0,0,0.03)] transition-all">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative flex items-center justify-between h-[52px] sm:h-[62px]">
            
            {/* ---------------------------------------------------- */}
            {/* LEFT: MOBILE MENU TOGGLE / DESKTOP NAV LINKS        */}
            {/* ---------------------------------------------------- */}
            <div className="relative z-10 flex items-center gap-1 sm:gap-6">
              
              {/* Mobile Menu Button */}
              <MenuToggleButton
                isOpen={isMenuOpen}
                onClick={() => setIsMenuOpen(prev => !prev)}
                className="lg:hidden"
              />

              {/* Desktop Left Nav Links (Minimalist Architecture) */}
              <nav className="hidden lg:flex items-center gap-5">
                <button
                  onClick={() => {
                    window.location.hash = '#/products';
                    setIsMenuOpen(false);
                  }}
                  className="py-1 text-[13px] font-sans tracking-wide transition-colors cursor-pointer text-stone-800 hover:text-[#7A152E] font-medium"
                >
                  Explore All
                </button>

                <button
                  onClick={() => {
                    window.location.hash = '#/offers';
                    setIsMenuOpen(false);
                  }}
                  className="py-1 text-[13px] font-sans tracking-wide transition-colors cursor-pointer text-[#7A152E] font-semibold flex items-center gap-1.5"
                >
                  <span>Offers</span>
                  <span className="bg-[#7A152E] text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full uppercase tracking-wider">
                    Privilege
                  </span>
                </button>

                <button
                  onClick={() => setIsMenuOpen(prev => !prev)}
                  className={`py-1 flex items-center gap-1.5 text-[13px] font-sans tracking-wide transition-colors cursor-pointer group ${
                    isMenuOpen
                      ? 'text-[#7A152E] font-semibold'
                      : 'text-stone-800 hover:text-[#7A152E] font-medium'
                  }`}
                >
                  <span>Collections</span>
                  <ChevronDown
                    className={`w-3.5 h-3.5 text-stone-400 group-hover:text-[#7A152E] transition-transform duration-300 ${
                      isMenuOpen ? 'rotate-180 text-[#7A152E]' : ''
                    }`}
                  />
                </button>
              </nav>
            </div>

            {/* ---------------------------------------------------- */}
            {/* CENTER: SOLYSTRA BRAND LOGO (Mathematically Centered) */}
            {/* ---------------------------------------------------- */}
            <div
              className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex items-center justify-center cursor-pointer py-1 z-20 pointer-events-auto"
              onClick={() => {
                window.location.hash = '#/';
                if (onSelectCategory) onSelectCategory('all');
                setIsMenuOpen(false);
              }}
            >
              <img
                src="solystra_assets/solystra_logo.png"
                alt="Solystra Jewels"
                className="h-6 sm:h-8 w-auto max-w-[115px] sm:max-w-[165px] object-contain hover:opacity-90 transition-opacity"
              />
            </div>

            {/* ---------------------------------------------------- */}
            {/* RIGHT: UTILITIES & ACTIONS (DESKTOP & MOBILE)        */}
            {/* ---------------------------------------------------- */}
            <div className="relative z-10 flex items-center gap-1 sm:gap-1.5">
              
              {/* Ateliers Trigger (Desktop) */}
              <button
                onClick={onOpenBoutique}
                className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 text-[11.5px] font-sans text-stone-700 hover:text-[#7A152E] hover:bg-stone-100/80 rounded-full transition-all cursor-pointer"
                title="Find Solystra Boutiques"
              >
                <MapPin className="w-3.5 h-3.5 text-[#7A152E]" />
                <span>Ateliers</span>
              </button>

              {/* Search Trigger (Mobile + Desktop) */}
              <button
                onClick={() => setIsSearchOpen(true)}
                className="p-1.5 sm:p-2 text-stone-700 hover:text-[#7A152E] transition-colors rounded-full hover:bg-stone-100 cursor-pointer"
                aria-label="Search jewelry collection"
              >
                <Search className="w-4 h-4 sm:w-[18px] sm:h-[18px] stroke-[1.7]" />
              </button>

              {/* Wishlist Trigger (Mobile + Desktop) */}
              <button
                onClick={() => setIsWishlistOpen(true)}
                className="relative p-1.5 sm:p-2 text-stone-700 hover:text-[#7A152E] transition-colors rounded-full hover:bg-stone-100 cursor-pointer"
                aria-label="Open wishlist"
              >
                <Heart className="w-4 h-4 sm:w-[18px] sm:h-[18px] stroke-[1.7]" />
                {wishlist.length > 0 && (
                  <span className="absolute top-0.5 right-0.5 bg-[#7A152E] text-white text-[8.5px] sm:text-[9.5px] font-bold w-3.5 h-3.5 sm:w-4 sm:h-4 rounded-full flex items-center justify-center shadow-xs">
                    {wishlist.length}
                  </span>
                )}
              </button>

              {/* Shopping Bag Trigger (Mobile + Desktop) */}
              <button
                onClick={() => setIsCartOpen(true)}
                className="relative p-1.5 sm:p-2 text-stone-700 hover:text-[#7A152E] transition-colors rounded-full hover:bg-stone-100 cursor-pointer flex items-center gap-1.5"
                aria-label="Open shopping bag"
              >
                <ShoppingBag className="w-4 h-4 sm:w-[18px] sm:h-[18px] stroke-[1.7]" />
                {cartItemCount > 0 && (
                  <span className="absolute top-0.5 right-0.5 lg:hidden bg-[#7A152E] text-white text-[8.5px] font-bold w-3.5 h-3.5 rounded-full flex items-center justify-center shadow-xs">
                    {cartItemCount}
                  </span>
                )}
                <span className="hidden lg:inline text-[12.5px] font-sans font-medium text-stone-800 hover:text-[#7A152E] tracking-tight">
                  Bag {cartItemCount > 0 ? `(${cartItemCount})` : '(0)'}
                </span>
              </button>

              {/* Desktop 2-Bar Menu Button (Bluorng Signature) */}
              <MenuToggleButton
                isOpen={isMenuOpen}
                onClick={() => setIsMenuOpen(prev => !prev)}
                className="hidden lg:flex ml-0.5"
              />

            </div>

          </div>
        </div>
      </header>

      {/* ============================================================ */}
      {/* 2. FROSTED GLASS BACKGROUND DIMMING OVERLAY                  */}
      {/* ============================================================ */}
      <div
        className={`fixed inset-0 top-[52px] sm:top-[62px] z-40 transition-all duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          isMenuOpen
            ? 'opacity-100 pointer-events-auto bg-stone-900/40 backdrop-blur-md'
            : 'opacity-0 pointer-events-none bg-stone-900/0 backdrop-blur-none'
        }`}
        onClick={() => setIsMenuOpen(false)}
        aria-hidden="true"
      />

      {/* ============================================================ */}
      {/* 3. FLUID COMPACT DROPDOWN DRAWER (LUXURY GLASSMORPHISM)      */}
      {/* ============================================================ */}
      <div
        className={`absolute top-full left-0 w-full z-50 overflow-hidden transition-all duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          isMenuOpen
            ? 'opacity-100 translate-y-0 scale-100 pointer-events-auto visible shadow-[0_30px_70px_-15px_rgba(0,0,0,0.25)]'
            : 'opacity-0 -translate-y-6 scale-[0.99] pointer-events-none invisible shadow-none'
        }`}
        style={{
          background: 'rgba(250, 248, 245, 0.95)',
          backdropFilter: 'blur(32px) saturate(180%)',
          WebkitBackdropFilter: 'blur(32px) saturate(180%)',
          borderBottomLeftRadius: '2rem',
          borderBottomRightRadius: '2rem',
          borderBottom: '1px solid rgba(197, 160, 89, 0.35)',
          borderLeft: '1px solid rgba(255, 255, 255, 0.7)',
          borderRight: '1px solid rgba(255, 255, 255, 0.7)',
        }}
      >
        <div className={`max-w-7xl mx-auto px-5 sm:px-8 py-6 sm:py-8 transition-all duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          isMenuOpen ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-3'
        }`}>
          
          {/* Desktop 5-Column Compact Grid */}
          <div className="hidden lg:grid grid-cols-5 gap-6 items-start">
            
            {/* Column 1: Featured Collections */}
            <div className="space-y-2.5">
              <div className="text-[11px] uppercase tracking-widest text-[#7A152E] font-bold mb-1">
                Featured Collections
              </div>
              {FEATURED_COLLECTIONS.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleNavClick(item.category)}
                  className="block text-left text-[14px] font-sans font-bold text-stone-900 hover:text-[#7A152E] transition-colors cursor-pointer tracking-tight"
                >
                  {item.label}
                </button>
              ))}
            </div>

            {/* Column 2: Category 1 (Necklaces) */}
            <div>
              <div className="text-[12.5px] font-bold text-stone-900 mb-2.5 tracking-tight flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                {CATEGORY_GROUPS[0].title}
              </div>
              <div className="flex flex-wrap gap-1.5">
                {CATEGORY_GROUPS[0].items.map((sub, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(CATEGORY_GROUPS[0].category)}
                    className="px-3 py-1.5 bg-white hover:bg-[#7A152E] text-stone-800 hover:text-white text-xs font-medium rounded-full border border-[#EAE4DC] hover:border-[#7A152E] shadow-2xs hover:shadow-xs transition-all cursor-pointer active:scale-95"
                  >
                    {sub}
                  </button>
                ))}
              </div>
            </div>

            {/* Column 3: Category 2 (Earrings & Rings) */}
            <div>
              <div className="text-[12.5px] font-bold text-stone-900 mb-2.5 tracking-tight flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                {CATEGORY_GROUPS[1].title}
              </div>
              <div className="flex flex-wrap gap-1.5">
                {CATEGORY_GROUPS[1].items.map((sub, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(CATEGORY_GROUPS[1].category)}
                    className="px-3 py-1.5 bg-white hover:bg-[#7A152E] text-stone-800 hover:text-white text-xs font-medium rounded-full border border-[#EAE4DC] hover:border-[#7A152E] shadow-2xs hover:shadow-xs transition-all cursor-pointer active:scale-95"
                  >
                    {sub}
                  </button>
                ))}
              </div>
            </div>

            {/* Column 4: Category 3 (Bracelets & Suites) */}
            <div>
              <div className="text-[12.5px] font-bold text-stone-900 mb-2.5 tracking-tight flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                {CATEGORY_GROUPS[2].title}
              </div>
              <div className="flex flex-wrap gap-1.5">
                {CATEGORY_GROUPS[2].items.map((sub, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(CATEGORY_GROUPS[2].category)}
                    className="px-3 py-1.5 bg-white hover:bg-[#7A152E] text-stone-800 hover:text-white text-xs font-medium rounded-full border border-[#EAE4DC] hover:border-[#7A152E] shadow-2xs hover:shadow-xs transition-all cursor-pointer active:scale-95"
                  >
                    {sub}
                  </button>
                ))}
              </div>
            </div>

            {/* Column 5: Shop by Tone (Swatch Pills) */}
            <div>
              <div className="text-[12.5px] font-bold text-stone-900 mb-2.5 tracking-tight flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#C5A059]" />
                Shop by Tone
              </div>
              <div className="grid grid-cols-2 gap-2">
                {TONE_SWATCHES.map((tone, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(tone.category)}
                    className="flex items-center justify-between px-2.5 py-1.5 bg-white hover:border-[#7A152E]/50 border border-[#EAE4DC] rounded-full shadow-2xs hover:shadow-xs transition-all cursor-pointer group active:scale-95"
                  >
                    <span className="text-[10px] font-bold tracking-wider text-stone-700 group-hover:text-[#7A152E]">
                      {tone.name}
                    </span>
                    <div className="flex items-center -space-x-1 ml-1.5">
                      {tone.dots.map((dotColor, dotIdx) => (
                        <span
                          key={dotIdx}
                          className="w-2.5 h-2.5 rounded-full border border-white shadow-2xs"
                          style={{ backgroundColor: dotColor }}
                        />
                      ))}
                    </div>
                  </button>
                ))}
              </div>
            </div>

          </div>

          {/* Mobile Clean High-Contrast Layout */}
          <div className="lg:hidden space-y-4 max-h-[70vh] overflow-y-auto no-scrollbar pr-0.5">
            {/* Direct Quick Action Buttons */}
            <div className="grid grid-cols-2 gap-2 pb-1">
              <button
                onClick={() => {
                  window.location.hash = '#/products';
                  setIsMenuOpen(false);
                }}
                className="py-2 px-3 bg-stone-900 hover:bg-stone-800 text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 shadow-xs active:scale-95 transition-all cursor-pointer"
              >
                <span>Explore Catalog</span>
              </button>
              <button
                onClick={() => {
                  window.location.hash = '#/offers';
                  setIsMenuOpen(false);
                }}
                className="py-2 px-3 bg-[#7A152E] hover:bg-[#590D1E] text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 shadow-xs active:scale-95 transition-all cursor-pointer"
              >
                <span>Offers Vault %</span>
              </button>
            </div>

            {/* Featured Links Bar */}
            <div className="flex flex-wrap gap-1.5 pb-3 border-b border-[#EAE4DC]">
              {FEATURED_COLLECTIONS.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => handleNavClick(item.category)}
                  className="px-3.5 py-1.5 bg-white hover:bg-[#7A152E] text-xs font-bold text-stone-900 hover:text-white rounded-full border border-[#EAE4DC] hover:border-[#7A152E] shadow-2xs active:scale-95 transition-all cursor-pointer"
                >
                  {item.label}
                </button>
              ))}
            </div>

            {/* Category Groups */}
            <div className="space-y-3">
              {CATEGORY_GROUPS.map((group, gIdx) => (
                <div key={gIdx}>
                  <div className="text-[11.5px] font-bold uppercase tracking-wider text-stone-900 mb-1.5">
                    {group.title}
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {group.items.map((sub, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleNavClick(group.category)}
                        className="px-3 py-1 bg-white text-[11.5px] text-stone-800 rounded-full border border-[#EAE4DC] shadow-2xs active:scale-95 transition-all"
                      >
                        {sub}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            {/* Shop by Tone */}
            <div className="pt-3 border-t border-[#EAE4DC]">
              <div className="text-[11.5px] font-bold uppercase tracking-wider text-stone-900 mb-2">
                Shop by Tone
              </div>
              <div className="flex flex-wrap gap-2">
                {TONE_SWATCHES.map((tone, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(tone.category)}
                    className="flex items-center gap-1.5 px-3 py-1 bg-white border border-[#EAE4DC] rounded-full text-xs font-semibold text-stone-800 shadow-2xs active:scale-95 transition-all"
                  >
                    <span>{tone.name}</span>
                    <div className="flex items-center -space-x-1">
                      {tone.dots.map((dotColor, dotIdx) => (
                        <span
                          key={dotIdx}
                          className="w-2.5 h-2.5 rounded-full border border-white"
                          style={{ backgroundColor: dotColor }}
                        />
                      ))}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
};
