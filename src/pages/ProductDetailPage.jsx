import React, { useState, useEffect, useRef } from 'react';
import { useShop } from '../context/ShopContext';
import { ProductCard } from '../components/ProductCard';
import {
  ShieldCheck,
  Truck,
  RotateCcw,
  Heart,
  ShoppingBag,
  Share2,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  Ruler,
  Check,
  X,
  Maximize2,
  MessageSquare,
  Package,
  CreditCard,
  Lock,
  Award,
  Feather,
  HelpCircle,
  Send,
  Tag,
  Gift
} from 'lucide-react';

export const ProductDetailPage = ({ productId }) => {
  const { PRODUCTS, addToCart, toggleWishlist, isInWishlist, showToast, setIsCartOpen, startCheckout, applyCoupon } = useShop();

  const product = PRODUCTS.find(p => p.id === productId) || PRODUCTS[0];

  const handleApplyOffer = (code) => {
    if (applyCoupon) {
      applyCoupon(code);
    }
    navigator.clipboard?.writeText(code);
    showToast(`Coupon code ${code} applied & copied!`);
  };

  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);

  // Clean product title: removes redundant "- 925 sterling silver" from titles
  const cleanTitle = (product.shortName || product.name || '')
    .replace(/\s*-\s*(925\s*)?(sterling\s*)?silver/gi, '')
    .replace(/\s*-\s*pure\s*silver/gi, '')
    .trim();

  // Floating Capsule CTA on mobile: pops up when scrolling down past product image
  const imageGalleryRef = useRef(null);
  const [showStickyCta, setShowStickyCta] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (!imageGalleryRef.current) return;
      const rect = imageGalleryRef.current.getBoundingClientRect();
      // Pop up smoothly as soon as user scrolls down past the product image
      if (rect.bottom < 260 || window.scrollY > 200) {
        setShowStickyCta(true);
      } else {
        setShowStickyCta(false);
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, [productId]);

  // Touch swipe handling for product images
  const touchStartXRef = useRef(null);
  const touchEndXRef = useRef(null);

  const handleTouchStart = (e) => {
    touchStartXRef.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e) => {
    touchEndXRef.current = e.touches[0].clientX;
  };

  const handleTouchEnd = () => {
    if (touchStartXRef.current === null || touchEndXRef.current === null) return;
    const diffX = touchStartXRef.current - touchEndXRef.current;
    const minSwipeDistance = 35;

    if (Math.abs(diffX) > minSwipeDistance && product.images && product.images.length > 1) {
      if (diffX > 0) {
        // Swiped Left -> Next image
        setSelectedImageIndex((prev) => (prev + 1) % product.images.length);
      } else {
        // Swiped Right -> Previous image
        setSelectedImageIndex((prev) => (prev - 1 + product.images.length) % product.images.length);
      }
    }

    touchStartXRef.current = null;
    touchEndXRef.current = null;
  };

  const [selectedMetal, setSelectedMetal] = useState(
    product.metals && product.metals.length ? product.metals[0] : 'Pure 925 Silver'
  );
  const [selectedSize, setSelectedSize] = useState('12');
  const [engravingText, setEngravingText] = useState('');
  const [showEngravingInput, setShowEngravingInput] = useState(false);
  const [quantity, setQuantity] = useState(1);

  const [showSizeGuide, setShowSizeGuide] = useState(false);
  const [activeTab, setActiveTab] = useState('specs');
  const [mobileExpandedSections, setMobileExpandedSections] = useState({});

  const toggleMobileSection = (id) => {
    setMobileExpandedSections(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const [pincode, setPincode] = useState('');
  const [pincodeResult, setPincodeResult] = useState(null);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviewForm, setReviewForm] = useState({ name: '', rating: 5, comment: '' });

  // Q&A State
  const [openQnaId, setOpenQnaId] = useState('qna-1');
  const [selectedQnaCategory, setSelectedQnaCategory] = useState('all');
  const [showAskQuestionModal, setShowAskQuestionModal] = useState(false);
  const [questionForm, setQuestionForm] = useState({ name: '', email: '', question: '' });

  const PRODUCT_QNA = [
    {
      id: 'qna-1',
      category: 'purity',
      question: 'Is this piece certified BIS Hallmarked 925 Sterling Silver?',
      answer: 'Yes, unconditionally. Every piece from Solystra Atelier is cast in solid 92.5% pure sterling silver and laser-inscribed with the official government-recognized BIS 925 hallmark on the clasp, inner shank, or rear casing. Each shipment includes a tamper-evident Certificate of Authenticity.',
      author: 'Atelier Quality Assurance',
      badge: 'Verified Expert',
      date: 'Official Response'
    },
    {
      id: 'qna-2',
      category: 'purity',
      question: 'Will the silver tarnish, oxidize, or turn skin green?',
      answer: 'No. Our creations receive an ultra-durable 2.0-micron double rhodium barrier coating (a rare precious metal from the platinum family). It provides an anti-tarnish mirror finish, prevents moisture oxidation, and is 100% hypoallergenic, nickel-free, and lead-free.',
      author: 'Master Silversmith',
      badge: 'Verified Expert',
      date: 'Official Response'
    },
    {
      id: 'qna-3',
      category: 'shipping',
      question: 'What is included in the packaging box and is shipping insured?',
      answer: 'Your jewelry arrives inside our signature emerald velvet keepsake box, accompanied by a luxury microfiber polishing cloth, sealed purity credentials, and a warranty card. Every parcel is 100% express insured against transit loss or damage across India.',
      author: 'Concierge Dispatch',
      badge: 'Verified Expert',
      date: 'Official Response'
    },
    {
      id: 'qna-4',
      category: 'shipping',
      question: 'What if the size does not fit or I want an exchange?',
      answer: 'We provide an unconditional 15-day exchange and return policy. If your ring size or bracelet fit needs adjustment, our insured courier will pick it up directly from your doorstep at zero fee, and your exchange or refund will be processed within 48 hours.',
      author: 'Customer Care Desk',
      badge: 'Verified Expert',
      date: 'Official Response'
    },
    {
      id: 'qna-5',
      category: 'care',
      question: 'How do I care for and maintain the stone brilliance at home?',
      answer: 'Simply buff gently with the complimentary Solystra microfiber polishing cloth after wearing. Keep pieces away from direct sprays of perfumes, chlorine pools, or harsh cleaning detergents. Store inside the dry velvet box to keep the Austrian stones fire-bright.',
      author: 'Atelier Care Guide',
      badge: 'Verified Expert',
      date: 'Official Response'
    }
  ];

  const filteredQna = selectedQnaCategory === 'all'
    ? PRODUCT_QNA
    : PRODUCT_QNA.filter(q => q.category === selectedQnaCategory);

  useEffect(() => {
    setSelectedImageIndex(0);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [productId]);

  const isWishlisted = isInWishlist(product.id);
  const isRing = product.category === 'rings';
  const isBracelet = product.category === 'bracelets';
  const sizes = isRing ? ['10', '12', '14', '16', '18', '20'] : ['6.5"', '7.0"', '7.5"'];

  const handleAddToCart = () => {
    addToCart(
      product,
      selectedMetal,
      isRing || isBracelet ? selectedSize : null,
      showEngravingInput ? engravingText : '',
      quantity
    );
  };

  const handleBuyNow = () => {
    addToCart(
      product,
      selectedMetal,
      isRing || isBracelet ? selectedSize : null,
      showEngravingInput ? engravingText : '',
      quantity
    );
    startCheckout();
  };

  const handleShare = () => {
    navigator.clipboard?.writeText(window.location.href);
    showToast('Product link copied to clipboard!');
  };

  const handlePincodeCheck = (e) => {
    e.preventDefault();
    if (!pincode || pincode.length < 6) {
      showToast('Please enter a valid 6-digit Indian Pincode', 'info');
      return;
    }
    const days = Math.floor(Math.random() * 2) + 2;
    const date = new Date();
    date.setDate(date.getDate() + days);
    const dateStr = date.toLocaleDateString('en-IN', { weekday: 'long', month: 'short', day: 'numeric' });
    setPincodeResult({
      success: true,
      message: `Express Delivery by ${dateStr} via BlueDart Insured Express`
    });
  };

  const emiAmount = Math.round(product.price / 3);
  const savingsAmount = product.mrp && product.mrp > product.price ? product.mrp - product.price : 0;
  const relatedProducts = PRODUCTS.filter(p => p.id !== product.id && p.category === product.category).slice(0, 4);

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] pb-24 font-sans">
      
      {/* Breadcrumb Bar (Hidden on Mobile View Only) */}
      <nav className="hidden sm:block border-b border-stone-200 bg-white py-3 px-4 sm:px-6 lg:px-8 text-xs text-stone-500">
        <div className="max-w-7xl mx-auto flex items-center gap-2 overflow-x-auto whitespace-nowrap">
          <a href="#/" className="hover:text-[#7A152E] transition-colors">Home</a>
          <ChevronRight className="w-3 h-3 text-stone-300" />
          <a
            href="#/"
            onClick={() => { window.location.hash = '#/'; }}
            className="capitalize hover:text-[#7A152E] transition-colors"
          >
            {product.categoryName}
          </a>
          <ChevronRight className="w-3 h-3 text-stone-300" />
          <span className="text-stone-800 font-medium truncate max-w-xs">{product.name}</span>
        </div>
      </nav>

      {/* Main PDP Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 sm:pt-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          
          {/* Left: Gallery with Vertical Thumbnail Rail (7 Cols) */}
          <div ref={imageGalleryRef} className="lg:col-span-7 flex flex-col-reverse sm:flex-row gap-4">
            
            {/* Vertical Thumbnail Rail */}
            {product.images.length > 1 && (
              <div className="flex sm:flex-col gap-2.5 overflow-x-auto sm:overflow-y-auto sm:max-h-[560px] no-scrollbar shrink-0">
                {product.images.map((img, idx) => (
                  <button
                    key={idx}
                    onClick={() => setSelectedImageIndex(idx)}
                    className={`relative w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden bg-white border transition-all shrink-0 cursor-pointer ${
                      selectedImageIndex === idx
                        ? 'border-[#7A152E] ring-2 ring-[#7A152E]/20 shadow-xs'
                        : 'border-stone-200 opacity-75 hover:opacity-100 hover:border-stone-400'
                    }`}
                    aria-label={`View angle ${idx + 1}`}
                  >
                    <img src={img} alt={`${product.name} angle ${idx + 1}`} className="w-full h-full object-cover block" />
                  </button>
                ))}
              </div>
            )}

            {/* Main Stage Viewport with Touch Swipe Gesture Support */}
            <div className="flex-1 space-y-4">
              <div
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={handleTouchEnd}
                className="relative aspect-square w-full rounded-2xl overflow-hidden bg-white border border-stone-200 shadow-xs group select-none touch-pan-y"
              >
                <img
                  src={product.images[selectedImageIndex] || product.images[0]}
                  alt={product.name}
                  className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 cursor-zoom-in block"
                  onClick={() => setIsLightboxOpen(true)}
                  draggable={false}
                />

                {/* Eyebrow Badges */}
                <div className="absolute top-4 left-4 flex flex-col gap-1.5 pointer-events-none z-10">
                  {product.badge && (
                    <span className="px-2.5 py-1 bg-[#7A152E] text-white text-[10.5px] uppercase tracking-wider font-semibold rounded shadow-xs">
                      {product.badge}
                    </span>
                  )}
                  <span className="px-2.5 py-0.5 bg-white/95 border border-stone-200 text-[#7A152E] text-[10.5px] font-medium tracking-wider uppercase rounded shadow-xs">
                    BIS 925 Hallmarked
                  </span>
                </div>

                {/* Action Overlays */}
                <div className="absolute top-4 right-4 flex items-center gap-2 z-10">
                  <button
                    onClick={() => setIsLightboxOpen(true)}
                    className="p-2.5 rounded-full bg-white/90 hover:bg-[#7A152E] text-stone-700 hover:text-white transition-all shadow-xs border border-stone-200 cursor-pointer"
                    aria-label="Enlarge Image"
                  >
                    <Maximize2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => toggleWishlist(product.id)}
                    className={`p-2.5 rounded-full backdrop-blur-xs transition-all shadow-xs border border-stone-200 cursor-pointer ${
                      isWishlisted ? 'bg-white text-[#7A152E]' : 'bg-white/90 text-stone-700 hover:text-[#7A152E]'
                    }`}
                    aria-label="Wishlist"
                  >
                    <Heart className={`w-4 h-4 ${isWishlisted ? 'fill-[#7A152E]' : ''}`} />
                  </button>
                </div>

                {/* Left/Right Navigation Chevrons on Main Image */}
                {product.images.length > 1 && (
                  <>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedImageIndex((prev) => (prev - 1 + product.images.length) % product.images.length);
                      }}
                      className="absolute left-2.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/85 hover:bg-white text-stone-800 shadow-sm border border-stone-200 flex items-center justify-center transition-all cursor-pointer z-10 active:scale-95"
                      aria-label="Previous image"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedImageIndex((prev) => (prev + 1) % product.images.length);
                      }}
                      className="absolute right-2.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/85 hover:bg-white text-stone-800 shadow-sm border border-stone-200 flex items-center justify-center transition-all cursor-pointer z-10 active:scale-95"
                      aria-label="Next image"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>

                    {/* Minimalist Image Dots Indicator on Mobile */}
                    <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex items-center gap-1.5 z-10 pointer-events-none">
                      {product.images.map((_, idx) => (
                        <span
                          key={idx}
                          className={`h-1.5 rounded-full transition-all duration-300 ${
                            selectedImageIndex === idx ? 'w-5 bg-[#7A152E]' : 'w-1.5 bg-black/25'
                          }`}
                        />
                      ))}
                    </div>
                  </>
                )}
              </div>
            </div>

          </div>

          {/* Right: Sticky Purchase Column (5 Cols) */}
          <div className="lg:col-span-5 lg:sticky lg:top-28 self-start space-y-5">
            
            {/* 1. Price, Discount, Taxes & Top Right Actions */}
            <div className="flex items-start justify-between pb-1">
              <div>
                <div className="flex items-baseline gap-2.5">
                  <span className="font-sans text-3xl sm:text-[34px] font-bold text-stone-900 tracking-tight">
                    ₹{product.price.toLocaleString('en-IN')}
                  </span>
                  <span className="text-sm sm:text-base font-bold text-[#D11A46]">
                    {product.discount ? (product.discount.toUpperCase().includes('OFF') ? product.discount : `${product.discount} Off`) : '52% Off'}
                  </span>
                </div>
                <div className="text-xs text-stone-500 mt-1 flex items-center gap-2">
                  <span className="line-through text-stone-400">
                    MRP ₹{product.mrp ? product.mrp.toLocaleString('en-IN') : (Math.round(product.price * 2.1)).toLocaleString('en-IN')}
                  </span>
                  <span>Incl. of all taxes</span>
                </div>
              </div>

              {/* Share & Wishlist Action Icons */}
              <div className="flex items-center gap-2 pt-1">
                <button
                  type="button"
                  onClick={handleShare}
                  className="w-9 h-9 rounded-full flex items-center justify-center text-stone-600 hover:text-stone-900 hover:bg-stone-100 transition-colors cursor-pointer"
                  title="Share Piece"
                  aria-label="Share"
                >
                  <Share2 className="w-4 h-4 stroke-[1.8]" />
                </button>
                <button
                  type="button"
                  onClick={() => toggleWishlist(product.id)}
                  className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors cursor-pointer ${
                    isWishlisted ? 'text-[#7A152E] bg-rose-50' : 'text-stone-600 hover:text-stone-900 hover:bg-stone-100'
                  }`}
                  title={isWishlisted ? "In your Wishlist" : "Add to Wishlist"}
                  aria-label="Wishlist"
                >
                  <Heart className={`w-4 h-4 stroke-[1.8] ${isWishlisted ? 'fill-[#7A152E] text-[#7A152E]' : ''}`} />
                </button>
              </div>
            </div>

            {/* 2. Product Title & Purity Tagline */}
            <div className="space-y-1">
              <h1 className="font-sans text-xl sm:text-2xl text-stone-800 font-normal leading-snug">
                {product.name}
              </h1>
              <p className="text-xs sm:text-[13px] text-stone-500 font-normal">
                Made with pure 925 silver
              </p>
            </div>

            {/* Subtle Metal & Size Options */}
            <div className="pt-1 pb-1 space-y-2 border-y border-stone-100 py-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-stone-500 font-medium">Metal:</span>
                  <div className="flex items-center gap-1.5">
                    {[
                      { name: 'Pure 925 Silver', label: 'Silver', color: 'bg-slate-300' },
                      { name: 'Rose Gold Plated', label: 'Rose Gold', color: 'bg-[#E5C3CB]' },
                      { name: '18K Gold Vermeil', label: '18K Gold', color: 'bg-[#C5A059]' }
                    ].map(m => (
                      <button
                        key={m.name}
                        type="button"
                        onClick={() => setSelectedMetal(m.name)}
                        className={`text-[11px] px-2 py-0.5 rounded-md border flex items-center gap-1 transition-all cursor-pointer ${
                          selectedMetal === m.name
                            ? 'border-[#7A152E] bg-[#7A152E] text-white font-medium shadow-2xs'
                            : 'border-stone-200 bg-white text-stone-600 hover:border-stone-300'
                        }`}
                      >
                        <span className={`w-1.5 h-1.5 rounded-full ${m.color}`} />
                        <span>{m.label}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {(isRing || isBracelet) && (
                  <div className="flex items-center gap-1.5">
                    <span className="text-[11px] text-stone-500 font-medium">Size:</span>
                    <div className="flex items-center gap-1">
                      {sizes.map(s => (
                        <button
                          key={s}
                          type="button"
                          onClick={() => setSelectedSize(s)}
                          className={`px-2 py-0.5 text-[11px] rounded-md border transition-all cursor-pointer ${
                            selectedSize === s
                              ? 'bg-[#7A152E] text-white border-[#7A152E] font-semibold shadow-2xs'
                              : 'bg-white text-stone-700 border-stone-200 hover:border-[#7A152E]/50'
                          }`}
                        >
                          {s}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Complimentary Laser Engraving toggle */}
              <div className="flex items-center justify-between text-[11px]">
                <label className="flex items-center gap-2 cursor-pointer text-stone-600">
                  <input
                    type="checkbox"
                    checked={showEngravingInput}
                    onChange={(e) => setShowEngravingInput(e.target.checked)}
                    className="w-3.5 h-3.5 accent-black rounded cursor-pointer"
                  />
                  <span>Add Complimentary Laser Engraving</span>
                </label>
                <span className="text-[#C5A059] font-bold text-[10px] tracking-wider uppercase">FREE</span>
              </div>

              {showEngravingInput && (
                <div className="pt-1">
                  <input
                    type="text"
                    maxLength={15}
                    value={engravingText}
                    onChange={(e) => setEngravingText(e.target.value)}
                    placeholder="Enter initials or date (e.g. S & V)"
                    className="w-full px-2.5 py-1.5 text-xs border border-stone-200 rounded-md focus:outline-none focus:border-stone-900 bg-stone-50"
                  />
                </div>
              )}
            </div>

            {/* 3. Action Button: Single Add to Cart Only */}
            <div className="pt-1">
              <button
                type="button"
                onClick={handleAddToCart}
                className="w-full py-4 px-6 rounded-xl bg-[#7A152E] hover:bg-[#590D1E] text-white font-sans text-xs sm:text-sm font-bold uppercase tracking-widest transition-all cursor-pointer active:scale-[0.98] shadow-md hover:shadow-lg text-center flex items-center justify-center gap-2.5 group"
              >
                <ShoppingBag className="w-4 h-4 text-[#F4D068] transition-transform group-hover:-translate-y-0.5" />
                <span>ADD TO CART</span>
              </button>
            </div>

            {/* 4. Available Offers */}
            <div className="space-y-2 pt-1">
              <div className="text-xs font-semibold text-stone-900 tracking-wide">
                Available offers
              </div>
              <div className="flex gap-2.5 overflow-x-auto hide-scrollbar pb-1">
                {[
                  { discount: 'Get 10% off', min: 'above ₹1990', code: 'SILVER10' },
                  { discount: 'Get 15% off', min: 'above ₹2990', code: 'SILVER15' },
                  { discount: 'Get 20% off', min: 'above ₹4990', code: 'SILVER20' },
                  { discount: 'Get 25% off', min: 'above ₹7990', code: 'SOLYSTRA25' }
                ].map((offer) => (
                  <button
                    key={offer.code}
                    type="button"
                    onClick={() => handleApplyOffer(offer.code)}
                    className="min-w-[130px] sm:min-w-[140px] p-3 rounded-xl bg-[#FAF5F0] border border-[#EAE0D3] text-left hover:border-[#7A152E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 active:scale-95 shadow-2xs"
                  >
                    <p className="text-xs font-semibold text-stone-900 leading-tight">{offer.discount}</p>
                    <p className="text-[10px] text-stone-600 mt-0.5">{offer.min}</p>
                    <div className="mt-2 text-[10.5px] font-mono tracking-wide flex items-center justify-between">
                      <span className="text-stone-700">use <strong className="text-[#7A152E] font-bold">{offer.code}</strong></span>
                      <span className="text-[8.5px] uppercase font-sans font-semibold text-stone-400 group-hover:text-[#7A152E]">Apply</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* 5. ATELIER BOGO PRIVILEGE: LUXURY SINGLE HERO SPOTLIGHT WITH AUTOMATIC LOOPED WHITE SHINE ANIMATION */}
            <div className="relative rounded-2xl bg-gradient-to-br from-[#29050D] via-[#4A0918] to-[#690D23] text-white p-5 sm:p-6 shadow-xl overflow-hidden border border-[#C5A059]/45 ring-1 ring-inset ring-white/10 group">
              {/* Automatic Looped Luxury White Shine Sweep Beam */}
              <div className="absolute inset-0 overflow-hidden pointer-events-none z-20">
                <div className="luxury-card-shine-beam" />
              </div>

              {/* Soft Ambient Radiance Gradients */}
              <div className="absolute -top-12 -right-12 w-48 h-48 bg-[#C5A059]/15 rounded-full blur-2xl pointer-events-none" />
              <div className="absolute -bottom-12 -left-12 w-48 h-48 bg-[#8E1634]/30 rounded-full blur-2xl pointer-events-none" />

              {/* Header Micro-Bar without star icons */}
              <div className="flex items-center justify-between pb-3 border-b border-[#C5A059]/20 relative z-10">
                <div className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#EAD7AE] shadow-[0_0_8px_#EAD7AE]" />
                  <span className="text-[10px] uppercase tracking-[0.22em] text-[#EAD7AE] font-bold font-sans">
                    ATELIER SIGNATURE PRIVILEGE
                  </span>
                </div>
                <span className="px-2.5 py-0.5 rounded-full bg-black/40 border border-[#C5A059]/35 text-[9px] font-mono font-medium text-amber-200/90 tracking-wide">
                  EXCLUSIVE OFFER
                </span>
              </div>

              {/* Single Product Showcase & Offer Narrative */}
              <div className="flex items-center gap-4 sm:gap-5 mt-4 relative z-10">
                {/* Left: Single Product Spotlight Pedestal */}
                <div className="relative w-24 h-24 sm:w-28 sm:h-28 rounded-2xl bg-gradient-to-b from-white/15 via-white/5 to-white/0 border border-[#C5A059]/50 p-2.5 flex items-center justify-center shrink-0 shadow-[0_12px_24px_rgba(0,0,0,0.45),inset_0_1px_1px_rgba(255,255,255,0.2)] group-hover:border-[#EAD7AE] transition-all duration-500">
                  {/* Subtle Ambient Gold Glow beneath the single jewel */}
                  <div className="absolute inset-2 rounded-xl bg-radial from-[#C5A059]/30 to-transparent blur-xs pointer-events-none" />

                  <img
                    src="solystra_assets/categories/cat_rings.png"
                    alt="Complimentary Pure 925 Solitaire Jewel"
                    className="w-full h-full object-contain filter drop-shadow-[0_6px_12px_rgba(0,0,0,0.55)] group-hover:scale-108 transition-transform duration-500 relative z-10"
                  />

                  <div className="absolute -bottom-2.5 left-1/2 -translate-x-1/2 px-2.5 py-0.5 rounded-full bg-gradient-to-r from-[#C5A059] via-[#E2C37D] to-[#C5A059] text-[#2D0610] font-sans font-black text-[8.5px] uppercase tracking-wider shadow-md whitespace-nowrap z-20 border border-white/30">
                    FREE GIFT
                  </div>
                </div>

                {/* Right: Editorial Headline & Interactive Action */}
                <div className="flex-1 min-w-0 flex flex-col justify-between py-0.5">
                  <div>
                    <div className="flex items-baseline gap-2 flex-wrap">
                      <h3 className="font-serif text-xl sm:text-2xl font-bold uppercase tracking-wide text-white leading-none drop-shadow-sm">
                        BUY 1 GET 1
                      </h3>
                      <span className="font-serif italic text-2xl sm:text-3xl text-[#EAD7AE] font-normal leading-none">
                        Free
                      </span>
                    </div>
                    <p className="text-[11.5px] text-stone-200/90 font-light mt-1.5 leading-relaxed">
                      Add any 2 handcrafted creations — the second jewel is gifted with our compliments.
                    </p>
                  </div>

                  {/* Coupon Code & Instant Claim CTA */}
                  <div className="pt-3 flex flex-wrap items-center gap-2.5">
                    <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/45 border border-dashed border-[#C5A059]/50 shadow-inner">
                      <span className="text-[9px] uppercase font-mono text-stone-300 tracking-wider">CODE:</span>
                      <span className="font-mono text-xs font-bold text-[#F4D068] tracking-widest">BOGOFREE</span>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleApplyOffer('BOGOFREE')}
                      className="px-4 py-2 rounded-xl bg-gradient-to-r from-[#C5A059] via-[#E2C37D] to-[#C5A059] bg-[length:200%_auto] hover:bg-right text-[#2D0610] text-xs font-bold uppercase tracking-wider transition-all duration-300 cursor-pointer active:scale-95 shadow-md hover:shadow-lg flex items-center gap-1.5 whitespace-nowrap"
                    >
                      <span>Claim Gift</span>
                      <Check className="w-3.5 h-3.5 stroke-[2.5]" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Bottom 3-Point Guarantee Strip */}
              <div className="mt-4 pt-3 border-t border-[#C5A059]/20 flex items-center justify-between text-[10px] text-stone-300 font-medium relative z-10 flex-wrap gap-2">
                <div className="flex items-center gap-1.5 text-[#EAD7AE]">
                  <span className="w-3.5 h-3.5 rounded-full bg-[#C5A059]/25 flex items-center justify-center text-[9px] text-[#EAD7AE] font-bold">✓</span>
                  <span className="text-stone-200">Auto-applied in bag</span>
                </div>
                <div className="flex items-center gap-1.5 text-[#EAD7AE]">
                  <span className="w-3.5 h-3.5 rounded-full bg-[#C5A059]/25 flex items-center justify-center text-[9px] text-[#EAD7AE] font-bold">✓</span>
                  <span className="text-stone-200">Pure 925 BIS Hallmarked</span>
                </div>
                <div className="flex items-center gap-1.5 text-[#EAD7AE]">
                  <span className="w-3.5 h-3.5 rounded-full bg-[#C5A059]/25 flex items-center justify-center text-[9px] text-[#EAD7AE] font-bold">✓</span>
                  <span className="text-stone-200">Complimentary Velvet Box</span>
                </div>
              </div>
            </div>

            {/* 6. Trust / 4-Pillar Strip */}
            <div className="p-3 sm:p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] grid grid-cols-4 divide-x divide-[#EAE4DC] text-center">
              {/* 1. Pure 925 Silver */}
              <div className="flex flex-col items-center justify-center px-1 sm:px-2 gap-1.5">
                <div className="w-8 h-8 rounded-full bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shadow-2xs">
                  <svg className="w-4 h-4 stroke-[1.6]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="9" r="6" />
                    <path d="M8.5 14.5L7 22l5-3 5 3-1.5-7.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <span className="text-[10px] sm:text-[11px] font-medium text-stone-800 leading-tight">
                  Pure<br />925 Silver
                </span>
              </div>

              {/* 2. Authenticity Certificate */}
              <div className="flex flex-col items-center justify-center px-1 sm:px-2 gap-1.5">
                <div className="w-8 h-8 rounded-full bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shadow-2xs">
                  <svg className="w-4 h-4 stroke-[1.6]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="4" y="3" width="16" height="18" rx="2" />
                    <path d="M8 7h8M8 11h8M8 15h4" strokeLinecap="round" />
                    <circle cx="15" cy="15" r="2" />
                  </svg>
                </div>
                <span className="text-[10px] sm:text-[11px] font-medium text-stone-800 leading-tight">
                  Authenticity<br />Certificate
                </span>
              </div>

              {/* 3. 15 Days Return */}
              <div className="flex flex-col items-center justify-center px-1 sm:px-2 gap-1.5">
                <div className="w-8 h-8 rounded-full bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shadow-2xs">
                  <svg className="w-4 h-4 stroke-[1.6]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M12 3L4 7.5v9L12 21l8-4.5v-9L12 3z" />
                    <path d="M12 12L4 7.5m8 4.5l8-4.5m-8 4.5V21" />
                  </svg>
                </div>
                <span className="text-[10px] sm:text-[11px] font-medium text-stone-800 leading-tight">
                  15 Days<br />Return
                </span>
              </div>

              {/* 4. 5 Lakh+ Customers */}
              <div className="flex flex-col items-center justify-center px-1 sm:px-2 gap-1.5">
                <div className="w-8 h-8 rounded-full bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shadow-2xs">
                  <svg className="w-4 h-4 stroke-[1.6]" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" strokeLinecap="round" />
                    <circle cx="9" cy="7" r="4" />
                    <path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" strokeLinecap="round" />
                  </svg>
                </div>
                <span className="text-[10px] sm:text-[11px] font-medium text-stone-800 leading-tight">
                  5 Lakh+<br />Customers
                </span>
              </div>
            </div>

            {/* 7. Estimated Delivery Time */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-stone-800 block">
                Estimated delivery time
              </label>
              <form onSubmit={handlePincodeCheck} className="flex h-10 border border-stone-300 rounded-md overflow-hidden focus-within:border-[#7A152E] transition-colors">
                <input
                  type="text"
                  maxLength={6}
                  value={pincode}
                  onChange={(e) => setPincode(e.target.value.replace(/\D/g, ''))}
                  placeholder="Enter 6 digit pincode"
                  className="flex-1 px-3.5 text-xs bg-white text-stone-900 placeholder-stone-400 focus:outline-none"
                />
                <button
                  type="submit"
                  className="px-6 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider transition-colors cursor-pointer"
                >
                  Check
                </button>
              </form>
              {pincodeResult && (
                <div className="text-xs text-stone-800 bg-[#FAF5EE] border border-[#EADCC8] rounded-md p-2.5 flex items-center gap-2 mt-2">
                  <Check className="w-4 h-4 text-[#7A152E] shrink-0 stroke-[2.2]" />
                  <span>{pincodeResult.message}</span>
                </div>
              )}
            </div>

            {/* 8. 1 YEAR PLATING WARRANTY Ribbon (Royal Burgundy & Gold Atelier Banner) */}
            <div
              onClick={() => showToast('Complimentary replating & ultrasonic spa cleaning covered under our 1-year guarantee!')}
              className="relative py-3.5 px-4 rounded-md bg-gradient-to-r from-[#4A0A19] via-[#7A152E] to-[#4A0A19] border border-[#8E1B38] text-center cursor-pointer hover:shadow-md transition-all overflow-hidden group shadow-sm"
            >
              <h4 className="font-sans text-xs sm:text-[13px] font-extrabold uppercase tracking-wider text-white group-hover:text-[#E8D3A2] transition-colors">
                1 YEAR PLATING WARRANTY
              </h4>
              <p className="text-[8.5px] sm:text-[9px] text-stone-200/80 mt-0.5 sm:absolute sm:right-3 sm:bottom-1 group-hover:text-white transition-colors">
                Click to know more about the T&Cs.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* 5-Star Professional Ecommerce Product Details & Assurances */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-10">
        <div className="bg-white rounded-2xl border border-stone-200 overflow-hidden shadow-2xs">
          
          {/* Desktop 5-Column Tab Bar (Perfect 20% width per tab, fills 100% with no empty space) */}
          <div className="hidden md:grid grid-cols-5 border-b border-stone-200 bg-[#FAF8F5]">
            {[
              { id: 'specs', label: 'Specifications & Purity' },
              { id: 'shipping', label: 'Shipping & Details' },
              { id: 'care', label: 'Jewelry Care Guide' },
              { id: 'packaging', label: 'Packaging & Gifting' },
              { id: 'warranty', label: 'Warranty & Authenticity' }
            ].map(tab => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 lg:px-3 text-[11px] lg:text-xs uppercase tracking-wider transition-all text-center cursor-pointer border-r border-stone-200 last:border-r-0 ${
                  activeTab === tab.id
                    ? 'border-b-2 border-b-[#7A152E] text-[#7A152E] bg-white font-bold shadow-2xs'
                    : 'text-stone-500 hover:text-stone-900 hover:bg-stone-100/60 font-medium'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Desktop Active Tab Content */}
          <div className="hidden md:block p-6 sm:p-10">
            {activeTab === 'specs' && (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
                  <h3 className="font-serif text-2xl text-stone-900 font-normal">
                    Certified Craftsmanship Specifications
                  </h3>
                  <span className="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">
                    BIS 925 Hallmark Verified
                  </span>
                </div>
                <p className="text-xs text-stone-500 font-light mb-4">
                  Every Solystra creation is individually hallmarked and micro-set in pure 925 sterling silver.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5 sm:gap-4 text-xs">
                  {Object.entries({
                    'Metal Purity': product.specs?.['Metal Purity'] || 'BIS Certified 925 Sterling Silver',
                    'Plating Finish': product.specs?.['Plating Finish'] || 'Anti-Tarnish Rhodium & Micron E-Coat',
                    'Stone Setting': product.specs?.['Stone Setting'] || 'AAA+ Austrian Solitaire Crystals',
                    'Hallmark Verification': product.specs?.['Hallmark Verification'] || 'Certified 925 Stamp on Clasp/Band',
                    'Warranty Coverage': product.specs?.['Warranty Coverage'] || '1-Year Plating Warranty Assurance',
                    'Skin Compatibility': '100% Nickel & Lead Free (Hypoallergenic)',
                    'Packaging': product.specs?.['Packaging'] || 'Luxury Suede Box with Authenticity Card',
                    'Shipping': 'Free Insured Express Delivery Across India',
                    ...(product.specs || {})
                  }).map(([key, value]) => (
                    <div key={key} className="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
                      <span className="text-stone-500 font-medium text-xs">{key}</span>
                      <span className="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'shipping' && (
              <div className="space-y-6">
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                  <h3 className="font-serif text-2xl text-stone-900 font-normal">
                    Shipping &amp; Product Details
                  </h3>
                  <span className="text-[11px] text-emerald-700 font-semibold uppercase tracking-wider flex items-center gap-1">
                    <Truck className="w-3.5 h-3.5" /> Free Insured Delivery
                  </span>
                </div>

                {/* Design Highlights & Details Callout */}
                <div className="p-5 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                  <h4 className="font-serif text-base text-stone-900 font-normal">
                    Design Story &amp; Atelier Notes
                  </h4>
                  <p className="text-xs sm:text-sm text-stone-600 leading-relaxed font-normal whitespace-pre-line">
                    {product.desc || "Handcrafted with architectural precision and finished with mirror rhodium polish. Designed for effortless daily wear and timeless festive radiance."}
                  </p>
                </div>

                {/* 4 Shipping & Delivery Pillars */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-1.5">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <Truck className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">24-48 Hr Dispatch</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Inspected and dispatched from our atelier within 24–48 hours via BlueDart Express Air.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-1.5">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <RotateCcw className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">15-Day Easy Returns</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Hassle-free doorstep exchanges or full refunds with complimentary return pickup.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-1.5">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <ShieldCheck className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">100% Insured Transit</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Full transit insurance coverage protecting your jewelry against loss or handling damage.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-1.5">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <CreditCard className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Cash on Delivery</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      COD available across 19,000+ Indian pincodes with real-time SMS &amp; WhatsApp tracking.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'care' && (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                  <h3 className="font-serif text-2xl text-stone-900 font-normal">
                    Jewelry Care &amp; Longevity Rituals
                  </h3>
                  <span className="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">
                    Daily Preservation
                  </span>
                </div>
                <p className="text-xs text-stone-500 font-light mb-4">
                  Follow these simple steps to keep your pure 925 silver jewelry sparkling like new for years.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <X className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Avoid Direct Sprays</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Apply perfumes, hairsprays, sanitizers, and lotions before wearing your jewelry to safeguard the finish.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <Package className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Velvet Vault Storage</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Store each piece separately in your Solystra velvet box or an airtight pouch to prevent micro-scratches.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <Feather className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Microfiber Polishing</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Gently buff with our complimentary lint-free cloth after wear to wipe away surface oils and fingerprints.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <ShieldCheck className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Water &amp; Chlorine Care</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Remove before swimming in chlorinated pools or entering steam rooms to preserve the protective e-coating.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'packaging' && (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                  <h3 className="font-serif text-2xl text-stone-900 font-normal">
                    Luxury Packaging &amp; Unboxing Experience
                  </h3>
                  <span className="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">
                    Gift Ready Presentation
                  </span>
                </div>
                <p className="text-xs text-stone-500 font-light mb-4">
                  Every Solystra order arrives packaged in an unboxing experience crafted to delight and impress.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <Package className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Royal Velvet Vault</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Encased in a bespoke deep-burgundy suede velvet keepsake box with gold foil emblem and plush satin interior.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <Award className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Authenticity Certificate</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Includes our official serialized BIS 925 Hallmark purity guarantee card with QR verification.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <Lock className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Tamper-Evident Seal</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Secured with a serialized safety seal ensuring untouched freshness straight from our certified atelier.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white border border-stone-200 shadow-2xs space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-[#FAF5EE] text-[#7A152E] flex items-center justify-center font-bold">
                      <Heart className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Complimentary Gifting</h5>
                    <p className="text-stone-500 text-[11.5px] leading-relaxed">
                      Includes a luxury ribbon gift tote and custom handwritten celebration gift note at no extra cost.
                    </p>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'warranty' && (
              <div className="space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1">
                  <h3 className="font-serif text-2xl text-stone-900 font-normal">
                    1-Year Warranty &amp; Authenticity Guarantee
                  </h3>
                  <span className="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">
                    Comprehensive Coverage
                  </span>
                </div>
                <p className="text-xs text-stone-500 font-light mb-4">
                  We stand unconditionally behind the purity, plating endurance, and architectural longevity of every piece.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <ShieldCheck className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">1-Year Plating Warranty</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Free replating and refinishing if any unexpected tarnish or color fading occurs within 365 days of delivery.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <Award className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Government BIS Hallmark</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Certified 92.5% pure sterling silver, stamped with official BIS hallmarking insignia on every piece.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <RotateCcw className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">Free Ultrasonic Spa</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Send your jewelry anytime for complimentary deep ultrasonic cleaning and prong security inspections.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
                    <div className="w-8 h-8 rounded-lg bg-white border border-stone-200 text-[#7A152E] flex items-center justify-center font-bold shadow-2xs">
                      <Check className="w-4 h-4 stroke-[2]" />
                    </div>
                    <h5 className="font-semibold text-stone-900 text-[13px]">100% Skin Safe Guarantee</h5>
                    <p className="text-stone-600 text-[11.5px] leading-relaxed">
                      Pure rhodium &amp; gold barrier layer, 100% free of nickel, lead, and cadmium, certified safe for sensitive skin.
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Mobile Accordion Stack with See More / See Less & Smooth In-Out Dropdown Animation */}
          <div className="md:hidden divide-y divide-stone-200">
            {[
              {
                id: 'specs',
                label: 'Product Specifications',
                subtitle: 'BIS 925 hallmark, purity & dimensions',
                icon: <Award className="w-4 h-4 stroke-[1.8]" />,
                content: (
                  <div className="space-y-3 pt-2">
                    <div className="grid grid-cols-1 gap-2.5 text-xs">
                      {Object.entries({
                        'Metal Purity': product.specs?.['Metal Purity'] || 'BIS Certified 925 Sterling Silver',
                        'Plating Finish': product.specs?.['Plating Finish'] || 'Anti-Tarnish Rhodium & Micron E-Coat',
                        'Stone Setting': product.specs?.['Stone Setting'] || 'AAA+ Austrian Solitaire Crystals',
                        'Hallmark Verification': product.specs?.['Hallmark Verification'] || 'Certified 925 Stamp on Clasp/Band',
                        'Warranty Coverage': product.specs?.['Warranty Coverage'] || '1-Year Plating Warranty Assurance',
                        'Skin Compatibility': '100% Nickel & Lead Free (Hypoallergenic)',
                        'Packaging': product.specs?.['Packaging'] || 'Luxury Suede Box with Authenticity Card',
                        'Shipping': 'Free Insured Express Delivery Across India',
                        ...(product.specs || {})
                      }).map(([key, value]) => (
                        <div key={key} className="flex justify-between items-center p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC]">
                          <span className="text-stone-500 font-medium text-xs">{key}</span>
                          <span className="font-semibold text-stone-800 text-xs text-right ml-2">{value}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              },
              {
                id: 'shipping',
                label: 'Shipping & Details',
                subtitle: '24-48 Hr dispatch, BlueDart express & 15-day returns',
                icon: <Truck className="w-4 h-4 stroke-[1.8]" />,
                content: (
                  <div className="space-y-3 pt-2">
                    <div className="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-1.5">
                      <h5 className="font-serif text-sm text-stone-900 font-medium">Design Story &amp; Details</h5>
                      <p className="text-xs text-stone-600 leading-relaxed whitespace-pre-line">
                        {product.desc || "Handcrafted with architectural precision and finished with mirror rhodium polish for effortless daily wear."}
                      </p>
                    </div>
                    <div className="grid grid-cols-1 gap-2 text-xs">
                      <div className="p-3 rounded-lg bg-white border border-stone-200 flex items-start gap-2.5">
                        <Truck className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-stone-900 text-xs">24-48 Hr BlueDart Express Air</p>
                          <p className="text-[11px] text-stone-500">Free delivery nationwide with live tracking.</p>
                        </div>
                      </div>
                      <div className="p-3 rounded-lg bg-white border border-stone-200 flex items-start gap-2.5">
                        <RotateCcw className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                        <div>
                          <p className="font-semibold text-stone-900 text-xs">15-Day Doorstep Returns</p>
                          <p className="text-[11px] text-stone-500">Zero-friction exchanges with free pickup.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              },
              {
                id: 'care',
                label: 'Jewelry Care Guide',
                subtitle: 'Daily preservation & cleaning rituals',
                icon: <ShieldCheck className="w-4 h-4 stroke-[1.8]" />,
                content: (
                  <div className="space-y-2 pt-2 text-xs">
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <X className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Avoid Direct Sprays</p>
                        <p className="text-[11px] text-stone-600">Apply perfumes and lotions before putting on jewelry.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <Package className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Velvet Vault Storage</p>
                        <p className="text-[11px] text-stone-600">Store individually in your velvet box to prevent scratches.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <Feather className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Microfiber Polishing</p>
                        <p className="text-[11px] text-stone-600">Buff gently with soft lint-free cloth after wearing.</p>
                      </div>
                    </div>
                  </div>
                )
              },
              {
                id: 'packaging',
                label: 'Packaging & Gifting',
                subtitle: 'Royal velvet keepsake vault & unboxing',
                icon: <Package className="w-4 h-4 stroke-[1.8]" />,
                content: (
                  <div className="space-y-2 pt-2 text-xs">
                    <div className="p-3 rounded-lg bg-white border border-stone-200 flex items-start gap-2.5">
                      <Package className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Royal Velvet Keepsake Vault</p>
                        <p className="text-[11px] text-stone-500">Deep burgundy suede box with plush satin cushion.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-white border border-stone-200 flex items-start gap-2.5">
                      <Award className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">BIS Hallmark Certificate Card</p>
                        <p className="text-[11px] text-stone-500">Official serialized purity verification included.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-white border border-stone-200 flex items-start gap-2.5">
                      <Heart className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Complimentary Gifting</p>
                        <p className="text-[11px] text-stone-500">Gold-foiled bag &amp; custom handwritten celebration note.</p>
                      </div>
                    </div>
                  </div>
                )
              },
              {
                id: 'warranty',
                label: 'Warranty & Authenticity',
                subtitle: '1-Year plating warranty & hallmark guarantee',
                icon: <ShieldCheck className="w-4 h-4 stroke-[1.8]" />,
                content: (
                  <div className="space-y-2 pt-2 text-xs">
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <ShieldCheck className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">1-Year Plating Warranty</p>
                        <p className="text-[11px] text-stone-600">Free replating &amp; refinishing if any tarnish occurs within 365 days.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <Award className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">Government BIS 925 Hallmark</p>
                        <p className="text-[11px] text-stone-600">Certified 92.5% pure silver with official purity stamp.</p>
                      </div>
                    </div>
                    <div className="p-3 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-start gap-2.5">
                      <Check className="w-4 h-4 text-[#7A152E] shrink-0 mt-0.5" />
                      <div>
                        <p className="font-semibold text-stone-900 text-xs">100% Skin Safe &amp; Hypoallergenic</p>
                        <p className="text-[11px] text-stone-600">Nickel &amp; lead free, biocompatible dual-micron rhodium barrier.</p>
                      </div>
                    </div>
                  </div>
                )
              }
            ].map(tab => {
              const isExpanded = !!mobileExpandedSections[tab.id];
              return (
                <div key={tab.id} className="bg-white">
                  {/* Accordion Header */}
                  <div
                    onClick={() => toggleMobileSection(tab.id)}
                    className="p-4 flex items-center justify-between cursor-pointer active:bg-stone-50 transition-colors select-none"
                  >
                    <div className="flex items-center gap-2.5 min-w-0 pr-2">
                      <span className="w-7 h-7 rounded-full bg-[#FAF5EE] border border-[#EADCC8] text-[#7A152E] flex items-center justify-center shrink-0">
                        {tab.icon}
                      </span>
                      <div className="min-w-0">
                        <h4 className="font-sans text-xs uppercase tracking-wider font-bold text-stone-900 leading-snug">
                          {tab.label}
                        </h4>
                        <p className="text-[10px] text-stone-500 font-normal leading-tight mt-0.5">
                          {tab.subtitle}
                        </p>
                      </div>
                    </div>

                    <button
                      type="button"
                      className="text-[11px] font-semibold text-[#7A152E] flex items-center gap-1 shrink-0 px-2.5 py-1 rounded-md bg-[#FAF5EE] border border-[#EADCC8] hover:bg-[#F3EAD9] transition-all cursor-pointer"
                    >
                      <span>{isExpanded ? 'See Less' : 'See More'}</span>
                      <ChevronDown
                        className={`w-3.5 h-3.5 text-[#7A152E] transition-transform duration-300 ease-in-out ${
                          isExpanded ? 'rotate-180' : 'rotate-0'
                        }`}
                      />
                    </button>
                  </div>

                  {/* Smooth In-Out Collapsible Dropdown Content */}
                  <div
                    className={`transition-all duration-300 ease-in-out overflow-hidden ${
                      isExpanded ? 'max-h-[1400px] opacity-100 pb-5 px-4' : 'max-h-0 opacity-0'
                    }`}
                  >
                    {tab.content}
                  </div>
                </div>
              );
            })}
          </div>

        </div>
      </section>

      {/* Complete The Look Section */}
      {relatedProducts.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-10">
          <div className="mb-6">
            <span className="text-xs uppercase tracking-wider text-[#7A152E] font-semibold block mb-1">
              Complete The Look
            </span>
            <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
              You May Also Like
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {relatedProducts.map(p => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        </section>
      )}

      {/* Customer Reviews Section */}
      <section id="reviews-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-10">
        <div className="bg-white rounded-2xl border border-stone-200 p-6 sm:p-10 shadow-2xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-8 border-b border-stone-200 gap-4">
            <div>
              <span className="text-xs uppercase tracking-wider text-[#7A152E] font-semibold block mb-1">
                Verified Reviews
              </span>
              <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
                Customer Reviews &amp; Ratings
              </h3>
            </div>
            <button
              onClick={() => setShowReviewModal(true)}
              className="px-6 py-2.5 bg-[#7A152E] text-white text-xs font-medium rounded-lg hover:bg-[#590D1E] transition-colors flex items-center gap-2 self-start shadow-xs cursor-pointer"
            >
              <MessageSquare className="w-4 h-4" />
              <span>Write a Review</span>
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 pt-8">
            <div className="flex flex-col items-center justify-center p-6 rounded-2xl bg-stone-50 border border-stone-200 text-center">
              <div className="font-serif text-5xl font-normal text-[#7A152E]">
                {product.rating}
              </div>
              <div className="text-xs font-semibold text-stone-800 my-2 uppercase tracking-wider">
                Overall Satisfaction
              </div>
              <span className="text-xs text-stone-500 font-normal">
                Based on {product.reviewsCount} verified purchases
              </span>
            </div>

            <div className="md:col-span-2 space-y-4">
              <div className="p-5 rounded-xl border border-stone-200 bg-stone-50/50 space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <div className="font-medium text-stone-900 flex items-center gap-2">
                    <span>Meera Sengupta</span>
                    <span className="px-2 py-0.5 rounded bg-white text-[#7A152E] border border-stone-200 text-[10px] font-semibold">
                      Verified Buyer
                    </span>
                  </div>
                  <span className="text-stone-400">3 days ago</span>
                </div>
                <div className="text-xs font-semibold text-[#7A152E]">Rated 5.0 / 5.0</div>
                <p className="text-xs text-stone-600 leading-relaxed font-normal">
                  "Exceeded all expectations. The silver polish is mirror bright and spotless, and the setting of the stones is firm with zero wobbles. Truly an authentic luxury experience."
                </p>
              </div>

              <div className="p-5 rounded-xl border border-stone-200 bg-stone-50/50 space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <div className="font-medium text-stone-900 flex items-center gap-2">
                    <span>Kavita Rao</span>
                    <span className="px-2 py-0.5 rounded bg-white text-[#7A152E] border border-stone-200 text-[10px] font-semibold">
                      Verified Buyer
                    </span>
                  </div>
                  <span className="text-stone-400">1 week ago</span>
                </div>
                <div className="text-xs font-semibold text-[#7A152E]">Rated 5.0 / 5.0</div>
                <p className="text-xs text-stone-600 leading-relaxed font-normal">
                  "The packaging alone is worth half the price! Felt like receiving a gift from a high-end atelier. Hallmark stamp is clearly visible on the clasp."
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          PRODUCT ADVISORY & FAQ SECTION (Clean Luxury Accordion)
          ======================================================== */}
      <section id="qna-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-12">
        <div className="bg-white rounded-2xl border border-[#EAE4DC] p-5 sm:p-8 lg:p-10 shadow-2xs">
          
          {/* Header Row */}
          <div className="flex flex-col sm:flex-row sm:items-end justify-between pb-5 border-b border-[#EAE4DC] gap-4">
            <div>
              <span className="text-[10px] sm:text-[11px] uppercase tracking-widest text-[#7A152E] font-bold block mb-1">
                Product Advisory
              </span>
              <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
                Frequently Asked Questions
              </h3>
              <p className="text-xs sm:text-sm text-stone-500 mt-1 font-light">
                Direct answers regarding silver purity, BIS hallmarking, sizing, and lifetime care.
              </p>
            </div>

            <button
              onClick={() => setShowAskQuestionModal(true)}
              className="px-4 py-2 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-xs transition-colors flex items-center gap-2 self-start sm:self-auto cursor-pointer shrink-0 active:scale-98"
            >
              <HelpCircle className="w-3.5 h-3.5 text-[#F4D068]" />
              <span>Ask a Question</span>
            </button>
          </div>

          {/* Category Filter Tabs */}
          <div className="flex items-center gap-2 pt-5 pb-3 overflow-x-auto hide-scrollbar">
            {[
              { id: 'all', label: 'All Questions' },
              { id: 'purity', label: 'Purity & Hallmarking' },
              { id: 'shipping', label: 'Shipping & Delivery' },
              { id: 'care', label: 'Jewelry Care & Sizing' }
            ].map(cat => (
              <button
                key={cat.id}
                onClick={() => setSelectedQnaCategory(cat.id)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all whitespace-nowrap cursor-pointer ${
                  selectedQnaCategory === cat.id
                    ? 'bg-[#7A152E] text-white shadow-xs'
                    : 'bg-stone-100 text-stone-600 hover:bg-stone-200/80 hover:text-stone-900'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Clean Minimalist Q&A Accordion Rows */}
          <div className="divide-y divide-[#EAE4DC] border-y border-[#EAE4DC] mt-2">
            {filteredQna.map((item) => {
              const isOpen = openQnaId === item.id;
              return (
                <div key={item.id} className="py-4 sm:py-5 group">
                  <button
                    onClick={() => setOpenQnaId(isOpen ? null : item.id)}
                    className="w-full flex items-center justify-between text-left gap-4 cursor-pointer"
                  >
                    <span className="font-serif text-base sm:text-lg font-normal text-stone-900 group-hover:text-[#7A152E] transition-colors leading-snug">
                      {item.question}
                    </span>
                    <ChevronDown
                      className={`w-4 h-4 text-stone-400 group-hover:text-[#7A152E] shrink-0 transition-transform duration-300 ${
                        isOpen ? 'rotate-180 text-[#7A152E]' : ''
                      }`}
                    />
                  </button>

                  {isOpen && (
                    <div className="mt-2.5 space-y-2.5">
                      <p className="text-xs sm:text-sm text-stone-600 font-light leading-relaxed pr-4">
                        {item.answer}
                      </p>
                      <div className="flex items-center gap-2 text-[11px] text-stone-400 font-sans pt-1">
                        <span className="text-[10px] uppercase tracking-wider text-[#7A152E] font-bold">
                          Atelier Certified
                        </span>
                        <span>&bull;</span>
                        <span className="text-stone-500">{item.author}</span>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Concierge Desk Card */}
          <div className="mt-6 p-4 sm:p-5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h5 className="text-xs sm:text-sm font-semibold text-stone-900">
                Have a bespoke inquiry about custom sizing or engraving?
              </h5>
              <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5 font-light">
                Our master silversmiths and concierge desk respond to all inquiries within 2 hours.
              </p>
            </div>

            <button
              onClick={() => setShowAskQuestionModal(true)}
              className="px-4 py-2 bg-white hover:bg-stone-50 text-[#7A152E] hover:text-[#590D1E] text-xs font-semibold rounded-xl border border-[#7A152E]/30 shadow-2xs transition-colors shrink-0 cursor-pointer self-start sm:self-auto"
            >
              Ask Concierge Desk &rarr;
            </button>
          </div>

        </div>
      </section>

      {/* Lightbox Modal */}
      {isLightboxOpen && (
        <div className="fixed inset-0 z-50 bg-black/90 backdrop-blur-xs flex items-center justify-center p-4">
          <button
            onClick={() => setIsLightboxOpen(false)}
            className="absolute top-6 right-6 p-3 rounded-full bg-white/10 hover:bg-white text-white hover:text-black transition-all cursor-pointer"
          >
            <X className="w-6 h-6" />
          </button>
          <div className="max-w-4xl max-h-[85vh] rounded-2xl overflow-hidden shadow-2xl">
            <img
              src={product.images[selectedImageIndex] || product.images[0]}
              alt={product.name}
              className="w-full h-full object-contain block"
            />
          </div>
        </div>
      )}

      {/* Sizing Guide Modal */}
      {showSizeGuide && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-8 space-y-4 shadow-2xl border border-stone-200">
            <div className="flex justify-between items-center border-b border-stone-200 pb-3">
              <h3 className="font-serif text-xl text-stone-900 font-normal">
                Ring &amp; Wrist Measurement Guide
              </h3>
              <button
                onClick={() => setShowSizeGuide(false)}
                className="p-1 text-stone-400 hover:text-stone-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="text-xs text-stone-600 space-y-3 font-normal">
              <p>To measure your ring size accurately at home:</p>
              <ol className="list-decimal pl-4 space-y-1">
                <li>Wrap a narrow strip of paper or string snugly around your intended finger.</li>
                <li>Mark the exact spot where the paper overlaps.</li>
                <li>Measure the millimeter length with a standard ruler.</li>
              </ol>
              <div className="border border-stone-200 rounded-xl overflow-hidden mt-3">
                <table className="w-full text-left divide-y divide-stone-200">
                  <thead className="bg-stone-50 text-[11px] font-semibold text-stone-800">
                    <tr>
                      <th className="p-2.5">Indian Ring Size</th>
                      <th className="p-2.5">Inner Diameter (mm)</th>
                      <th className="p-2.5">Circumference (mm)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-stone-200 text-[11px]">
                    <tr><td className="p-2.5 font-medium">10</td><td className="p-2.5">15.9 mm</td><td className="p-2.5">50.0 mm</td></tr>
                    <tr><td className="p-2.5 font-medium">12</td><td className="p-2.5">16.5 mm</td><td className="p-2.5">51.8 mm</td></tr>
                    <tr><td className="p-2.5 font-medium">14</td><td className="p-2.5">17.2 mm</td><td className="p-2.5">54.0 mm</td></tr>
                    <tr><td className="p-2.5 font-medium">16</td><td className="p-2.5">17.8 mm</td><td className="p-2.5">56.0 mm</td></tr>
                    <tr><td className="p-2.5 font-medium">18</td><td className="p-2.5">18.5 mm</td><td className="p-2.5">58.0 mm</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <button
              onClick={() => setShowSizeGuide(false)}
              className="w-full py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-wider font-medium rounded-lg hover:bg-[#590D1E] transition-colors cursor-pointer"
            >
              Got It
            </button>
          </div>
        </div>
      )}

      {/* Review Modal */}
      {showReviewModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-stone-200">
            <div className="flex justify-between items-center border-b border-stone-200 pb-3">
              <h3 className="font-serif text-xl text-stone-900 font-normal">Share Your Review</h3>
              <button
                onClick={() => setShowReviewModal(false)}
                className="p-1 text-stone-400 hover:text-stone-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-stone-700 font-medium mb-1">Your Full Name</label>
                <input
                  type="text"
                  value={reviewForm.name}
                  onChange={(e) => setReviewForm({ ...reviewForm, name: e.target.value })}
                  placeholder="e.g. Radhika Sharma"
                  className="w-full px-3 py-2 border border-stone-200 rounded-lg focus:outline-none focus:border-[#7A152E]"
                />
              </div>
              <div>
                <label className="block text-stone-700 font-medium mb-1">Rating Score</label>
                <div className="flex gap-2">
                  {[1, 2, 3, 4, 5].map(score => (
                    <button
                      key={score}
                      type="button"
                      onClick={() => setReviewForm({ ...reviewForm, rating: score })}
                      className={`w-9 h-9 rounded-lg border text-xs font-semibold transition-all cursor-pointer ${
                        reviewForm.rating === score
                          ? 'bg-[#7A152E] text-white border-[#7A152E]'
                          : 'bg-white border-stone-200 text-stone-700 hover:border-[#7A152E]'
                      }`}
                    >
                      {score}.0
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-stone-700 font-medium mb-1">Your Review</label>
                <textarea
                  rows={3}
                  value={reviewForm.comment}
                  onChange={(e) => setReviewForm({ ...reviewForm, comment: e.target.value })}
                  placeholder="Share details about the silver luster, packaging, and fit..."
                  className="w-full px-3 py-2 border border-stone-200 rounded-lg focus:outline-none focus:border-[#7A152E]"
                />
              </div>
            </div>
            <button
              onClick={() => {
                showToast('Thank you! Your verified review has been submitted.');
                setShowReviewModal(false);
                setReviewForm({ name: '', rating: 5, comment: '' });
              }}
              className="w-full py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-wider font-medium rounded-lg hover:bg-[#590D1E] transition-colors cursor-pointer"
            >
              Submit Review
            </button>
          </div>
        </div>
      )}

      {/* Ask a Question Modal */}
      {showAskQuestionModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-stone-200">
            <div className="flex justify-between items-center border-b border-stone-200 pb-3">
              <div>
                <span className="text-[10px] uppercase tracking-wider text-[#7A152E] font-bold block">
                  Atelier Inquiry
                </span>
                <h3 className="font-serif text-xl text-stone-900 font-normal">Ask a Question</h3>
              </div>
              <button
                onClick={() => setShowAskQuestionModal(false)}
                className="p-1 text-stone-400 hover:text-stone-800 cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-stone-700 font-medium mb-1">Your Name</label>
                <input
                  type="text"
                  value={questionForm.name}
                  onChange={(e) => setQuestionForm({ ...questionForm, name: e.target.value })}
                  placeholder="e.g. Radhika Sharma"
                  className="w-full px-3 py-2 border border-stone-200 rounded-lg focus:outline-none focus:border-[#7A152E]"
                />
              </div>

              <div>
                <label className="block text-stone-700 font-medium mb-1">Email Address</label>
                <input
                  type="email"
                  value={questionForm.email}
                  onChange={(e) => setQuestionForm({ ...questionForm, email: e.target.value })}
                  placeholder="radhika@example.com"
                  className="w-full px-3 py-2 border border-stone-200 rounded-lg focus:outline-none focus:border-[#7A152E]"
                />
              </div>

              <div>
                <label className="block text-stone-700 font-medium mb-1">Your Question about {product.name}</label>
                <textarea
                  rows={3}
                  value={questionForm.question}
                  onChange={(e) => setQuestionForm({ ...questionForm, question: e.target.value })}
                  placeholder="e.g. Can this necklace be adjusted in length? Is the hallmark stamped on the clasp?"
                  className="w-full px-3 py-2 border border-stone-200 rounded-lg focus:outline-none focus:border-[#7A152E]"
                />
              </div>
            </div>

            <button
              onClick={() => {
                if (!questionForm.question) {
                  showToast('Please enter your question before submitting.', 'info');
                  return;
                }
                showToast('Thank you! Your question has been submitted to our atelier concierge.');
                setShowAskQuestionModal(false);
                setQuestionForm({ name: '', email: '', question: '' });
              }}
              className="w-full py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-wider font-bold rounded-lg hover:bg-[#590D1E] transition-colors cursor-pointer flex items-center justify-center gap-2"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Submit Inquiry</span>
            </button>
          </div>
        </div>
      )}

      {/* ========================================================
          FLOATING MOBILE CAPSULE CTA (Buy Now & Add to Cart)
          Floating capsule matching the mobile bottom bar shape & blur
          Smoothly springs in/out when scrolling past product image
          ======================================================== */}
      <aside
        aria-label="Floating Product Purchase Action"
        className={`fixed bottom-3.5 left-3 right-3 sm:left-6 sm:right-6 max-w-md mx-auto z-40 lg:hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${
          showStickyCta
            ? 'translate-y-0 scale-100 opacity-100 pointer-events-auto'
            : 'translate-y-16 scale-90 opacity-0 pointer-events-none'
        }`}
      >
        <div className="backdrop-blur-2xl bg-[#FAF8F5]/95 border border-white/90 shadow-[0_16px_40px_rgba(0,0,0,0.16),0_2px_8px_rgba(122,21,46,0.08)] rounded-full px-2 py-1.5 flex items-center justify-between gap-2">
          
          {/* Left: Round Thumbnail & Pricing */}
          <div className="flex items-center gap-2 min-w-0 flex-1 pl-1">
            <img
              src={product.images[0]}
              alt={product.name}
              className="w-9 h-9 rounded-full object-cover border border-[#EAE4DC] shrink-0 bg-white shadow-2xs"
            />
            <div className="min-w-0">
              <p className="text-[11.5px] text-stone-900 font-semibold truncate leading-tight">
                {cleanTitle}
              </p>
              <div className="flex items-baseline gap-1 mt-0.5 whitespace-nowrap">
                <span className="text-xs font-bold text-stone-950 font-sans">
                  ₹{product.price.toLocaleString('en-IN')}
                </span>
                {product.mrp && product.mrp > product.price && (
                  <span className="text-[10px] text-stone-400 line-through">
                    ₹{product.mrp.toLocaleString('en-IN')}
                  </span>
                )}
                {product.discount && (
                  <span className="text-[9px] font-bold text-[#D11A46] uppercase whitespace-nowrap">
                    {product.discount}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Right: Capsule CTA Buttons */}
          <div className="flex items-center gap-1.5 shrink-0">
            <button
              type="button"
              onClick={handleAddToCart}
              className="py-2 px-3 rounded-full border border-[#7A152E] text-[#7A152E] bg-white hover:bg-[#FAF8F5] text-xs font-bold flex items-center gap-1 active:scale-95 transition-all cursor-pointer shadow-2xs"
              title="Add to Cart"
            >
              <ShoppingBag className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>

            <button
              type="button"
              onClick={handleBuyNow}
              className="py-2 px-4 rounded-full bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold flex items-center gap-1 active:scale-95 transition-all cursor-pointer shadow-md tracking-wide"
            >
              <span>Buy Now</span>
            </button>
          </div>

        </div>
      </aside>

    </div>
  );
};

