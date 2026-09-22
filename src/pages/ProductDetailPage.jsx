import React, { useState, useEffect, useRef } from 'react';
import { useShop } from '../context/ShopContext';
import { ProductCard } from '../components/ProductCard';
import { MetalPurityBadge } from '../components/MetalPurityBadge';
import { GoldShoppingBag } from '../components/GoldShoppingBag';
import { DeliveryIcon, HallmarkIcon, ExchangeIcon, WarrantyIcon } from '../components/TrustBadges';
import {
  ShieldCheck,
  Truck,
  RotateCcw,
  Heart,
  ShoppingBag,
  Share2,
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
  Gift,
  Crown,
  Users,
  BadgeCheck,
  Star,
  ThumbsUp,
  CheckCircle2,
  Search,
  SlidersHorizontal,
  Sparkles,
  ArrowRight
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

  const INITIAL_REVIEWS = [
    {
      id: 'rev-1',
      name: 'Meera Sengupta',
      avatar: 'MS',
      location: 'Mumbai, MH',
      rating: 5,
      headline: 'Exceeded all expectations — mirror bright luxury finish!',
      comment: 'Exceeded all expectations. The silver polish is mirror bright and spotless, and the setting of the stones is firm with zero wobbles. Truly an authentic luxury experience.',
      date: '3 days ago',
      verified: true,
      helpfulCount: 24,
      metal: '925 Sterling Silver',
      finish: 'Rhodium Platinum Luster'
    },
    {
      id: 'rev-2',
      name: 'Kavita Rao',
      avatar: 'KR',
      location: 'Bengaluru, KA',
      rating: 5,
      headline: 'Packaging alone is worth half the price!',
      comment: 'The emerald velvet keepsake box alone is worth half the price! Felt like receiving a gift from a high-end atelier. BIS 925 Hallmark stamp is clearly visible and laser-crisp on the clasp.',
      date: '1 week ago',
      verified: true,
      helpfulCount: 19,
      metal: '925 Sterling Silver',
      finish: 'Signature Velvet Box'
    },
    {
      id: 'rev-3',
      name: 'Pooja Deshmukh',
      avatar: 'PD',
      location: 'Pune, MH',
      rating: 5,
      headline: 'Mesmerizing sparkle under natural sunlight',
      comment: 'I was hesitant about buying fine jewelry online, but Solystra Atelier proved me wrong. The sparkle of the stones is comparable to fine lab diamonds, and the solid silver feels substantial and weighty, not hollow.',
      date: '2 weeks ago',
      verified: true,
      helpfulCount: 15,
      metal: '925 Sterling Silver',
      finish: 'Insured Delivery'
    },
    {
      id: 'rev-4',
      name: 'Ananya Sharma',
      avatar: 'AS',
      location: 'New Delhi, DL',
      rating: 4,
      headline: 'Delicate craftsmanship, very comfortable clasp',
      comment: 'Very fine detailing and delicate craftsmanship. Sizing was exact according to their size guide. Arrived in 3 days with tamper-proof security seal and official purity certificate.',
      date: '3 weeks ago',
      verified: true,
      helpfulCount: 8,
      metal: '925 Sterling Silver',
      finish: 'Atelier Certified'
    }
  ];

  const [reviewsList, setReviewsList] = useState(INITIAL_REVIEWS);
  const [reviewRatingFilter, setReviewRatingFilter] = useState('all');
  const [reviewSortBy, setReviewSortBy] = useState('helpful');
  const [helpfulVotedReviews, setHelpfulVotedReviews] = useState({});
  const [isSortDropdownOpen, setIsSortDropdownOpen] = useState(false);
  const sortDropdownRef = useRef(null);

  useEffect(() => {
    const handleSortClickOutside = (e) => {
      if (sortDropdownRef.current && !sortDropdownRef.current.contains(e.target)) {
        setIsSortDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleSortClickOutside);
    document.addEventListener('touchstart', handleSortClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleSortClickOutside);
      document.removeEventListener('touchstart', handleSortClickOutside);
    };
  }, []);

  const SORT_OPTIONS = [
    { id: 'helpful', label: 'Most Helpful' },
    { id: 'recent', label: 'Most Recent' },
    { id: 'highest', label: 'Highest Rating' },
    { id: 'lowest', label: 'Lowest Rating' }
  ];

  const currentSortLabel = SORT_OPTIONS.find(o => o.id === reviewSortBy)?.label || 'Most Helpful';

  const handleHelpfulReview = (id) => {
    setHelpfulVotedReviews(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const filteredReviews = reviewsList
    .filter(r => {
      if (reviewRatingFilter === 'all') return true;
      return r.rating === Number(reviewRatingFilter);
    })
    .sort((a, b) => {
      if (reviewSortBy === 'recent') {
        return b.id.localeCompare(a.id);
      }
      if (reviewSortBy === 'highest') {
        return b.rating - a.rating;
      }
      if (reviewSortBy === 'lowest') {
        return a.rating - b.rating;
      }
      const aHelpful = a.helpfulCount + (helpfulVotedReviews[a.id] ? 1 : 0);
      const bHelpful = b.helpfulCount + (helpfulVotedReviews[b.id] ? 1 : 0);
      return bHelpful - aHelpful;
    });

  // Q&A State
  const [expandedQnaIds, setExpandedQnaIds] = useState({});
  const [selectedQnaCategory, setSelectedQnaCategory] = useState('all');
  const [showAskQuestionModal, setShowAskQuestionModal] = useState(false);
  const [questionForm, setQuestionForm] = useState({ name: '', email: '', question: '' });
  const [qnaSearchQuery, setQnaSearchQuery] = useState('');
  const [qnaHelpfulVoted, setQnaHelpfulVoted] = useState({});
  const [expandedReviewIds, setExpandedReviewIds] = useState({});

  const toggleQna = (id) => {
    setExpandedQnaIds(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const toggleReview = (id) => {
    setExpandedReviewIds(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const PRODUCT_QNA = [
    {
      id: 'qna-1',
      category: 'purity',
      question: 'Is this piece certified BIS Hallmarked 925 Sterling Silver?',
      answer: 'Yes, unconditionally. Every piece from Solystra Atelier is cast in solid 92.5% pure sterling silver and laser-inscribed with the official government-recognized BIS 925 hallmark on the clasp, inner shank, or rear casing. Each shipment includes a tamper-evident Certificate of Authenticity and purity card.',
      author: 'Master Silversmith • Solystra QA',
      badge: 'Verified Atelier Expert',
      helpfulCount: 42
    },
    {
      id: 'qna-2',
      category: 'purity',
      question: 'Will the silver tarnish, oxidize, or turn skin green over time?',
      answer: 'No. Our creations receive an ultra-durable 2.0-micron double rhodium barrier coating (a rare precious metal from the platinum family). It provides an anti-tarnish mirror finish, prevents moisture oxidation, and is 100% hypoallergenic, nickel-free, and lead-free.',
      author: 'Metallurgy Specialist',
      badge: 'Verified Atelier Expert',
      helpfulCount: 38
    },
    {
      id: 'qna-3',
      category: 'shipping',
      question: 'What is included in the packaging box and is shipping insured?',
      answer: 'Your jewelry arrives inside our signature emerald velvet keepsake box, accompanied by a luxury microfiber polishing cloth, sealed purity credentials, and a warranty card. Every parcel is 100% express insured against transit loss or damage across India.',
      author: 'Concierge Dispatch Team',
      badge: 'Verified Atelier Expert',
      helpfulCount: 29
    },
    {
      id: 'qna-4',
      category: 'shipping',
      question: 'What if the size does not fit or I want an exchange?',
      answer: 'We provide an unconditional 15-day exchange and return policy. If your ring size or bracelet fit needs adjustment, our insured courier will pick it up directly from your doorstep at zero fee, and your exchange or refund will be processed within 48 hours of inspection.',
      author: 'Customer Care Desk',
      badge: 'Verified Atelier Expert',
      helpfulCount: 31
    },
    {
      id: 'qna-5',
      category: 'care',
      question: 'Can I wear this jewelry during daily showers, swimming, or workouts?',
      answer: 'While our dual-layer rhodium plating offers superior water resistance compared to standard silver, we recommend avoiding prolonged contact with hot chlorinated water, pool chemicals, direct perfumes, or harsh detergents to maintain stone setting brilliance for decades.',
      author: 'Atelier Care Guide',
      badge: 'Verified Atelier Expert',
      helpfulCount: 23
    },
    {
      id: 'qna-6',
      category: 'care',
      question: 'How do I care for and maintain the stone brilliance at home?',
      answer: 'Simply buff gently with the complimentary Solystra microfiber polishing cloth after wearing. Keep pieces away from direct sprays of perfumes. Store inside the dry velvet box provided to keep the stones fire-bright.',
      author: 'Gemological Specialist',
      badge: 'Verified Atelier Expert',
      helpfulCount: 19
    }
  ];

  const handleHelpfulQna = (id) => {
    setQnaHelpfulVoted(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  const filteredQna = PRODUCT_QNA.filter(item => {
    const matchesCategory = selectedQnaCategory === 'all' || item.category === selectedQnaCategory;
    const matchesSearch = !qnaSearchQuery.trim() ||
      item.question.toLowerCase().includes(qnaSearchQuery.toLowerCase()) ||
      item.answer.toLowerCase().includes(qnaSearchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

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
  const relatedScrollRef = useRef(null);



  const sameCategory = PRODUCTS.filter(p => p.id !== product.id && p.category === product.category);
  const otherProducts = PRODUCTS.filter(p => p.id !== product.id && p.category !== product.category);
  const relatedProducts = [...sameCategory, ...otherProducts].slice(0, 10);

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
          
          {/* Left: Sticky Gallery with Vertical Thumbnail Rail (7 Cols) */}
          <div ref={imageGalleryRef} className="lg:col-span-7 lg:sticky lg:top-20 self-start flex flex-col-reverse sm:flex-row gap-4">
            
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

                {/* Marketing Status Tag (Top-Left) */}
                {product.badge && (
                  <div className="absolute top-4 left-4 pointer-events-none z-10">
                    <span className="px-3 py-1 bg-[#7A152E] text-white text-[10.5px] uppercase tracking-wider font-semibold rounded-full shadow-md border border-white/25">
                      {product.badge}
                    </span>
                  </div>
                )}

                {/* Atelier Hallmark Seal (Bottom-Left Craftsmanship Mark) */}
                <div className="absolute bottom-4 left-4 pointer-events-none z-10 transition-transform duration-300 group-hover:scale-105">
                  <MetalPurityBadge product={product} size="lg" />
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

          {/* Right: Purchase Details & Action Column (5 Cols) */}
          <div className="lg:col-span-5 space-y-5">
            
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

            {/* Color & Size Customization Area */}
            <div className="pt-1 pb-1 space-y-3 border-y border-stone-100 py-3">
              
              {/* 1. Dedicated Color Selection Row */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-semibold text-stone-800">
                    Color:
                  </span>
                  <span className="text-xs text-[#7A152E] font-medium bg-rose-50 px-2 py-0.5 rounded-md border border-rose-100">
                    {[
                      { name: 'Pure 925 Silver', label: 'Silver' },
                      { name: 'Rose Gold Plated', label: 'Rose Gold' },
                      { name: '18K Gold Vermeil', label: '18K Gold' }
                    ].find(m => m.name === selectedMetal)?.label || 'Silver'}
                  </span>
                </div>

                <div className="flex items-center gap-1.5 flex-wrap">
                  {[
                    { 
                      name: 'Pure 925 Silver', 
                      label: 'Silver', 
                      dotClass: 'bg-gradient-to-tr from-slate-400 via-slate-100 to-slate-300 border border-slate-300' 
                    },
                    { 
                      name: 'Rose Gold Plated', 
                      label: 'Rose Gold', 
                      dotClass: 'bg-gradient-to-tr from-[#C9808C] via-[#FCE3E8] to-[#E5A8B2] border border-[#C9808C]/40' 
                    },
                    { 
                      name: '18K Gold Vermeil', 
                      label: '18K Gold', 
                      dotClass: 'bg-gradient-to-tr from-[#946A1E] via-[#F7E7C4] to-[#C99D46] border border-[#946A1E]/50' 
                    }
                  ].map(m => {
                    const isSelected = selectedMetal === m.name;
                    return (
                      <button
                        key={m.name}
                        type="button"
                        onClick={() => setSelectedMetal(m.name)}
                        className={`text-xs px-2.5 py-1 rounded-lg border flex items-center gap-1.5 transition-all cursor-pointer font-medium active:scale-95 ${
                          isSelected
                            ? 'border-[#7A152E] bg-[#7A152E] text-white shadow-xs'
                            : 'border-stone-200 bg-white text-stone-700 hover:border-stone-300 hover:bg-stone-50'
                        }`}
                      >
                        <span className={`w-2 h-2 rounded-full shrink-0 ${m.dotClass} ${isSelected ? 'ring-1 ring-white/60' : ''}`} />
                        <span>{m.label}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* 2. Dedicated Ring Sizes Row (Fully Responsive) */}
              {isRing && (
                <div className="pt-2.5 border-t border-stone-100 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-stone-800">
                        Select Ring Size:
                      </span>
                      <span className="text-xs font-bold text-[#7A152E] bg-[#7A152E]/10 px-2 py-0.5 rounded-md border border-[#7A152E]/20">
                        Size {selectedSize}
                      </span>
                    </div>

                    {/* Size Guide Trigger */}
                    <button
                      type="button"
                      onClick={() => setShowSizeGuide(true)}
                      className="text-[11px] text-[#7A152E] hover:text-[#590D1E] hover:underline font-semibold flex items-center gap-1 cursor-pointer transition-colors"
                    >
                      <Ruler className="w-3.5 h-3.5" />
                      <span>Size Guide</span>
                    </button>
                  </div>

                  {/* Responsive Ring Size Pills (Wraps gracefully on any screen width) */}
                  <div className="flex flex-wrap items-center gap-2 sm:gap-2.5">
                    {sizes.map(s => {
                      const isSelected = selectedSize === s;
                      return (
                        <button
                          key={s}
                          type="button"
                          onClick={() => setSelectedSize(s)}
                          className={`min-w-[42px] sm:min-w-[46px] h-9 px-3 text-xs sm:text-[13px] font-bold rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-center active:scale-95 ${
                            isSelected
                              ? 'bg-[#7A152E] text-white border-[#7A152E] shadow-sm ring-2 ring-[#7A152E]/25'
                              : 'bg-white text-stone-700 border-stone-200 hover:border-[#7A152E] hover:text-[#7A152E] hover:bg-[#FAF8F5]'
                          }`}
                        >
                          {s}
                        </button>
                      );
                    })}
                  </div>

                  <p className="text-[10.5px] text-stone-500 font-light">
                    Standard Indian ring sizing &bull; Complimentary 15-day exchange if size doesn&apos;t fit
                  </p>
                </div>
              )}

              {/* Bracelet Size Row (if bracelet product) */}
              {isBracelet && (
                <div className="pt-2.5 border-t border-stone-100 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-stone-800">
                        Select Wrist Size:
                      </span>
                      <span className="text-xs font-bold text-[#7A152E] bg-[#7A152E]/10 px-2 py-0.5 rounded-md border border-[#7A152E]/20">
                        {selectedSize}
                      </span>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2">
                    {sizes.map(s => {
                      const isSelected = selectedSize === s;
                      return (
                        <button
                          key={s}
                          type="button"
                          onClick={() => setSelectedSize(s)}
                          className={`min-w-[50px] h-9 px-3 text-xs font-bold rounded-xl border transition-all duration-200 cursor-pointer flex items-center justify-center active:scale-95 ${
                            isSelected
                              ? 'bg-[#7A152E] text-white border-[#7A152E] shadow-sm ring-2 ring-[#7A152E]/25'
                              : 'bg-white text-stone-700 border-stone-200 hover:border-[#7A152E] hover:text-[#7A152E] hover:bg-[#FAF8F5]'
                          }`}
                        >
                          {s}
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

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
                <GoldShoppingBag className="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" />
                <span className="leading-none">ADD TO CART</span>
              </button>
            </div>

            {/* 4. Solystra Atelier Trust Badges & Delivery Concierge */}
            <div className="rounded-2xl bg-[#FAF6F0] border border-[#E8DFC8] p-3.5 sm:p-4 space-y-3.5 shadow-2xs">
              
              {/* 4 Official Fine Jewellery Trust Badges (Exact match to Landing Page) */}
              <div className="grid grid-cols-4 gap-1 sm:gap-2 text-center">
                {/* Badge 1: Insured Delivery */}
                <div className="flex flex-col items-center group cursor-default">
                  <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-white border border-[#E8DFC8] flex items-center justify-center text-[#7A152E] shadow-2xs group-hover:scale-105 group-hover:border-[#7A152E]/40 transition-all mb-1.5">
                    <DeliveryIcon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] sm:text-xs font-bold text-stone-900 leading-tight block">
                    Insured Delivery
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-stone-500 font-normal leading-tight block mt-0.5">
                    Express Air
                  </span>
                </div>

                {/* Badge 2: BIS 925 Hallmark */}
                <div className="flex flex-col items-center group cursor-default">
                  <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-white border border-[#E8DFC8] flex items-center justify-center text-[#7A152E] shadow-2xs group-hover:scale-105 group-hover:border-[#7A152E]/40 transition-all mb-1.5">
                    <HallmarkIcon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] sm:text-xs font-bold text-stone-900 leading-tight block">
                    BIS 925 Hallmark
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-stone-500 font-normal leading-tight block mt-0.5">
                    Tested Purity
                  </span>
                </div>

                {/* Badge 3: 7-Day Exchanges */}
                <div className="flex flex-col items-center group cursor-default">
                  <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-white border border-[#E8DFC8] flex items-center justify-center text-[#7A152E] shadow-2xs group-hover:scale-105 group-hover:border-[#7A152E]/40 transition-all mb-1.5">
                    <ExchangeIcon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] sm:text-xs font-bold text-stone-900 leading-tight block">
                    7-Day Exchanges
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-stone-500 font-normal leading-tight block mt-0.5">
                    Doorstep Pickup
                  </span>
                </div>

                {/* Badge 4: 1-Year Warranty */}
                <div className="flex flex-col items-center group cursor-default">
                  <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-xl bg-white border border-[#E8DFC8] flex items-center justify-center text-[#7A152E] shadow-2xs group-hover:scale-105 group-hover:border-[#7A152E]/40 transition-all mb-1.5">
                    <WarrantyIcon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] sm:text-xs font-bold text-stone-900 leading-tight block">
                    1-Year Warranty
                  </span>
                  <span className="text-[9px] sm:text-[10px] text-stone-500 font-normal leading-tight block mt-0.5">
                    Plating Guarantee
                  </span>
                </div>
              </div>

              {/* Solystra Royal Burgundy 1-Year Plating Warranty Pill (Responsive Zero Clipping Layout) */}
              <div
                onClick={() => showToast('Complimentary replating & ultrasonic spa cleaning covered under our 1-year warranty!')}
                className="relative overflow-hidden rounded-xl bg-gradient-to-r from-[#4A0A19] via-[#7A152E] to-[#4A0A19] border border-[#8E1B38] py-2 px-3 sm:px-4 flex items-center justify-center gap-1.5 sm:gap-2 cursor-pointer hover:shadow-md transition-all shadow-xs select-none"
              >
                {/* Smooth crystal-clear diagonal light sheen */}
                <div className="luxury-shine-sweep pointer-events-none" />
                
                <ShieldCheck className="w-3.5 h-3.5 text-[#EAD7AE] shrink-0 relative z-10" />
                <span className="relative z-10 font-sans text-[9.5px] min-[360px]:text-[10.5px] sm:text-xs font-semibold uppercase tracking-wide sm:tracking-wider text-white whitespace-nowrap text-center">
                  1-Year Warranty &bull; Free Replating &amp; Care
                </span>
              </div>

              {/* Delivery Estimation Concierge */}
              <div>
                <div className="flex items-center gap-1.5 text-xs font-semibold text-stone-900 mb-2">
                  <Truck className="w-3.5 h-3.5 text-[#7A152E]" />
                  <span>Estimated Delivery</span>
                </div>

                <form onSubmit={handlePincodeCheck} className="flex h-10 rounded-xl overflow-hidden border border-stone-300 focus-within:border-[#7A152E] transition-colors bg-white shadow-2xs">
                  <input
                    type="text"
                    maxLength={6}
                    value={pincode}
                    onChange={(e) => setPincode(e.target.value.replace(/\D/g, ''))}
                    placeholder="Enter 6-digit Indian pincode..."
                    className="flex-1 px-3.5 text-xs text-stone-900 placeholder-stone-400 focus:outline-none bg-transparent"
                  />
                  <button
                    type="submit"
                    className="px-5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider transition-colors cursor-pointer active:scale-95"
                  >
                    Check
                  </button>
                </form>

                {pincodeResult && (
                  <div className="mt-2 p-2.5 rounded-xl bg-emerald-50/70 border border-emerald-200/80 flex items-start gap-2 text-xs text-emerald-900">
                    <Check className="w-4 h-4 text-emerald-700 mt-0.5 shrink-0 stroke-[2.5]" />
                    <span className="leading-snug">{pincodeResult.message}</span>
                  </div>
                )}
              </div>

            </div>

            {/* 5. Available Offers */}
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

            {/* 6. ATELIER BOGO PRIVILEGE: SIGNATURE ROYAL BURGUNDY BANNER (#7A152E THEME) */}
            <div className="relative rounded-2xl text-white p-3.5 sm:p-4 shadow-md overflow-hidden bg-gradient-to-r from-[#4A0A19] via-[#7A152E] to-[#4A0A19] border border-[#C5A059]/45 ring-1 ring-inset ring-white/15 group">
              {/* Subtle Warm Gold Ambient Radiance Over Royal Burgundy */}
              <div className="absolute inset-0 bg-gradient-to-tr from-[#D4AF37]/15 via-transparent to-[#D4AF37]/10 pointer-events-none" />

              {/* Main Content Row: Matching Burgundy Jewel + Clean Offer Details */}
              <div className="flex items-center gap-3.5 sm:gap-4 relative z-10">
                {/* Solitaire Jewel on Royal Burgundy Velvet (Rounded corners + gold hairline border) */}
                <div className="relative w-16 h-16 sm:w-20 sm:h-20 shrink-0 rounded-xl sm:rounded-2xl overflow-hidden border border-[#D4AF37]/50 shadow-md">
                  <img
                    src="/solystra_assets/promos/bogo_gift_solitaire.jpg"
                    alt="Complimentary Atelier Solitaire Jewel"
                    className="w-full h-full object-cover group-hover:scale-108 transition-transform duration-500"
                  />
                  {/* Subtle inner gold rim gleam */}
                  <div className="absolute inset-0 rounded-xl sm:rounded-2xl ring-1 ring-inset ring-white/20 pointer-events-none" />
                </div>

                {/* Offer Copy & Direct CTA */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-2 flex-wrap">
                    <h3 className="font-serif text-base sm:text-lg font-bold tracking-tight text-white drop-shadow-xs">
                      BUY 1, RECEIVE 1
                    </h3>
                    <span className="font-serif italic text-lg sm:text-xl text-[#FFF0D0] font-normal leading-none drop-shadow-xs">
                      Free
                    </span>
                  </div>
                  <p className="text-[11px] sm:text-xs text-rose-100/90 font-light mt-0.5 leading-snug">
                    Add any 2 creations &mdash; the 2nd jewel is gifted with our compliments.
                  </p>

                  {/* Code Badge & CTA Button */}
                  <div className="mt-2 flex items-center gap-2 flex-wrap">
                    <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[#2D060F]/60 border border-[#D4AF37]/45 shadow-inner backdrop-blur-xs">
                      <span className="text-[8.5px] uppercase font-serif text-[#F4D068] font-bold tracking-wider">CODE</span>
                      <span className="w-px h-3 bg-[#D4AF37]/40" />
                      <span className="font-mono text-[11px] font-bold text-white tracking-wider">BOGOFREE</span>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleApplyOffer('BOGOFREE')}
                      className="btn-real-gold px-3.5 py-1 rounded-lg text-[11px] font-bold uppercase tracking-wider cursor-pointer active:scale-95 flex items-center gap-1 shadow-sm"
                    >
                      <span>Claim Gift</span>
                      <Check className="w-3 h-3 stroke-[3]" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Bottom Assurance Micro-Strip */}
              <div className="mt-2.5 pt-2 border-t border-[#D4AF37]/25 flex items-center justify-between text-[10px] sm:text-[10.5px] text-rose-100/90 font-medium relative z-10 flex-wrap gap-x-3 gap-y-1">
                <div className="flex items-center gap-1">
                  <Check className="w-3 h-3 text-[#FFF0D0] stroke-[2.5]" />
                  <span>Auto-applied in cart</span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-[#FFF0D0] font-bold">&bull;</span>
                  <span>Pure 925 BIS Hallmarked</span>
                </div>
                <div className="flex items-center gap-1">
                  <span className="text-[#FFF0D0] font-bold">&bull;</span>
                  <span>Complimentary Velvet Box</span>
                </div>
              </div>
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

      {/* Complete The Look Section (Smooth Row Slide Scroll) */}
      {relatedProducts.length > 0 && (
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-10 overflow-hidden">
          <div className="flex items-end justify-between mb-4 sm:mb-6">
            <div>
              <span className="text-xs uppercase tracking-wider text-[#7A152E] font-semibold block mb-1">
                Complete The Look
              </span>
              <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
                You May Also Like
              </h3>
            </div>

          </div>

          {/* Horizontal Smooth Sliding Row with Snap & Touch Physics */}
          <div
            ref={relatedScrollRef}
            className="flex gap-3 sm:gap-5 overflow-x-auto no-scrollbar scroll-smooth snap-x snap-mandatory py-2 -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8"
            style={{
              WebkitOverflowScrolling: 'touch',
              scrollBehavior: 'smooth'
            }}
          >
            {relatedProducts.map(p => (
              <div
                key={p.id}
                data-related-card="true"
                className="w-[200px] xs:w-[220px] sm:w-[240px] md:w-[260px] lg:w-[280px] shrink-0 snap-start select-none"
              >
                <ProductCard product={p} />
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Customer Reviews Section (Solystra Luxury Atelier Standard) */}
      <section id="reviews-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-10 sm:mt-14">
        <div className="bg-white rounded-2xl border border-[#EAE4DC] p-5 sm:p-8 lg:p-10 shadow-xs">
          
          {/* Section Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-[#EAE4DC] gap-4">
            <div className="space-y-1">
              <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
                Customer Reviews
              </h3>
              <p className="text-xs sm:text-sm text-stone-500 font-light">
                Authentic reflections from patrons who cherish this handcrafted Solystra creation.
              </p>
            </div>

            <button
              type="button"
              onClick={() => setShowReviewModal(true)}
              className="px-5 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold uppercase tracking-wider rounded-xl shadow-xs transition-all flex items-center gap-2 self-start sm:self-auto cursor-pointer active:scale-98 shrink-0"
            >
              <MessageSquare className="w-3.5 h-3.5 text-[#EAD7AE]" />
              <span>Write a Review</span>
            </button>
          </div>

          {/* Rating Overview & Breakdown Grid (Solystra Luxury Architecture) */}
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 lg:gap-8 py-8 border-b border-[#EAE4DC]">
            
            {/* 1. Overall Score & Recommendation (4 cols) */}
            <div className="md:col-span-4 flex flex-col justify-between bg-[#FAF8F5] rounded-2xl p-5 sm:p-6 border border-[#EAE4DC]">
              <div>
                <div className="flex items-baseline gap-3">
                  <span className="font-serif text-5xl sm:text-6xl font-normal text-[#7A152E] leading-none">
                    {product.rating || 4.9}
                  </span>
                  <div>
                    <div className="flex items-center gap-1">
                      {[1, 2, 3, 4, 5].map((s) => (
                        <Star
                          key={s}
                          className="w-4 h-4 text-[#C5A059] fill-[#C5A059]"
                        />
                      ))}
                    </div>
                    <span className="text-xs text-stone-500 font-medium block mt-1">
                      {product.rating || 4.9} out of 5 stars
                    </span>
                  </div>
                </div>

                {/* Recommend Badge (Solystra Champagne Gold & Burgundy Theme) */}
                <div className="mt-4 pt-4 border-t border-[#EAE4DC]">
                  <div className="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-[#FAF6EE] text-[#7A152E] text-xs font-medium border border-[#E8DCC4] w-full">
                    <CheckCircle2 className="w-4 h-4 text-[#7A152E] shrink-0" />
                    <span className="font-serif text-sm">98% of collectors recommend this creation</span>
                  </div>
                  <p className="text-[11px] text-stone-500 mt-2 font-light">
                    Aggregated from {product.reviewsCount || 128} verified order deliveries across India.
                  </p>
                </div>
              </div>

              {/* Characteristic Ratings */}
              <div className="mt-6 pt-4 border-t border-[#EAE4DC] space-y-2 text-xs">
                <div className="text-[11px] font-semibold uppercase tracking-wider text-stone-700 mb-2">
                  Atelier Quality Metrics
                </div>
                {[
                  { label: 'Silver Purity & Hallmarking', score: '5.0' },
                  { label: 'Stone Sparkle & Setting', score: '4.9' },
                  { label: 'Keepsake Velvet Packaging', score: '5.0' },
                  { label: 'Value for Investment', score: '4.8' }
                ].map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between text-stone-600">
                    <span className="text-[11px]">{item.label}</span>
                    <span className="font-medium text-stone-900 flex items-center gap-1">
                      <span>{item.score}</span>
                      <Star className="w-3 h-3 text-[#C5A059] fill-[#C5A059]" />
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* 2. Rating Breakdown Bars (5 cols) */}
            <div className="md:col-span-5 flex flex-col justify-center space-y-3 px-1 sm:px-3">
              <div className="text-xs font-semibold uppercase tracking-wider text-stone-700 mb-1">
                Rating Breakdown
              </div>
              {[
                { star: 5, pct: 88, count: Math.round((product.reviewsCount || 128) * 0.88) },
                { star: 4, pct: 9, count: Math.round((product.reviewsCount || 128) * 0.09) },
                { star: 3, pct: 2, count: Math.round((product.reviewsCount || 128) * 0.02) },
                { star: 2, pct: 1, count: Math.round((product.reviewsCount || 128) * 0.01) },
                { star: 1, pct: 0, count: 0 }
              ].map((item) => {
                const isSelected = reviewRatingFilter === item.star;
                return (
                  <button
                    key={item.star}
                    type="button"
                    onClick={() => setReviewRatingFilter(isSelected ? 'all' : item.star)}
                    className={`w-full flex items-center gap-3 group text-left transition-colors cursor-pointer rounded-lg p-1.5 ${
                      isSelected ? 'bg-[#FAF0F2] ring-1 ring-[#7A152E]/30' : 'hover:bg-[#FAF8F5]'
                    }`}
                  >
                    <span className="text-xs font-medium text-stone-700 w-12 flex items-center gap-1 group-hover:text-[#7A152E]">
                      <span>{item.star} star</span>
                    </span>
                    <div className="flex-1 h-2.5 bg-[#F3EFE9] rounded-full overflow-hidden border border-[#EAE4DC]/60 relative">
                      <div
                        className="h-full bg-linear-to-r from-[#C5A059] to-[#7A152E] rounded-full transition-all duration-500"
                        style={{ width: `${item.pct}%` }}
                      />
                    </div>
                    <span className="text-xs text-stone-500 font-medium w-10 text-right group-hover:text-[#7A152E]">
                      {item.pct}%
                    </span>
                  </button>
                );
              })}

              {reviewRatingFilter !== 'all' && (
                <div className="pt-2 flex items-center justify-between">
                  <span className="text-xs text-stone-500">
                    Showing only {reviewRatingFilter}-star reviews
                  </span>
                  <button
                    type="button"
                    onClick={() => setReviewRatingFilter('all')}
                    className="text-xs text-[#7A152E] hover:underline font-semibold cursor-pointer"
                  >
                    Clear Filter
                  </button>
                </div>
              )}
            </div>

            {/* 3. Review This Design Prompt (3 cols) */}
            <div className="md:col-span-3 flex flex-col justify-center p-5 rounded-2xl border border-[#EAE4DC] bg-white space-y-3">
              <h4 className="font-serif text-lg text-stone-900 font-normal">
                Review this creation
              </h4>
              <p className="text-xs text-stone-500 font-light leading-relaxed">
                Share your impressions with fellow collectors and receive 100 Solystra Club Reward Points.
              </p>
              <div className="flex items-center gap-1 py-1 text-stone-300">
                {[1, 2, 3, 4, 5].map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => {
                      setReviewForm(prev => ({ ...prev, rating: s }));
                      setShowReviewModal(true);
                    }}
                    className="hover:text-[#C5A059] hover:scale-110 transition-transform cursor-pointer"
                    title={`Rate ${s} stars`}
                  >
                    <Star className="w-5 h-5 fill-current" />
                  </button>
                ))}
              </div>
              <button
                type="button"
                onClick={() => setShowReviewModal(true)}
                className="w-full py-2 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-medium rounded-lg transition-colors cursor-pointer text-center shadow-xs"
              >
                Write Customer Review
              </button>
            </div>

          </div>

          {/* Filter Pills & Sorting Bar (Custom Luxury Dropdown with Proper UX) */}
          <div className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-[#EAE4DC]">
            <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-1 sm:pb-0 flex-1 min-w-0">
              <span className="text-xs font-semibold text-stone-500 mr-1 shrink-0">Filter:</span>
              {[
                { id: 'all', label: `All Reviews (${reviewsList.length})` },
                { id: 5, label: `5 Stars (${reviewsList.filter(r => r.rating === 5).length})` },
                { id: 4, label: `4 Stars (${reviewsList.filter(r => r.rating === 4).length})` }
              ].map(filter => (
                <button
                  key={filter.id}
                  type="button"
                  onClick={() => setReviewRatingFilter(filter.id)}
                  className={`px-3 py-1 rounded-full text-xs font-medium transition-all whitespace-nowrap cursor-pointer shrink-0 ${
                    reviewRatingFilter === filter.id
                      ? 'bg-[#7A152E] text-white shadow-2xs'
                      : 'bg-[#FAF8F5] text-stone-700 border border-[#EAE4DC] hover:border-[#7A152E]/30'
                  }`}
                >
                  {filter.label}
                </button>
              ))}
            </div>

            {/* Bespoke Luxury Sort Dropdown with Proper UX */}
            <div ref={sortDropdownRef} className="relative self-start sm:self-auto shrink-0 z-20">
              <button
                type="button"
                onClick={() => setIsSortDropdownOpen(!isSortDropdownOpen)}
                className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-[#FAF8F5] hover:bg-[#FAF0F2] border border-[#EAE4DC] hover:border-[#7A152E]/40 text-xs font-medium text-stone-800 transition-all cursor-pointer shadow-2xs select-none active:scale-98"
                aria-haspopup="listbox"
                aria-expanded={isSortDropdownOpen}
              >
                <span className="text-stone-400 font-normal">Sort:</span>
                <span className="text-stone-900 font-semibold">{currentSortLabel}</span>
                <ChevronDown
                  className={`w-3.5 h-3.5 text-[#7A152E] transition-transform duration-200 ${
                    isSortDropdownOpen ? 'rotate-180' : ''
                  }`}
                />
              </button>

              {/* Floating Luxury Menu with Backdrop Shadow */}
              {isSortDropdownOpen && (
                <div
                  className="absolute left-0 sm:left-auto sm:right-0 top-full mt-1.5 w-44 rounded-xl bg-white border border-[#EAE4DC] shadow-xl py-1.5 z-40 animate-in fade-in zoom-in-95 duration-150"
                  role="listbox"
                >
                  {SORT_OPTIONS.map(option => (
                    <button
                      key={option.id}
                      type="button"
                      onClick={() => {
                        setReviewSortBy(option.id);
                        setIsSortDropdownOpen(false);
                      }}
                      className={`w-full flex items-center justify-between px-3.5 py-2 text-xs text-left transition-colors cursor-pointer ${
                        reviewSortBy === option.id
                          ? 'bg-[#FAF0F2] text-[#7A152E] font-semibold'
                          : 'text-stone-700 hover:bg-[#FAF8F5] hover:text-stone-900'
                      }`}
                      role="option"
                      aria-selected={reviewSortBy === option.id}
                    >
                      <span>{option.label}</span>
                      {reviewSortBy === option.id && (
                        <Check className="w-3.5 h-3.5 text-[#7A152E]" />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Review Cards List (Solystra Atelier Theme & Fully Responsive) */}
          <div className="divide-y divide-[#EAE4DC] pt-2">
            {filteredReviews.map((review) => {
              const isHelpfulVoted = !!helpfulVotedReviews[review.id];
              return (
                <article key={review.id} className="py-6 sm:py-7 space-y-3">
                  
                  {/* User Profile Header (Zero wrapping collisions on mobile) */}
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-3 min-w-0">
                      <div className="w-10 h-10 rounded-full bg-[#FAF0F2] text-[#7A152E] font-serif font-bold text-xs flex items-center justify-center shrink-0 border border-[#EAD5DA]">
                        {review.avatar}
                      </div>
                      <div className="min-w-0">
                        <div className="flex flex-wrap items-center gap-1.5">
                          <span className="font-medium text-stone-900 text-sm">
                            {review.name}
                          </span>
                          {review.verified && (
                            <span className="inline-flex items-center gap-1 text-[10px] font-semibold text-[#8B6B38] bg-[#FAF6EE] px-2 py-0.5 rounded-full border border-[#E8DCC4] shrink-0">
                              <ShieldCheck className="w-2.5 h-2.5 text-[#C5A059]" />
                              <span>Verified Collector</span>
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] text-stone-400 mt-0.5 flex items-center gap-2">
                          {review.location && <span>{review.location}</span>}
                          {review.location && <span>•</span>}
                          <span>{review.date}</span>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Rating Stars & Headline */}
                  <div className="flex flex-wrap items-center gap-2">
                    <div className="flex items-center gap-0.5">
                      {[1, 2, 3, 4, 5].map((s) => (
                        <Star
                          key={s}
                          className={`w-3.5 h-3.5 ${
                            s <= review.rating
                              ? 'text-[#C5A059] fill-[#C5A059]'
                              : 'text-stone-300'
                          }`}
                        />
                      ))}
                    </div>
                    <h5 className="font-semibold text-stone-900 text-xs sm:text-sm">
                      {review.headline}
                    </h5>
                  </div>

                  {/* Variation Tag in Solystra Theme */}
                  {(review.metal || review.finish) && (
                    <div className="inline-flex flex-wrap items-center gap-1.5 text-[11px] text-stone-600 bg-[#FAF8F5] px-2.5 py-1 rounded-lg border border-[#EAE4DC]">
                      <span className="text-stone-400">Specification:</span>
                      <span className="font-medium text-[#7A152E]">{review.metal}</span>
                      {review.finish && (
                        <>
                          <span className="text-stone-300">•</span>
                          <span className="font-medium text-stone-700">{review.finish}</span>
                        </>
                      )}
                    </div>
                  )}

                  {/* Comment Body with Inline WhatsApp-Style Read More */}
                  {(() => {
                    const isRevExpanded = !!expandedReviewIds[review.id];
                    const REV_LIMIT = 140;
                    const isRevLong = review.comment.length > REV_LIMIT;
                    const revCut = isRevLong ? review.comment.lastIndexOf(' ', REV_LIMIT) : REV_LIMIT;
                    const rawRevSnippet = isRevLong ? review.comment.slice(0, revCut > 0 ? revCut : REV_LIMIT) : review.comment;
                    const revSnippet = rawRevSnippet.replace(/[.,\s]+$/, '');

                    return (
                      <p className="text-xs sm:text-sm text-stone-600 leading-relaxed font-normal">
                        "{isRevExpanded || !isRevLong ? (
                          <>
                            <span>{review.comment}</span>{' '}
                            {isRevLong && (
                              <button
                                type="button"
                                onClick={() => toggleReview(review.id)}
                                className="inline font-semibold text-[#7A152E] hover:underline cursor-pointer select-none text-xs ml-1"
                              >
                                See less
                              </button>
                            )}
                          </>
                        ) : (
                          <>
                            <span>{revSnippet}...</span>{' '}
                            <button
                              type="button"
                              onClick={() => toggleReview(review.id)}
                              className="inline font-semibold text-[#7A152E] hover:underline cursor-pointer select-none text-xs"
                            >
                              Read more
                            </button>
                          </>
                        )}"
                      </p>
                    );
                  })()}

                  {/* Solystra Helpful Action Bar */}
                  <div className="flex items-center gap-3 pt-1 text-xs text-stone-500">
                    <button
                      type="button"
                      onClick={() => handleHelpfulReview(review.id)}
                      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all cursor-pointer border active:scale-95 ${
                        isHelpfulVoted
                          ? 'bg-[#FAF0F2] border-[#7A152E] text-[#7A152E]'
                          : 'bg-[#FAF8F5] border-[#EAE4DC] hover:border-[#7A152E]/40 text-stone-700 hover:text-[#7A152E]'
                      }`}
                    >
                      <ThumbsUp className="w-3.5 h-3.5 text-[#C5A059]" />
                      <span>Helpful ({review.helpfulCount + (isHelpfulVoted ? 1 : 0)})</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => showToast('Feedback recorded. Thank you!')}
                      className="text-stone-400 hover:text-[#7A152E] transition-colors text-[11px] cursor-pointer"
                    >
                      Report
                    </button>
                  </div>

                </article>
              );
            })}
          </div>

        </div>
      </section>

      {/* ========================================================
          CUSTOMER QUESTIONS & ANSWERS (Solystra Luxury Advisory)
          ======================================================== */}
      <section id="qna-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8 sm:mt-12">
        <div className="bg-white rounded-2xl border border-[#EAE4DC] p-5 sm:p-8 lg:p-10 shadow-xs">
          
          {/* Header Row */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-[#EAE4DC] gap-4">
            <div className="space-y-1">
              <h3 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">
                Frequently Asked Questions
              </h3>
              <p className="text-xs sm:text-sm text-stone-500 font-light">
                Verified answers regarding BIS 925 hallmarking, custom sizing, insured courier dispatch, and lifetime care.
              </p>
            </div>

            <button
              type="button"
              onClick={() => setShowAskQuestionModal(true)}
              className="px-5 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold uppercase tracking-wider rounded-xl shadow-xs transition-colors flex items-center gap-2 self-start sm:self-auto cursor-pointer shrink-0 active:scale-98"
            >
              <HelpCircle className="w-3.5 h-3.5 text-[#EAD7AE]" />
              <span>Ask a Question</span>
            </button>
          </div>

          {/* Luxury Search Bar */}
          <div className="pt-6 pb-4">
            <div className="relative max-w-2xl">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#C5A059]" />
              <input
                type="text"
                value={qnaSearchQuery}
                onChange={(e) => setQnaSearchQuery(e.target.value)}
                placeholder="Search answers, purity, sizing, courier dispatch, care..."
                className="w-full pl-10 pr-10 py-2.5 bg-[#FAF8F5] border border-[#EAE4DC] rounded-xl text-xs sm:text-sm text-stone-900 placeholder:text-stone-400 focus:outline-none focus:border-[#7A152E] focus:bg-white focus:ring-1 focus:ring-[#7A152E]/20 transition-all shadow-2xs"
              />
              {qnaSearchQuery && (
                <button
                  type="button"
                  onClick={() => setQnaSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 hover:text-stone-700 p-1 cursor-pointer"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          </div>

          {/* Category Filter Tabs */}
          <div className="flex items-center gap-2 pb-4 overflow-x-auto no-scrollbar">
            {[
              { id: 'all', label: 'All Questions' },
              { id: 'purity', label: 'BIS Hallmark & Purity' },
              { id: 'shipping', label: 'Shipping & Free 15-Day Returns' },
              { id: 'care', label: 'Jewelry Care & Daily Wear' }
            ].map(cat => (
              <button
                key={cat.id}
                type="button"
                onClick={() => setSelectedQnaCategory(cat.id)}
                className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all whitespace-nowrap cursor-pointer ${
                  selectedQnaCategory === cat.id
                    ? 'bg-[#7A152E] text-white shadow-xs'
                    : 'bg-[#FAF8F5] text-stone-700 border border-[#EAE4DC] hover:border-[#7A152E]/30'
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Q&A Cards (WhatsApp-Style Inline Read More / See Less Inside Paragraph) */}
          {filteredQna.length > 0 ? (
            <div className="divide-y divide-[#EAE4DC] border-t border-[#EAE4DC]">
              {filteredQna.map((item) => {
                const isExpanded = !!expandedQnaIds[item.id];
                const isVoted = !!qnaHelpfulVoted[item.id];
                const LIMIT = 135;
                const isLong = item.answer.length > LIMIT;
                const cleanCut = isLong ? item.answer.lastIndexOf(' ', LIMIT) : LIMIT;
                const rawSnippet = isLong ? item.answer.slice(0, cleanCut > 0 ? cleanCut : LIMIT) : item.answer;
                const snippet = rawSnippet.replace(/[.,\s]+$/, '');

                return (
                  <div key={item.id} className="py-5 sm:py-6 space-y-3">
                    
                    {/* Question Row with Q Badge (Pure Title, No Dropdown Button) */}
                    <div className="flex items-start gap-3">
                      <span className="px-2 py-0.5 bg-[#FAF0F2] text-[#7A152E] border border-[#EAD5DA] text-[11px] font-cinzel font-bold rounded-md shrink-0 mt-0.5 tracking-wide">
                        Q
                      </span>
                      <h4 className="font-serif text-base sm:text-lg font-normal text-stone-900 leading-snug">
                        {item.question}
                      </h4>
                    </div>

                    {/* Answer Row with A Badge & Inline WhatsApp-style Read More */}
                    <div className="flex items-start gap-3 pl-0 sm:pl-1">
                      <span className="px-2 py-0.5 bg-[#FAF6EE] text-[#8B6B38] border border-[#E8DCC4] text-[11px] font-cinzel font-bold rounded-md shrink-0 mt-0.5 tracking-wide">
                        A
                      </span>
                      <div className="space-y-2 flex-1 min-w-0">
                        <p className="text-xs sm:text-sm text-stone-700 font-light leading-relaxed">
                          {isExpanded || !isLong ? (
                            <>
                              <span>{item.answer}</span>{' '}
                              {isLong && (
                                <button
                                  type="button"
                                  onClick={() => toggleQna(item.id)}
                                  className="inline font-semibold text-[#7A152E] hover:underline cursor-pointer select-none text-xs ml-1"
                                >
                                  See less
                                </button>
                              )}
                            </>
                          ) : (
                            <>
                              <span>{snippet}...</span>{' '}
                              <button
                                type="button"
                                onClick={() => toggleQna(item.id)}
                                className="inline font-semibold text-[#7A152E] hover:underline cursor-pointer select-none text-xs"
                              >
                                Read more
                              </button>
                            </>
                          )}
                        </p>

                        {/* Atelier Attribution & Helpful Count */}
                        <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-[11px] text-stone-400 border-t border-[#FAF5EE]">
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="font-medium text-[#7A152E]">
                              {item.author}
                            </span>
                            <span>•</span>
                            <span className="inline-flex items-center gap-1 text-[#8B6B38] bg-[#FAF6EE] px-2 py-0.5 rounded-full border border-[#E8DCC4] font-medium text-[10px]">
                              <Award className="w-2.5 h-2.5 text-[#C5A059]" />
                              <span>{item.badge}</span>
                            </span>
                          </div>

                          <button
                            type="button"
                            onClick={() => handleHelpfulQna(item.id)}
                            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all cursor-pointer border active:scale-95 ${
                              isVoted
                                ? 'bg-[#FAF0F2] border-[#7A152E] text-[#7A152E]'
                                : 'bg-[#FAF8F5] border-[#EAE4DC] hover:border-[#7A152E]/30 text-stone-700 hover:text-[#7A152E]'
                            }`}
                          >
                            <ThumbsUp className="w-3 h-3 text-[#C5A059]" />
                            <span>Helpful ({item.helpfulCount + (isVoted ? 1 : 0)})</span>
                          </button>
                        </div>
                      </div>
                    </div>

                  </div>
                );
              })}
            </div>
          ) : (
            <div className="py-12 text-center space-y-3 border-t border-[#EAE4DC]">
              <HelpCircle className="w-10 h-10 text-[#C5A059] mx-auto opacity-70" />
              <p className="text-sm font-medium text-stone-800">
                No answers found matching "{qnaSearchQuery}"
              </p>
              <p className="text-xs text-stone-500 max-w-md mx-auto font-light">
                Have a specific query regarding custom sizing, hallmarking or care? Our concierge desk will answer within 2 hours.
              </p>
              <button
                type="button"
                onClick={() => {
                  setQuestionForm(prev => ({ ...prev, question: qnaSearchQuery }));
                  setShowAskQuestionModal(true);
                }}
                className="px-5 py-2 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold rounded-xl shadow-xs transition-colors inline-flex items-center gap-2 cursor-pointer mt-2"
              >
                <HelpCircle className="w-3.5 h-3.5 text-[#EAD7AE]" />
                <span>Ask Atelier Team Directly</span>
              </button>
            </div>
          )}

          {/* Concierge Desk Help Banner */}
          <div className="mt-8 p-4 sm:p-5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#FAF0F2] text-[#7A152E] border border-[#EAD5DA] flex items-center justify-center shrink-0">
                <Award className="w-5 h-5 text-[#7A152E]" />
              </div>
              <div>
                <h5 className="text-xs sm:text-sm font-semibold text-stone-900">
                  Have a bespoke inquiry about custom sizing, engraving, or gold hallmarking?
                </h5>
                <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5 font-light">
                  Our master silversmiths and concierge desk respond to all inquiries within 2 hours.
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setShowAskQuestionModal(true)}
              className="px-4 py-2 bg-white hover:bg-[#FAF8F5] text-[#7A152E] text-xs font-semibold rounded-xl border border-[#7A152E]/30 shadow-2xs transition-all shrink-0 cursor-pointer self-start sm:self-auto inline-flex items-center gap-1.5 group"
            >
              <span>Ask Concierge Desk</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
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
                if (!reviewForm.comment.trim()) {
                  showToast('Please enter your review comment before submitting.', 'info');
                  return;
                }
                const newRev = {
                  id: 'rev-' + Date.now(),
                  name: reviewForm.name.trim() || 'Verified Collector',
                  avatar: (reviewForm.name.trim() || 'VC').slice(0, 2).toUpperCase(),
                  location: 'India',
                  rating: reviewForm.rating || 5,
                  headline: reviewForm.rating === 5 ? 'Exceptional Atelier Craftsmanship!' : 'Verified Customer Review',
                  comment: reviewForm.comment.trim(),
                  date: 'Just now',
                  verified: true,
                  helpfulCount: 0,
                  metal: '925 Sterling Silver',
                  finish: 'Official Hallmark'
                };
                setReviewsList(prev => [newRev, ...prev]);
                showToast('Thank you! Your verified review has been published.');
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
          RING & JEWELRY SIZE GUIDE MODAL
          ======================================================== */}
      {showSizeGuide && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="relative w-full max-w-lg bg-white rounded-2xl p-6 sm:p-7 shadow-2xl border border-[#EAE4DC] max-h-[90vh] overflow-y-auto">
            <button
              onClick={() => setShowSizeGuide(false)}
              className="absolute top-4 right-4 p-2 text-stone-400 hover:text-stone-800 rounded-full hover:bg-stone-100 transition-colors cursor-pointer"
              aria-label="Close Size Guide"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 mb-1">
              <div className="w-8 h-8 rounded-full bg-[#7A152E]/10 flex items-center justify-center text-[#7A152E]">
                <Ruler className="w-4 h-4" />
              </div>
              <div>
                <h3 className="font-serif text-xl font-bold text-stone-900">
                  Ring Size Guide
                </h3>
                <p className="text-xs text-stone-500">
                  Standard Indian Ring Size Chart & Fitment Guide
                </p>
              </div>
            </div>

            {/* Indian Size Chart Table */}
            <div className="mt-4 border border-stone-200 rounded-xl overflow-hidden shadow-2xs">
              <table className="w-full text-left text-xs">
                <thead className="bg-[#FAF8F5] border-b border-stone-200 text-stone-800 font-semibold">
                  <tr>
                    <th className="py-2.5 px-3">Indian Size</th>
                    <th className="py-2.5 px-3">Inner Diameter</th>
                    <th className="py-2.5 px-3">Circumference</th>
                    <th className="py-2.5 px-3">Select</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-stone-100">
                  {[
                    { size: '10', dia: '15.9 mm', circ: '50.0 mm' },
                    { size: '12', dia: '16.5 mm', circ: '51.9 mm' },
                    { size: '14', dia: '17.2 mm', circ: '54.0 mm' },
                    { size: '16', dia: '17.8 mm', circ: '56.0 mm' },
                    { size: '18', dia: '18.5 mm', circ: '58.1 mm' },
                    { size: '20', dia: '19.1 mm', circ: '60.0 mm' }
                  ].map((row) => (
                    <tr
                      key={row.size}
                      onClick={() => {
                        setSelectedSize(row.size);
                        setShowSizeGuide(false);
                      }}
                      className={`cursor-pointer transition-colors ${
                        selectedSize === row.size
                          ? 'bg-[#7A152E]/10 font-bold text-[#7A152E]'
                          : 'hover:bg-stone-50 text-stone-700'
                      }`}
                    >
                      <td className="py-2 px-3 font-semibold">{row.size}</td>
                      <td className="py-2 px-3 text-stone-600">{row.dia}</td>
                      <td className="py-2 px-3 text-stone-600">{row.circ}</td>
                      <td className="py-2 px-3">
                        <button
                          type="button"
                          className={`text-[11px] px-2 py-0.5 rounded-md font-semibold cursor-pointer ${
                            selectedSize === row.size
                              ? 'bg-[#7A152E] text-white'
                              : 'bg-stone-100 text-stone-600 hover:bg-[#7A152E] hover:text-white'
                          }`}
                        >
                          {selectedSize === row.size ? 'Selected' : 'Choose'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* How to measure */}
            <div className="mt-4 p-3 rounded-xl bg-[#FAF8F5] border border-stone-200 text-xs space-y-1.5">
              <h4 className="font-semibold text-stone-900">How to find your ring size:</h4>
              <p className="text-stone-600 leading-relaxed">
                1. Take an existing ring that fits your intended finger comfortably.<br />
                2. Measure the <strong>inside diameter</strong> in millimeters (mm) with a ruler.<br />
                3. Match with the chart above. If you are between sizes, we recommend ordering the larger size.
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-stone-200 flex justify-end">
              <button
                type="button"
                onClick={() => setShowSizeGuide(false)}
                className="px-5 py-2 bg-[#7A152E] text-white text-xs font-bold rounded-xl hover:bg-[#590D1E] cursor-pointer"
              >
                Done
              </button>
            </div>
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
        className={`fixed bottom-3.5 left-4 right-4 max-w-sm mx-auto z-40 lg:hidden transition-all duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] ${
          showStickyCta
            ? 'translate-y-0 scale-100 opacity-100 pointer-events-auto'
            : 'translate-y-16 scale-90 opacity-0 pointer-events-none'
        }`}
      >
        <div className="backdrop-blur-2xl bg-[#FAF8F5]/95 border border-white/90 shadow-[0_16px_40px_rgba(0,0,0,0.18),0_2px_8px_rgba(122,21,46,0.1)] rounded-full p-1.5 flex items-center justify-center gap-2">
          <button
            type="button"
            onClick={handleAddToCart}
            className="flex-1 py-2.5 px-3 rounded-full border border-[#7A152E] text-[#7A152E] bg-white hover:bg-[#FAF8F5] text-xs sm:text-sm font-bold flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer shadow-2xs"
            title="Add to Cart"
          >
            <ShoppingBag className="w-4 h-4" />
            <span>Add to Cart</span>
          </button>

          <button
            type="button"
            onClick={handleBuyNow}
            className="flex-1 py-2.5 px-3 rounded-full bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs sm:text-sm font-bold flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer shadow-md tracking-wide"
          >
            <span>Buy Now</span>
          </button>
        </div>
      </aside>

    </div>
  );
};

