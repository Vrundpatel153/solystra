import React, { useState, useEffect, useRef } from 'react';
import { useShop } from '../context/ShopContext';
import {
  Search,
  Heart,
  ShoppingBag,
  ChevronDown,
  ChevronRight,
  ArrowRight,
  MapPin,
  ShieldCheck,
  Sparkles
} from 'lucide-react';

const FEATURED_COLLECTIONS = [
  { label: 'New Atelier Arrivals', category: 'all', desc: 'Fresh handcrafted releases' },
  { label: 'The 18K Gold Suite', category: 'bracelets', desc: 'Italian vermeil & tennis links' },
  { label: 'Blush Rose Gold Edit', category: 'necklaces', desc: 'Warm feminine luminescence' },
  { label: 'Modern Classic Rings', category: 'rings', desc: 'Everyday solitaires & bands' },
  { label: 'Signature Bestsellers', category: 'bestseller', desc: 'Our most-coveted icons' }
];

const CATEGORY_ITEMS = [
  { label: 'Rings & Solitaires', category: 'rings', desc: 'Eternity, cocktail & promise bands' },
  { label: 'Necklaces & Pendants', category: 'necklaces', desc: 'Solitaires, chokers & lariats' },
  { label: 'Earrings & Studs', category: 'earrings', desc: 'Huggies, drops & statement studs' },
  { label: 'Bracelets & Cuffs', category: 'bracelets', desc: 'Tennis links, charms & kada cuffs' },
  { label: 'Complete Heirloom Suites', category: 'complete_sets', desc: 'Curated gift boxes & suites' }
];

const TONE_SWATCHES = [
  {
    name: 'Pure 925 Silver',
    purity: 'BIS Hallmarked • 92.5%',
    dots: ['#F8FAFC', '#CBD5E1', '#64748B'],
    category: 'all'
  },
  {
    name: '18K Gold Vermeil',
    purity: 'Thick Gold Layer • Mirror Polish',
    dots: ['#F3DFB0', '#C5A059', '#8C6118'],
    category: 'bracelets'
  },
  {
    name: '18K Rose Gold Finish',
    purity: 'Blush Luminescence',
    dots: ['#F8BBD0', '#E89895', '#D47B78'],
    category: 'necklaces'
  },
  {
    name: 'Oxidized Artisan Silver',
    purity: 'Vintage Heritage Patina',
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
    <div ref={menuContainerRef} className="sticky top-0 z-40 w-full font-sans">
      
      {/* ============================================================ */}
      {/* 1. TOP NAVBAR HEADER                                         */}
      {/* ============================================================ */}
      <header className="relative w-full z-50 bg-[#FAF8F5] border-b border-[#EAE4DC] shadow-sm transition-all">
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
                  className="py-1 text-[13px] font-sans tracking-wide transition-colors cursor-pointer text-[#7A152E] hover:text-[#5A0F22] font-semibold flex items-center gap-1.5 group"
                >
                  <span className="text-[#7A152E] group-hover:text-[#5A0F22] transition-colors">Offers</span>
                  <span className="bg-[#7A152E] text-white text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider shadow-2xs group-hover:bg-[#5A0F22] transition-colors">
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
          background: '#FAF8F5',
          borderBottomLeftRadius: '2rem',
          borderBottomRightRadius: '2rem',
          borderBottom: '1px solid rgba(197, 160, 89, 0.35)',
          borderLeft: '1px solid #EAE4DC',
          borderRight: '1px solid #EAE4DC',
        }}
      >
        <div className={`max-w-7xl mx-auto px-5 sm:px-8 py-6 sm:py-8 transition-all duration-700 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          isMenuOpen ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-3'
        }`}>
          
          {/* Desktop Mega Menu with Editorial Showcase */}
          <div className="hidden lg:grid grid-cols-12 gap-8 items-start">
            
            {/* Column 1: Featured Collections (3 cols) */}
            <div className="col-span-3 space-y-3 border-r border-[#EAE4DC]/80 pr-6">
              <div className="text-[11px] uppercase tracking-[0.2em] text-[#7A152E] font-bold pb-2 border-b border-[#EAE4DC]/60">
                Curated Collections
              </div>
              <div className="space-y-0.5 pt-1">
                {FEATURED_COLLECTIONS.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(item.category)}
                    className="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#FAF0F2] transition-all cursor-pointer group flex items-center justify-between"
                  >
                    <div>
                      <div className="text-[13px] font-sans font-semibold text-stone-900 group-hover:text-[#7A152E] transition-colors leading-tight">
                        {item.label}
                      </div>
                      <div className="text-[11px] text-stone-400 font-light mt-0.5">
                        {item.desc}
                      </div>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-stone-300 group-hover:text-[#7A152E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" />
                  </button>
                ))}
              </div>
            </div>

            {/* Column 2: Jewelry Categories (3 cols) */}
            <div className="col-span-3 space-y-3 border-r border-[#EAE4DC]/80 pr-6">
              <div className="text-[11px] uppercase tracking-[0.2em] text-stone-800 font-bold pb-2 border-b border-[#EAE4DC]/60">
                Jewelry Categories
              </div>
              <div className="space-y-0.5 pt-1">
                {CATEGORY_ITEMS.map((cat, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(cat.category)}
                    className="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#FAF8F5] transition-all cursor-pointer group flex items-center justify-between"
                  >
                    <div>
                      <div className="text-[13px] font-sans font-semibold text-stone-900 group-hover:text-[#7A152E] transition-colors leading-tight">
                        {cat.label}
                      </div>
                      <div className="text-[11px] text-stone-400 font-light mt-0.5">
                        {cat.desc}
                      </div>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-stone-300 group-hover:text-[#7A152E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" />
                  </button>
                ))}
                
                <button
                  onClick={() => {
                    window.location.hash = '#/categories';
                    setIsMenuOpen(false);
                  }}
                  className="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#FAF0F2] transition-all cursor-pointer group flex items-center justify-between mt-2 pt-2 border-t border-[#EAE4DC]/60"
                >
                  <div className="text-[12px] font-semibold text-[#7A152E] group-hover:text-[#590D1E] flex items-center gap-1.5">
                    <span>Explore All Categories</span>
                    <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </button>
              </div>
            </div>

            {/* Column 3: Precious Metals & Tones (3 cols) */}
            <div className="col-span-3 space-y-3 border-r border-[#EAE4DC]/80 pr-6">
              <div className="text-[11px] uppercase tracking-[0.2em] text-stone-800 font-bold pb-2 border-b border-[#EAE4DC]/60">
                Precious Finishes
              </div>
              <div className="space-y-2 pt-1">
                {TONE_SWATCHES.map((tone, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(tone.category)}
                    className="w-full text-left p-2.5 rounded-xl bg-white hover:bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/30 transition-all cursor-pointer group shadow-2xs"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[12px] font-sans font-semibold text-stone-900 group-hover:text-[#7A152E] transition-colors">
                        {tone.name}
                      </span>
                      <div className="flex items-center -space-x-1">
                        {tone.dots.map((dotColor, dotIdx) => (
                          <span
                            key={dotIdx}
                            className="w-2.5 h-2.5 rounded-full border border-white shadow-2xs"
                            style={{ backgroundColor: dotColor }}
                          />
                        ))}
                      </div>
                    </div>
                    <div className="text-[10.5px] text-stone-400 font-light">
                      {tone.purity}
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Column 4: Curated Editorial Showcase Spotlight Card (3 cols) */}
            <div className="col-span-3 space-y-3">
              <div className="text-[11px] uppercase tracking-[0.2em] text-[#C5A059] font-bold pb-2 border-b border-[#EAE4DC]/60 flex items-center gap-1.5">
                <Sparkles className="w-3 h-3 text-[#C5A059]" />
                <span>Atelier Showcase</span>
              </div>
              
              <div
                onClick={() => {
                  window.location.hash = '#/products';
                  setIsMenuOpen(false);
                }}
                className="relative rounded-2xl overflow-hidden bg-stone-900 group cursor-pointer aspect-[16/11] border border-[#EAE4DC] shadow-md flex flex-col justify-end p-4 transition-all duration-300 hover:shadow-xl"
              >
                <img
                  src="solystra_assets/categories/zavya_style/necklaces.png"
                  alt="Atelier Royal Gala Solitaires"
                  className="absolute inset-0 w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-700 opacity-80"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
                <div className="relative z-10 space-y-0.5">
                  <span className="text-[9px] font-sans font-bold uppercase tracking-[0.2em] text-[#EAD7AE] block">
                    Limited Gala Edition
                  </span>
                  <h4 className="font-serif text-[15px] text-white font-normal leading-snug">
                    The Solystra Heirloom Edit
                  </h4>
                  <p className="text-[11px] text-stone-300 font-light line-clamp-1">
                    BIS 925 Silver &amp; 18K Gold Solitaires
                  </p>
                  <div className="pt-1.5">
                    <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#EAD7AE] group-hover:text-white transition-colors">
                      <span>Explore Collection</span>
                      <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
                    </span>
                  </div>
                </div>
              </div>

              {/* Atelier Trust Assurance Strip */}
              <div className="p-2.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center gap-2 text-stone-600">
                <ShieldCheck className="w-4 h-4 text-[#7A152E] shrink-0" />
                <span className="text-[10px] font-medium leading-tight text-stone-700">
                  100% Certified BIS 925 Hallmark &bull; Insured Delivery
                </span>
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
                className="py-2.5 px-3 bg-stone-900 hover:bg-stone-800 text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 shadow-xs active:scale-95 transition-all cursor-pointer"
              >
                <span>Explore Catalog</span>
              </button>
              <button
                onClick={() => {
                  window.location.hash = '#/offers';
                  setIsMenuOpen(false);
                }}
                className="py-2.5 px-3 bg-[#7A152E] hover:bg-[#590D1E] text-white rounded-xl text-xs font-semibold flex items-center justify-center gap-1.5 shadow-xs active:scale-95 transition-all cursor-pointer"
              >
                <span>Offers Privilege %</span>
              </button>
            </div>

            {/* Curated Collections List */}
            <div className="space-y-1 pb-3 border-b border-[#EAE4DC]">
              <div className="text-[11px] font-bold uppercase tracking-wider text-[#7A152E] mb-1.5">
                Curated Collections
              </div>
              <div className="grid grid-cols-1 gap-1">
                {FEATURED_COLLECTIONS.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(item.category)}
                    className="w-full text-left p-2 rounded-lg hover:bg-stone-100 flex items-center justify-between text-xs font-medium text-stone-800 cursor-pointer"
                  >
                    <span>{item.label}</span>
                    <span className="text-[10px] text-stone-400">{item.desc}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Categories List */}
            <div className="space-y-1 pb-3 border-b border-[#EAE4DC]">
              <div className="text-[11px] font-bold uppercase tracking-wider text-stone-900 mb-1.5">
                Categories
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                {CATEGORY_ITEMS.map((cat, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(cat.category)}
                    className="p-2 bg-white rounded-lg border border-[#EAE4DC] text-left text-xs font-medium text-stone-800 cursor-pointer"
                  >
                    <div className="font-semibold">{cat.label.split(' ')[0]}</div>
                    <div className="text-[9.5px] text-stone-400 mt-0.5 truncate">{cat.label}</div>
                  </button>
                ))}

                <button
                  onClick={() => {
                    window.location.hash = '#/categories';
                    setIsMenuOpen(false);
                  }}
                  className="col-span-2 p-2.5 bg-[#FAF0F2] rounded-lg border border-[#7A152E]/20 text-center text-xs font-semibold text-[#7A152E] hover:bg-[#F3E2E6] transition-colors cursor-pointer flex items-center justify-center gap-1.5"
                >
                  <span>Explore All Categories Archive</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Shop by Tone */}
            <div className="pt-1">
              <div className="text-[11px] font-bold uppercase tracking-wider text-stone-900 mb-2">
                Shop by Tone
              </div>
              <div className="grid grid-cols-2 gap-2">
                {TONE_SWATCHES.map((tone, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(tone.category)}
                    className="flex items-center justify-between px-3 py-2 bg-white border border-[#EAE4DC] rounded-xl text-xs font-medium text-stone-800 shadow-2xs active:scale-95 transition-all cursor-pointer"
                  >
                    <span className="text-[11px]">{tone.name}</span>
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
