import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { useShop } from '../context/ShopContext';
import { ProductCard } from '../components/ProductCard';
import { TrustBadgesRow } from '../components/TrustBadges';
import { TRUST_PILLARS, CUSTOMER_REVIEWS } from '../data/catalog';
import { useDragScroll } from '../utils/useDragScroll';
import { GoldShoppingBag } from '../components/GoldShoppingBag';
import {
  ArrowRight,
  ChevronRight,
  Check,
  Shield,
  Award,
  RefreshCw,
  Truck,
  Lock,
  ShoppingBag,
  Play,
  Pause,
  X,
  Volume2,
  VolumeX,
  Eye,
  Heart,
  Star,
  Crown,
  ShieldCheck
} from 'lucide-react';

const HERO_BANNERS = [
  {
    id: 1,
    desktopImg: 'solystra_assets/banners/banner_pc_2.jpg',
    mobileImg: 'solystra_assets/banners/banner_mob_2.jpg',
    title: 'The 18K Gold Suite',
    subtitle: 'Layered tennis bracelets and kada cuffs in 18K Italian gold vermeil.',
    desc: 'Crafted in pure 925 sterling silver with a rich, radiant gold polish built for daily elegance.',
    tag: 'NEW ARRIVALS',
    cta: 'Shop Gold Suites',
    category: 'bracelets'
  },
  {
    id: 2,
    desktopImg: 'solystra_assets/banners/banner_blush_tones_pc.jpg',
    mobileImg: 'solystra_assets/banners/banner_blush_tones_mob.jpg',
    title: 'Blush Tones Collection',
    subtitle: 'Delicate pink enamel blossoms and brilliant solitaires.',
    desc: 'Feminine, radiant silhouettes handcrafted for everyday elegance and festive celebrations.',
    tag: 'MOST LOVED',
    cta: 'Explore Collection',
    category: 'necklaces'
  },
  {
    id: 3,
    desktopImg: 'solystra_assets/banners/banner_pc_3.jpg',
    mobileImg: 'solystra_assets/banners/banner_mob_3.jpg',
    title: 'Modern Classics',
    subtitle: 'Certified 925 silver bands, huggies and solitaires.',
    desc: 'Finished with dual-micron anti-tarnish rhodium for a lifetime of mirror brilliance.',
    tag: 'SIGNATURE PIECES',
    cta: 'Shop Classics',
    category: 'rings'
  },
  {
    id: 4,
    desktopImg: 'solystra_assets/banners/banner_gift_sets_pc.jpg',
    mobileImg: 'solystra_assets/banners/banner_gift_sets_mob.jpg',
    title: 'Signature Gift Sets',
    subtitle: 'Delivered in bespoke velvet keepsake vault with hallmark certificate.',
    desc: 'Complete jewelry sets paired for weddings, anniversaries, and personal milestones.',
    tag: 'GIFTING GUIDE',
    cta: 'Discover Gift Sets',
    category: 'complete_sets'
  }
];

// Architectural Zavya-Style Category Cards (Squircle Pods with Burgundy & Champagne Gold Halo)
const CATEGORY_CARDS = [
  {
    id: 'necklaces',
    name: 'Necklaces',
    count: '14 Designs',
    img: 'solystra_assets/categories/zavya_style/necklaces.png'
  },
  {
    id: 'earrings',
    name: 'Earrings',
    count: '10 Designs',
    img: 'solystra_assets/categories/zavya_style/earrings.png'
  },
  {
    id: 'bracelets',
    name: 'Bracelets',
    count: '12 Designs',
    img: 'solystra_assets/categories/zavya_style/bracelets.png'
  },
  {
    id: 'rings',
    name: 'Rings',
    count: '8 Designs',
    img: 'solystra_assets/categories/zavya_style/rings.png'
  },
  {
    id: 'anklets',
    name: 'Anklets',
    count: '6 Designs',
    img: 'solystra_assets/categories/zavya_style/anklets.png'
  },
  {
    id: 'complete_sets',
    name: 'Gift Suites',
    count: '6 Sets',
    img: 'solystra_assets/categories/zavya_style/complete_sets.png'
  },
  {
    id: 'chains',
    name: 'Chains',
    count: '8 Designs',
    img: 'solystra_assets/categories/zavya_style/chains.png'
  },
  {
    id: 'mangalsutras',
    name: 'Mangalsutra',
    count: '8 Designs',
    img: 'solystra_assets/categories/zavya_style/mangalsutras.png'
  },
  {
    id: 'nose_pins',
    name: 'Nose Pins',
    count: '6 Designs',
    img: 'solystra_assets/categories/zavya_style/nose_pins.png'
  },
  {
    id: 'mens_collection',
    name: "Men's Silver",
    count: '7 Designs',
    img: 'solystra_assets/categories/zavya_style/mens.png'
  }
];

// Top Curated Collections (Editorial tall portrait cards with signature script typography)
const TOP_COLLECTIONS = [
  {
    id: 'col-ombre',
    title: 'Ombre',
    subtitle: 'COLLECTION',
    desc: 'Gradient pink sapphires and warm rose vermeil cuffs.',
    img: '/solystra_assets/collections/collection_ombre.jpg',
    category: 'rings',
    tag: 'BESTSELLER'
  },
  {
    id: 'col-celestial',
    title: 'Celestial',
    subtitle: 'COLLECTION',
    desc: 'Starlight solitaire drops and cosmic pavé earrings.',
    img: '/solystra_assets/collections/collection_celestial.jpg',
    category: 'earrings',
    tag: 'NEW DROP'
  },
  {
    id: 'col-heart',
    title: 'Heart Echoes',
    subtitle: 'COLLECTION',
    desc: 'Romantic heart pendants and intertwined keepsake chains.',
    img: '/solystra_assets/collections/collection_heart.jpg',
    category: 'complete_sets',
    tag: 'ROMANCE'
  },
  {
    id: 'col-infinite',
    title: 'Infinite Bond',
    subtitle: 'COLLECTION',
    desc: 'Continuous loop cuffs and eternal silver tennis bracelets.',
    img: '/solystra_assets/collections/collection_infinite.jpg',
    category: 'bracelets',
    tag: 'GIFTING'
  },
  {
    id: 'col-ruby',
    title: 'Ruby Radiance',
    subtitle: 'COLLECTION',
    desc: 'Deep pigeon-blood rubies prong-set in 18K gold vermeil.',
    img: '/solystra_assets/collections/collection_ruby.jpg',
    category: 'rings',
    tag: 'ROYAL EDIT'
  },
  {
    id: 'col-studs',
    title: 'Solitaire Studs',
    subtitle: 'COLLECTION',
    desc: 'Brilliant round-cut Austrian crystal studs in pure 925 silver.',
    img: '/solystra_assets/collections/collection_studs.jpg',
    category: 'earrings',
    tag: 'TIMELESS'
  },
  {
    id: 'col-drops',
    title: 'Drop Elegance',
    subtitle: 'COLLECTION',
    desc: 'Graceful cascading silhouette earrings and matching pendants.',
    img: '/solystra_assets/collections/collection_drops.jpg',
    category: 'necklaces',
    tag: 'SIGNATURE'
  }
];

const OCCASIONS = TOP_COLLECTIONS;

// Multi-combo Curated Atelier Pairings with Delicate Glowing Hotspots & Model Imagery (Necklace + Earrings)
const STYLING_COMBOS = [
  {
    id: 'combo-1',
    name: 'Amethyst Floral Blossom Set',
    tag: 'ROSE GOLD VERMEIL',
    desc: 'Handcrafted floral blossom necklace paired with matching petal drop earrings.',
    editorialImg: '/solystra_assets/banners/banner_blush_tones_pc.jpg',
    imagePosition: 'object-[75%_center]',
    items: [
      {
        id: 'c1-item-1',
        productId: 'amethyst-bloom-necklace-set-925-sterling-silver',
        type: 'NECKLACE',
        name: 'Amethyst Bloom Floral Necklace',
        metal: 'Rose Gold Vermeil • Handcrafted Setting',
        price: 9585,
        mrp: 11981,
        image: '/solystra_assets/products/amethyst-bloom-necklace-set-925-sterling-silver/angle_1.png',
        hotspot: { x: 75.1, y: 55.0, label: 'Floral Blossom Necklace' }
      },
      {
        id: 'c1-item-2',
        productId: 'flora-band-hoops',
        type: 'EARRINGS',
        name: 'Blossom Petal Drop Earrings',
        metal: 'Rose Gold Vermeil • Double-Micron Rhodium',
        price: 2499,
        mrp: 3499,
        image: '/solystra_assets/categories/cat_earrings.png',
        hotspot: { x: 78.6, y: 27.1, label: 'Blossom Drop Earrings' }
      }
    ],
    bundlePrice: 12084,
    originalPrice: 15480,
    savings: 3396
  },
  {
    id: 'combo-2',
    name: 'Classic Solitaire Set',
    tag: 'PURE 925 STERLING SILVER',
    desc: 'Brilliant Austrian solitaire pendant paired with matching solitaire drop earrings.',
    editorialImg: '/solystra_assets/banners/banner_pc_1.jpg',
    imagePosition: 'object-[72%_center]',
    items: [
      {
        id: 'c2-item-1',
        productId: 'universal-embrace',
        type: 'NECKLACE',
        name: 'Universal Solitaire Drop Necklace',
        metal: 'Pure 925 Silver • Brilliant Cut Solitaire',
        price: 2799,
        mrp: 3999,
        image: '/solystra_assets/categories/cat_necklaces.png',
        hotspot: { x: 32.3, y: 76.2, pcX: 45.9, pcY: 83.9, label: 'Solitaire Pendant Necklace' }
      },
      {
        id: 'c2-item-2',
        productId: 'classic-knot-earrings',
        type: 'EARRINGS',
        name: 'Solitaire Drop Earrings',
        metal: 'Pure 925 Silver • Cushion Cut Drop',
        price: 2299,
        mrp: 3299,
        image: '/solystra_assets/categories/cat_earrings.png',
        hotspot: { x: 42.7, y: 40.6, pcX: 53.1, pcY: 44.6, label: 'Solitaire Drop Earrings' }
      }
    ],
    bundlePrice: 5098,
    originalPrice: 7298,
    savings: 2200
  },
  {
    id: 'combo-3',
    name: 'Gala Choker & Chandelier Set',
    tag: 'FINE EVENING WEAR',
    desc: 'Graduated tennis choker in pure silver paired with tiered chandelier drops.',
    editorialImg: '/solystra_assets/generated/cocktail_glam.jpg',
    imagePosition: 'object-center',
    items: [
      {
        id: 'c3-item-1',
        productId: 'golden-meadow-necklace-set-925-sterling-silver',
        type: 'NECKLACE',
        name: 'Grand Solitaire Tennis Choker',
        metal: 'Pure 925 Silver • Graduated Tennis Links',
        price: 5499,
        mrp: 7999,
        image: '/solystra_assets/categories/cat_necklaces.png',
        hotspot: { x: 52.5, y: 50.5, label: 'Graduated Tennis Choker' }
      },
      {
        id: 'c3-item-2',
        productId: 'greek-pattern-hoops',
        type: 'EARRINGS',
        name: 'Imperial Chandelier Drops',
        metal: 'Pure 925 Silver • Multi-Tier Drops',
        price: 3499,
        mrp: 4999,
        image: '/solystra_assets/categories/cat_earrings.png',
        hotspot: { x: 60.8, y: 34.5, label: 'Imperial Chandelier Drops' }
      }
    ],
    bundlePrice: 8998,
    originalPrice: 12998,
    savings: 4000
  }
];

// Video Reels for the Horizontal Video Side-Scroll
const VIDEO_REELS = [
  {
    id: 'reel-1',
    title: 'Aura Solitaire Drop Pendant',
    category: 'necklaces',
    metal: 'Pure 925 Sterling Silver',
    price: 2799,
    mrp: 3999,
    videoSrc: 'solystra_assets/videos/reel_01_pen-30277-g.mp4',
    productImage: 'zavya_assets/products/pendant/pen-30277-g/01_pen-30277-g.jpg',
    desc: 'Watch the 57-facet Austrian solitaire refract pure white fire under unedited studio lighting.'
  },
  {
    id: 'reel-2',
    title: 'Radiant Cascade Drop Hoops',
    category: 'earrings',
    metal: 'Double-Micron Rhodium',
    price: 2499,
    mrp: 3499,
    videoSrc: 'solystra_assets/videos/reel_02_ear-21096-g.mp4',
    productImage: 'zavya_assets/products/drop_earrings/ear-21096-g/07_ear-21096-g.jpg',
    desc: 'Seamless snap-lock closure and fluid movement designed for featherlight all-day wear.'
  },
  {
    id: 'reel-3',
    title: 'Imperial Link Tennis Bracelet',
    category: 'bracelets',
    metal: '18K Italian Gold Vermeil',
    price: 3899,
    mrp: 5499,
    videoSrc: 'solystra_assets/videos/reel_03_br-80505-g.mp4',
    productImage: 'zavya_assets/products/bracelet/br-80505-g/01_br-80505-g.jpg',
    desc: 'Individually articulated links that drape effortlessly around the wrist with a double safety clasp.'
  },
  {
    id: 'reel-4',
    title: 'Heart Solitaire Halo Studs',
    category: 'earrings',
    metal: '18K Gold & Pure Silver',
    price: 2199,
    mrp: 2999,
    videoSrc: 'solystra_assets/videos/reel_04_halo-heart.mp4',
    productImage: 'zavya_assets/products/diamond_stud_earrings/0-75-ct-halo-heart-solitaire-gold-stud-earring/01_0-75-ct-halo-heart-solitaire-gold-stud-earring.jpg',
    desc: 'Brilliant heart solitaire halo studs catching every ray of light with exceptional diamond clarity.'
  },
  {
    id: 'reel-5',
    title: 'Lambency Solitaire Diamond Ring',
    category: 'rings',
    metal: 'VVS Diamond Fire • 925 Silver',
    price: 3199,
    mrp: 4499,
    videoSrc: 'solystra_assets/videos/reel_05_lambency.mp4',
    productImage: 'zavya_assets/products/diamond_solitaire_ring/0-75-ct-lambency-solitaire-diamond-ring/01_0-75-ct-lambency-solitaire-diamond-ring.jpg',
    desc: 'Precision prong-set Austrian lab diamond solitaire displaying prismatic spectral dispersion.'
  },
  {
    id: 'reel-6',
    title: 'Golden Meadow Lariat Set',
    category: 'necklaces',
    metal: '18K Gold & 925 Silver',
    price: 4299,
    mrp: 5999,
    videoSrc: 'solystra_assets/videos/reel_06_nl-30455-g.mp4',
    productImage: 'zavya_assets/products/necklace/nl-30455-g/01_nl-30455-g.jpg',
    desc: 'Statement festive neckline brilliance paired with matching sparkling drop earrings.'
  },
  {
    id: 'reel-7',
    title: 'Celestial Solitaire Diamond Pendant',
    category: 'necklaces',
    metal: 'Pure 925 Sterling Silver',
    price: 2799,
    mrp: 3999,
    videoSrc: 'solystra_assets/videos/reel_07_celestial.mp4',
    productImage: 'zavya_assets/products/diamond_pendant/0-75-ct-celestial-solitaire-lab-grown-diamond-pendant-without-chain/01_0-75-ct-celestial-solitaire-lab-grown-diamond-pendant-without-chain.jpg',
    desc: 'A pure solitaire focal stone handset in an open gallery to maximize ambient light transmission.'
  },
  {
    id: 'reel-8',
    title: 'Peacock Rose Gold Kada Bangle',
    category: 'bracelets',
    metal: 'Rose Gold • Pure 925 Silver',
    price: 3699,
    mrp: 4999,
    videoSrc: 'solystra_assets/videos/reel_08_peacock.mp4',
    productImage: 'zavya_assets/products/kada_bracelet/peacock-925-sterling-silver-bracelet-in-rose-gold-valentine-hamper/01_peacock-925-sterling-silver-bracelet-in-rose-gold-valentine-hamper.jpg',
    desc: 'Sculpted artisan peacock motif cuffs finished with high-luster rose gold vermeil.'
  },
  {
    id: 'reel-9',
    title: 'Imperial Solid Kada Cuff',
    category: 'mens',
    metal: 'Pure 925 Solid Silver',
    price: 4599,
    mrp: 6499,
    videoSrc: 'solystra_assets/videos/reel_09_mens-bangle.mp4',
    productImage: 'zavya_assets/products/kada_bracelet_men/bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle/01_bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle.jpg',
    desc: 'Substantial solid 925 sterling silver kada cuff with precision beveled edges and high-gloss polish.'
  },
  {
    id: 'reel-10',
    title: 'Eternal Spark Keepsake Set',
    category: 'complete_sets',
    metal: 'Rose Gold Vermeil Ensemble',
    price: 4799,
    mrp: 6999,
    videoSrc: 'solystra_assets/videos/reel_10_eternal-spark.mp4',
    productImage: 'zavya_assets/products/jewellery_sets/eternal-spark-rose-gold-sterling-silver-jewellery-set/01_eternal-spark-rose-gold-sterling-silver-jewellery-set.jpg',
    desc: 'Harmonious necklace, earrings, and ring ensemble delivered in royal velvet keepsake vault.'
  },
  {
    id: 'reel-11',
    title: 'Infinity Charm Evil Eye Bracelet',
    category: 'bracelets',
    metal: 'Anti-Tarnish Rhodium Silver',
    price: 1899,
    mrp: 2599,
    videoSrc: 'solystra_assets/videos/reel_11_evil-eye.mp4',
    productImage: 'zavya_assets/products/evil_eye_bracelet/infinity-charm-rhodium-plated-bracelet-with-evil-eye-cubic-zirconia/01_infinity-charm-rhodium-plated-bracelet-with-evil-eye-cubic-zirconia.jpg',
    desc: 'Protective evil eye talisman framed with micro-pavé Austrian cubic zirconia.'
  },
  {
    id: 'reel-12',
    title: 'Rose Gold Glimmering Fusion Anklet',
    category: 'anklets',
    metal: 'Rose Gold & 925 Silver',
    price: 1999,
    mrp: 2799,
    videoSrc: 'solystra_assets/videos/reel_12_anklet.mp4',
    productImage: 'zavya_assets/products/anklets/rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama/01_rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama.jpg',
    desc: 'Whisper-soft chain with micro-beaded clusters and anti-tarnish protective sealing.'
  }
];

export const HomePage = ({ activeCategory, onSelectCategory }) => {
  const { PRODUCTS, addToCart, setIsCartOpen, setIsCheckoutOpen, showToast } = useShop();

  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedCategory, setSelectedCategory] = useState(activeCategory || 'all');
  const [selectedMaxPrice, setSelectedMaxPrice] = useState(null);
  const [viewFullCatalog, setViewFullCatalog] = useState(false);

  // Video modal state
  const [activeVideoModal, setActiveVideoModal] = useState(null);
  const [isVideoMuted, setIsVideoMuted] = useState(true);

  // Drag to scroll hooks for silky smooth desktop & mobile navigation
  const categoryDrag = useDragScroll({ isInfiniteLoop: false, momentum: true });
  const categoryScrollRef = categoryDrag.ref;

  const topCollectionsDrag = useDragScroll();
  const topCollectionsScrollRef = topCollectionsDrag.ref;

  const videoDrag = useDragScroll();
  const videoScrollRef = videoDrag.ref;

  const bestsellersScrollRef = useRef(null);
  const newlyLaunchedScrollRef = useRef(null);

  // Auto-scroll loop states for hands-free infinite exploration
  const isVideoInteracting = useRef(false);
  const videoAnimationId = useRef(null);
  const [activeHotspotId, setActiveHotspotId] = useState(null);

  const TRIPLE_TOP_COLLECTIONS = useMemo(() => [
    ...TOP_COLLECTIONS.map(c => ({ ...c, loopId: `${c.id}-set1` })),
    ...TOP_COLLECTIONS.map(c => ({ ...c, loopId: `${c.id}-set2` })),
    ...TOP_COLLECTIONS.map(c => ({ ...c, loopId: `${c.id}-set3` })),
  ], []);

  const TRIPLE_VIDEO_REELS = useMemo(() => [
    ...VIDEO_REELS.map(r => ({ ...r, loopId: `${r.id}-set1` })),
    ...VIDEO_REELS.map(r => ({ ...r, loopId: `${r.id}-set2` })),
    ...VIDEO_REELS.map(r => ({ ...r, loopId: `${r.id}-set3` })),
  ], []);

  useEffect(() => {
    if (activeCategory && activeCategory !== 'all') {
      setSelectedCategory(activeCategory);
      setViewFullCatalog(true);
    }
  }, [activeCategory]);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % HERO_BANNERS.length);
    }, 6000);
    return () => clearInterval(timer);
  }, []);

  const handleCategorySelect = (cat) => {
    setSelectedCategory(cat);
    if (onSelectCategory) {
      onSelectCategory(cat);
    }
    setViewFullCatalog(true);
    document.getElementById('bestsellers-showcase')?.scrollIntoView({ behavior: 'smooth' });
  };

  const handlePriceFilter = (maxPrice) => {
    setSelectedMaxPrice(maxPrice);
    setSelectedCategory('all');
    setViewFullCatalog(true);
    document.getElementById('bestsellers-showcase')?.scrollIntoView({ behavior: 'smooth' });
  };

  // Top Collections: Track active centered card on mobile for dynamic peek-and-scale effect
  const [activeCollectionIndex, setActiveCollectionIndex] = useState(7);
  const isTopCollectionsScrollTicking = useRef(false);

  const handleTopCollectionsScroll = useCallback(() => {
    if (isTopCollectionsScrollTicking.current) return;
    isTopCollectionsScrollTicking.current = true;

    requestAnimationFrame(() => {
      const el = topCollectionsScrollRef.current;
      if (el) {
        const containerCenter = el.scrollLeft + el.clientWidth / 2;
        const cards = el.querySelectorAll('[data-collection-card]');
        
        let closestIdx = 7;
        let minDiff = Infinity;

        for (let i = 0; i < cards.length; i++) {
          const card = cards[i];
          const cardCenter = card.offsetLeft + card.clientWidth / 2;
          const diff = Math.abs(containerCenter - cardCenter);
          if (diff < minDiff) {
            minDiff = diff;
            closestIdx = i;
          }
        }

        setActiveCollectionIndex((prev) => (prev !== closestIdx ? closestIdx : prev));

        // Seamless continuous loop wrap
        const singleSet = el.scrollWidth / 3;
        if (singleSet > 50) {
          if (el.scrollLeft < 30) {
            el.scrollLeft += singleSet;
          } else if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          }
        }
      }
      isTopCollectionsScrollTicking.current = false;
    });
  }, [topCollectionsScrollRef]);

  const handleCollectionCardClick = useCallback((col, idx) => {
    if (idx !== activeCollectionIndex) {
      const el = topCollectionsScrollRef.current;
      if (el) {
        const cards = el.querySelectorAll('[data-collection-card]');
        if (cards[idx]) {
          cards[idx].scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
        }
      }
      return;
    }
    handleCategorySelect(col.category);
  }, [activeCollectionIndex, topCollectionsScrollRef]);

  // Helper function for left/right slide scrolling with auto continuous looping
  const scrollLoop = (ref, direction, amount = 340) => {
    const el = ref.current;
    if (!el) return;

    const singleSetWidth = el.scrollWidth / 3;

    if (direction < 0) {
      if (el.scrollLeft <= 25) {
        el.style.scrollBehavior = 'auto';
        el.scrollLeft = el.scrollLeft + singleSetWidth;
      }
    } else {
      if (el.scrollLeft >= singleSetWidth * 2 - 25) {
        el.style.scrollBehavior = 'auto';
        el.scrollLeft = el.scrollLeft - singleSetWidth;
      }
    }

    el.scrollBy({ left: direction * amount, behavior: 'smooth' });
  };

  // Attach seamless infinite circular boundary protection and quiet re-centering for collections scrollers
  useEffect(() => {
    const scrollers = [
      topCollectionsScrollRef
    ];

    const initPositions = () => {
      scrollers.forEach((ref) => {
        const el = ref.current;
        if (!el) return;
        const singleSet = el.scrollWidth / 3;
        if (singleSet > 50 && (el.scrollLeft < 50 || el.scrollLeft >= singleSet * 2.5)) {
          el.scrollLeft = singleSet;
        }
      });
    };

    initPositions();
    const t1 = setTimeout(initPositions, 150);
    const t2 = setTimeout(initPositions, 600);
    window.addEventListener('resize', initPositions);

    const cleanups = scrollers.map((ref) => {
      const el = ref.current;
      if (!el) return null;

      let scrollTimeout = null;

      const handleScroll = () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
          const singleSet = el.scrollWidth / 3;
          if (singleSet <= 50) return;

          if (el.scrollLeft < 30) {
            el.scrollLeft += singleSet;
          } else if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          }
        }, 120);
      };

      el.addEventListener('scroll', handleScroll, { passive: true });
      return () => {
        el.removeEventListener('scroll', handleScroll);
        clearTimeout(scrollTimeout);
      };
    });

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      window.removeEventListener('resize', initPositions);
      cleanups.forEach((cleanup) => cleanup && cleanup());
    };
  }, []);

  // Bulletproof requestAnimationFrame smooth scroll engine for video reels
  const smoothScrollVideo = (el, amount, duration = 650) => {
    if (!el) return;
    if (videoAnimationId.current) {
      cancelAnimationFrame(videoAnimationId.current);
      videoAnimationId.current = null;
    }

    const start = el.scrollLeft;
    const singleSet = el.scrollWidth / 3;

    let adjustedStart = start;
    if (singleSet > 100) {
      if (amount > 0 && start >= singleSet * 2 - 20) {
        adjustedStart = start - singleSet;
        el.scrollLeft = adjustedStart;
      } else if (amount < 0 && start <= 40) {
        adjustedStart = start + singleSet;
        el.scrollLeft = adjustedStart;
      }
    }

    const startTime = performance.now();

    const step = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // easeInOutCubic for organic, luxury glide
      const ease = progress < 0.5
        ? 4 * progress * progress * progress
        : 1 - Math.pow(-2 * progress + 2, 3) / 2;

      el.scrollLeft = adjustedStart + (amount * ease);

      if (progress < 1 && !isVideoInteracting.current) {
        videoAnimationId.current = requestAnimationFrame(step);
      } else {
        videoAnimationId.current = null;
        if (singleSet > 100) {
          if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          } else if (el.scrollLeft < 20) {
            el.scrollLeft += singleSet;
          }
        }
      }
    };

    videoAnimationId.current = requestAnimationFrame(step);
  };

  // Handle manual left/right navigation for video reels
  const handleVideoScroll = (direction) => {
    const el = videoScrollRef.current;
    if (!el) return;
    const firstCard = el.querySelector(':scope > div');
    const cardWidth = firstCard ? firstCard.offsetWidth : (el.clientWidth < 640 ? 205 : 255);
    const gap = el.clientWidth < 640 ? 16 : 20;
    const step = cardWidth + gap;

    smoothScrollVideo(el, direction * step, 500);
  };

  // Dedicated Video Reels: Silk-smooth continuous infinite glide without stops/breaks
  useEffect(() => {
    const el = videoScrollRef.current;
    if (!el) return;

    let animId = null;
    let isHoverPaused = false;
    const scrollSpeed = 0.75; // Calm, continuous luxury marquee glide (~45px/sec)

    // Center to middle set initially
    const initVideoPos = () => {
      const singleSet = el.scrollWidth / 3;
      if (singleSet > 50 && (el.scrollLeft < 50 || el.scrollLeft >= singleSet * 2.2)) {
        el.scrollLeft = singleSet;
      }
    };

    initVideoPos();
    const t1 = setTimeout(initVideoPos, 200);
    const t2 = setTimeout(initVideoPos, 600);

    const step = () => {
      if (!isHoverPaused && !isVideoInteracting.current) {
        el.scrollLeft += scrollSpeed;
        const singleSet = el.scrollWidth / 3;
        if (singleSet > 50) {
          if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          } else if (el.scrollLeft <= 10) {
            el.scrollLeft += singleSet;
          }
        }
      }
      animId = requestAnimationFrame(step);
    };

    animId = requestAnimationFrame(step);

    const handleMouseEnter = () => { isHoverPaused = true; };
    const handleMouseLeave = () => { isHoverPaused = false; };
    const handleTouchStart = () => { isVideoInteracting.current = true; };
    const handleTouchEnd = () => {
      setTimeout(() => { isVideoInteracting.current = false; }, 400);
    };

    el.addEventListener('mouseenter', handleMouseEnter);
    el.addEventListener('mouseleave', handleMouseLeave);
    el.addEventListener('touchstart', handleTouchStart, { passive: true });
    el.addEventListener('touchend', handleTouchEnd, { passive: true });

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
      if (animId) cancelAnimationFrame(animId);
      el.removeEventListener('mouseenter', handleMouseEnter);
      el.removeEventListener('mouseleave', handleMouseLeave);
      el.removeEventListener('touchstart', handleTouchStart);
      el.removeEventListener('touchend', handleTouchEnd);
    };
  }, []);


  // Top 4 Bestsellers for the curated home section (1 clean row of 4 on desktop, 2x2 on mobile)
  const bestsellers = useMemo(() => {
    return PRODUCTS.filter((p) => p.badge === 'Bestseller' || p.badge === 'Atelier Gala').slice(0, 4);
  }, [PRODUCTS]);

  // Newly Launched pieces (6 items for rich carousel display)
  const newlyLaunchedProducts = useMemo(() => {
    const list = PRODUCTS.filter((p) => p.isNew || p.badge === 'Newly Launched');
    return list.length >= 6 ? list.slice(0, 6) : PRODUCTS.slice(0, 6);
  }, [PRODUCTS]);

  const tripleNewlyLaunched = useMemo(() => [
    ...newlyLaunchedProducts,
    ...newlyLaunchedProducts,
    ...newlyLaunchedProducts
  ], [newlyLaunchedProducts]);

  useEffect(() => {
    const el = newlyLaunchedScrollRef.current;
    if (!el) return;
    const singleSet = el.scrollWidth / 3;
    if (singleSet > 0) {
      el.scrollLeft = singleSet;
    }
  }, [newlyLaunchedProducts]);

  const handleNewlyLaunchedScroll = () => {
    const el = newlyLaunchedScrollRef.current;
    if (!el) return;
    const singleSet = el.scrollWidth / 3;
    if (singleSet <= 0) return;
    if (el.scrollLeft < 15) {
      el.scrollLeft += singleSet;
    } else if (el.scrollLeft >= singleSet * 2 - 15) {
      el.scrollLeft -= singleSet;
    }
  };

  // Filtered list when user explores full catalog (with dedicated Gold, Silver & Price support)
  const filteredProducts = useMemo(() => {
    let list = [...PRODUCTS];
    if (selectedMaxPrice) {
      list = list.filter((p) => p.price <= selectedMaxPrice);
    }
    if (selectedCategory !== 'all') {
      if (selectedCategory === 'bestseller') {
        list = list.filter((p) => p.badge === 'Bestseller' || p.badge === 'Atelier Gala');
      } else if (selectedCategory === 'new_arrivals') {
        list = list.filter((p) => p.isNew || p.badge === 'Newly Launched');
      } else if (selectedCategory === 'complete_sets') {
        list = list.filter((p) => p.name.toLowerCase().includes('set') || p.category === 'necklaces');
      } else if (selectedCategory === 'gold') {
        list = list.filter((p) => 
          (p.metals && p.metals.some(m => m.toLowerCase().includes('gold') && !m.toLowerCase().includes('rose'))) ||
          p.name.toLowerCase().includes('gold') ||
          p.desc?.toLowerCase().includes('gold') ||
          p.category === 'bracelets'
        );
      } else if (selectedCategory === 'silver') {
        list = list.filter((p) => 
          (p.metals && p.metals.some(m => m.toLowerCase().includes('silver'))) ||
          p.name.toLowerCase().includes('silver') ||
          p.desc?.toLowerCase().includes('silver') ||
          p.category === 'rings' ||
          p.category === 'necklaces'
        );
      } else if (selectedCategory === 'rose_gold') {
        list = list.filter((p) => 
          (p.metals && p.metals.some(m => m.toLowerCase().includes('rose'))) ||
          p.name.toLowerCase().includes('rose') ||
          p.desc?.toLowerCase().includes('rose')
        );
      } else if (selectedCategory === 'mangalsutras') {
        list = list.filter((p) => p.category === 'necklaces');
      } else if (selectedCategory === 'nose_pins') {
        list = list.filter((p) => p.category === 'earrings');
      } else if (selectedCategory === 'mens_collection') {
        list = list.filter((p) => p.category === 'bracelets' || p.category === 'rings');
      } else {
        list = list.filter((p) => p.category === selectedCategory);
      }
    }
    return list;
  }, [PRODUCTS, selectedCategory, selectedMaxPrice]);

  // Multi-combo state with auto-slide timer
  const [currentComboIndex, setCurrentComboIndex] = useState(0);
  const [isComboPaused, setIsComboPaused] = useState(false);

  useEffect(() => {
    if (isComboPaused) return;
    const timer = setInterval(() => {
      setCurrentComboIndex((prev) => (prev + 1) % STYLING_COMBOS.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [isComboPaused, currentComboIndex]);

  const activeCombo = STYLING_COMBOS[currentComboIndex];

  const handleAddCurrentComboToBag = () => {
    activeCombo.items.forEach((item) => {
      const matched = PRODUCTS.find((p) => p.id === item.productId || p.name.toLowerCase().includes(item.name.toLowerCase().split(' ')[0])) || PRODUCTS[0];
      addToCart(matched, item.metal, null, '', 1);
    });
    showToast(`"${activeCombo.name}" (${activeCombo.items.length} pieces) added to your bag!`);
    setIsCartOpen(true);
  };

  const handleAddVideoProduct = (reel) => {
    const matchedProduct = PRODUCTS.find(
      (p) => p.name.toLowerCase().includes(reel.title.toLowerCase().split(' ')[0]) || p.category === reel.category
    ) || PRODUCTS[0];
    addToCart(matchedProduct, reel.metal, null, '', 1);
    showToast(`${reel.title} has been added to your bag!`);
    setIsCartOpen(true);
  };

  const handleBuyNowVideoProduct = (reel) => {
    const matchedProduct = PRODUCTS.find(
      (p) => p.name.toLowerCase().includes(reel.title.toLowerCase().split(' ')[0]) || p.category === reel.category
    ) || PRODUCTS[0];
    addToCart(matchedProduct, reel.metal, null, '', 1);
    showToast(`Proceeding to checkout with ${reel.title}...`);
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
    if (window.location.hash !== '#/checkout') {
      window.location.hash = '#/checkout';
    }
  };

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] overflow-x-hidden font-sans">
      
      {/* ========================================================
          1. HERO CAMPAIGN BANNER CAROUSEL
          ======================================================== */}
      <section className="relative w-full overflow-hidden bg-stone-900 border-b border-stone-200">
        <div className="relative w-full aspect-[4/5] sm:aspect-[21/9] lg:aspect-[24/10] min-h-[460px] sm:min-h-[480px] lg:min-h-[520px] max-h-[640px]">
          {HERO_BANNERS.map((banner, idx) => (
            <div
              key={banner.id}
              className={`absolute inset-0 transition-opacity duration-700 ease-in-out ${
                idx === currentSlide ? 'opacity-100 z-10' : 'opacity-0 z-0 pointer-events-none'
              }`}
            >
              {/* Responsive picture */}
              <picture>
                <source media="(max-width: 640px)" srcSet={banner.mobileImg} />
                <img
                  src={banner.desktopImg}
                  alt={banner.title}
                  className="w-full h-full object-cover object-center block"
                  loading={idx === 0 ? 'eager' : 'lazy'}
                />
              </picture>

              {/* Gradient overlays for crystal clear text legibility */}
              <div className="absolute inset-0 bg-gradient-to-r from-black/85 via-black/45 to-transparent hidden sm:block pointer-events-none" />
              <div className="absolute inset-0 bg-gradient-to-t from-black/95 via-black/60 to-black/35 sm:hidden pointer-events-none" />

              {/* Editorial Text Overlay */}
              <div className="absolute inset-0 z-10 flex items-center">
                <div className="max-w-7xl w-full mx-auto px-6 sm:px-10 lg:px-14">
                  <div className="max-w-xl text-left">
                    <span className="inline-block text-[10.5px] sm:text-xs tracking-widest text-[#F5E6CC] uppercase font-semibold mb-1.5 sm:mb-3 drop-shadow-md">
                      {banner.tag}
                    </span>

                    <h2 className="font-serif text-2xl xs:text-[26px] sm:text-4xl md:text-5xl lg:text-6xl text-white font-normal leading-[1.15] sm:leading-[1.1] tracking-tight drop-shadow-[0_3px_12px_rgba(0,0,0,0.8)] max-w-full">
                      {banner.title}
                    </h2>

                    <p className="text-xs sm:text-base lg:text-lg text-stone-100 mt-1.5 sm:mt-3 leading-snug sm:leading-relaxed font-light drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)] max-w-lg line-clamp-2 sm:line-clamp-none">
                      {banner.subtitle}
                    </p>

                    <div className="mt-9 sm:mt-7 flex items-center gap-4">
                      <button
                        onClick={() => {
                          if (banner.category && onSelectCategory) {
                            onSelectCategory(banner.category);
                          }
                          setViewFullCatalog(true);
                          document.getElementById('bestsellers-showcase')?.scrollIntoView({ behavior: 'smooth' });
                        }}
                        className="inline-flex items-center gap-2 px-5 sm:px-8 py-2.5 sm:py-3 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs sm:text-sm font-medium rounded-lg shadow-lg hover:shadow-xl transition-all cursor-pointer"
                      >
                        <span>{banner.cta}</span>
                        <ArrowRight className="w-4 h-4 text-white/90" />
                      </button>

                      <button
                        onClick={() => {
                          window.location.hash = '#/products';
                        }}
                        className="hidden sm:inline-flex items-center text-xs font-medium tracking-wide text-white/90 hover:text-white underline underline-offset-4 decoration-[#C5A059] py-3 px-2 transition-colors cursor-pointer"
                      >
                        Explore All Pieces
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Dots Indicator */}
          <div className="absolute bottom-4 inset-x-0 z-20 flex justify-center gap-2">
            {HERO_BANNERS.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrentSlide(i)}
                className={`h-1.5 rounded-full transition-all duration-300 cursor-pointer ${
                  i === currentSlide ? 'w-7 bg-[#C5A059] shadow-xs' : 'w-2 bg-white/40 hover:bg-white/70'
                }`}
                aria-label={`Slide ${i + 1}`}
              />
            ))}
          </div>
        </div>
      </section>

      {/* ========================================================
          2. TRUST BADGES STRIP (Directly Below Hero Banner)
          ======================================================== */}
      <section className="py-2 sm:py-3 bg-white border-b border-[#EAE4DC] shadow-[0_2px_10px_rgba(0,0,0,0.02)]">
        <div className="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
          <TrustBadgesRow variant="home" />
        </div>
      </section>

      {/* ========================================================
          3. CATEGORIES: 6 FEATURED ON PC + EXPLORE CATEGORIES REDIRECT
          ======================================================== */}
      <section className="py-3 sm:py-5 bg-white border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-2.5 sm:px-6 lg:px-8">
          
          {/* Header with Title and "Explore Categories" Action */}
          <div className="flex items-center justify-between mb-3 sm:mb-4 px-1">
            <div>
              <span className="text-[10px] sm:text-[10.5px] uppercase tracking-widest text-[#7A152E] font-semibold block mb-0.5">
                SHOP BY CATEGORY
              </span>
              <h2 className="font-serif text-lg sm:text-2xl md:text-3xl text-stone-900 font-normal">
                Explore by Category
              </h2>
            </div>

            {/* Redirect to Categories Page with Full-Size Cards */}
            <button
              type="button"
              onClick={() => {
                window.location.hash = '#/categories';
              }}
              className="inline-flex items-center gap-1 sm:gap-1.5 text-xs sm:text-sm font-semibold text-[#7A152E] hover:text-[#590D1E] group transition-colors cursor-pointer py-1 px-2 -mr-2 rounded-lg hover:bg-[#FAF0F2]"
            >
              <span>Explore Categories</span>
              <ChevronRight className="w-3.5 h-3.5 sm:w-4 sm:h-4 group-hover:translate-x-0.5 transition-transform" />
            </button>
          </div>

          {/* PC Layout: Only these 6 categories in a clean, non-scrolling 6-column grid */}
          <div className="hidden md:grid md:grid-cols-6 gap-3.5 lg:gap-5 pt-1 pb-1">
            {CATEGORY_CARDS.slice(0, 6).map((cat) => {
              const isSelected = selectedCategory === cat.id;
              return (
                <div
                  key={cat.id}
                  onClick={() => handleCategorySelect(cat.id)}
                  className="group cursor-pointer flex flex-col items-center select-none"
                >
                  {/* Zavya-Style Squircle Card with Aurelia Royal Burgundy & Champagne Gold Gradient Halo */}
                  <div className={`w-full relative p-[2px] rounded-[22px] lg:rounded-[26px] bg-gradient-to-tr transition-all duration-300 ${
                    isSelected 
                      ? 'from-[#7A152E] via-[#C5A059] to-[#7A152E] shadow-[0_6px_20px_rgba(122,21,46,0.25)] scale-[1.03]' 
                      : 'from-[#7A152E]/80 via-[#D4AF37] to-[#F6E3B8] group-hover:from-[#D4AF37] group-hover:via-[#F6E3B8] group-hover:to-[#7A152E] shadow-2xs group-hover:shadow-[0_8px_20px_rgba(122,21,46,0.18)] group-hover:-translate-y-1'
                  }`}>
                    <div className="w-full aspect-square rounded-[20px] lg:rounded-[24px] overflow-hidden bg-white relative flex items-center justify-center border border-white/60">
                      <img
                        src={cat.img}
                        alt={cat.name}
                        draggable="false"
                        className="w-full h-full object-cover group-hover:scale-108 transition-transform duration-500 block pointer-events-none"
                        loading="lazy"
                      />

                      {/* Ambient Specular Hover Sheen */}
                      <div className="absolute inset-0 bg-gradient-to-t from-[#7A152E]/15 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </div>
                  </div>

                  {/* Clean Centered Typography */}
                  <span className={`font-serif text-[13px] lg:text-[15px] transition-colors text-center mt-2.5 line-clamp-1 tracking-tight ${
                    isSelected 
                      ? 'text-[#7A152E] font-bold' 
                      : 'text-stone-900 font-medium group-hover:text-[#7A152E]'
                  }`}>
                    {cat.name}
                  </span>
                </div>
              );
            })}
          </div>

          {/* Mobile Layout: Buttery-smooth, lag-free touch-swipe row of categories + Explore All Card */}
          <div
            ref={categoryScrollRef}
            {...categoryDrag.dragProps}
            className="md:hidden flex flex-nowrap gap-3 sm:gap-4 overflow-x-auto hide-scrollbar pb-2.5 pt-1 px-2.5 sm:px-4 cursor-grab active:cursor-grabbing select-none overscroll-x-contain touch-pan-x [-webkit-overflow-scrolling:touch] scroll-smooth"
          >
            {CATEGORY_CARDS.slice(0, 6).map((cat) => {
              const isSelected = selectedCategory === cat.id;
              return (
                <div
                  key={cat.id}
                  onClick={categoryDrag.handleItemClick(() => handleCategorySelect(cat.id))}
                  className="w-[76px] xs:w-[84px] sm:w-[96px] shrink-0 group cursor-pointer flex flex-col items-center select-none"
                >
                  <div className={`w-full relative p-[1.5px] rounded-[18px] bg-gradient-to-tr transition-all duration-300 ${
                    isSelected
                      ? 'from-[#7A152E] via-[#C5A059] to-[#7A152E] shadow-[0_4px_14px_rgba(122,21,46,0.2)]'
                      : 'from-[#7A152E]/85 via-[#D4AF37] to-[#F6E3B8] shadow-2xs'
                  }`}>
                    <div className="w-full aspect-square rounded-[16.5px] overflow-hidden bg-white relative flex items-center justify-center border border-white/60">
                      <img
                        src={cat.img}
                        alt={cat.name}
                        draggable="false"
                        className="w-full h-full object-cover block pointer-events-none"
                        loading="lazy"
                      />
                    </div>
                  </div>

                  <span className={`font-serif text-[10.5px] xs:text-[11.5px] sm:text-[12.5px] text-center mt-1.5 line-clamp-1 tracking-tight ${
                    isSelected ? 'text-[#7A152E] font-bold' : 'text-stone-900 font-semibold'
                  }`}>
                    {cat.name}
                  </span>
                </div>
              );
            })}

            {/* Explore All Card on Mobile */}
            <div
              onClick={categoryDrag.handleItemClick(() => {
                window.location.hash = '#/categories';
              })}
              className="w-[76px] xs:w-[84px] sm:w-[96px] shrink-0 group cursor-pointer flex flex-col items-center select-none"
            >
              <div className="w-full relative p-[1.5px] rounded-[18px] bg-gradient-to-tr from-[#7A152E]/40 via-[#D4AF37]/50 to-[#7A152E]/40 shadow-2xs">
                <div className="w-full aspect-square rounded-[16.5px] bg-[#FAF8F5] flex flex-col items-center justify-center p-2 text-center border border-[#EAE4DC]">
                  <div className="w-6 h-6 rounded-full bg-[#7A152E]/10 flex items-center justify-center mb-1">
                    <ChevronRight className="w-3.5 h-3.5 text-[#7A152E]" />
                  </div>
                  <span className="text-[8px] font-bold uppercase tracking-wider text-[#7A152E]">
                    Explore
                  </span>
                </div>
              </div>
              <span className="font-serif text-[10.5px] xs:text-[11.5px] sm:text-[12.5px] font-semibold text-[#7A152E] text-center mt-1.5 line-clamp-1 tracking-tight">
                View All
              </span>
            </div>
          </div>

        </div>
      </section>

      {/* ========================================================
          4. BEST SELLERS SHOWCASE
          ======================================================== */}
      <section id="bestsellers-showcase" className="py-4 sm:py-6 bg-[#FAF8F5] border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-3 pb-2 border-b border-[#EAE4DC] gap-3">
            <div>
              <span className="text-xs uppercase tracking-widest text-[#7A152E] font-semibold block mb-1">
                {viewFullCatalog ? 'FULL CATALOG' : 'BESTSELLERS'}
              </span>
              <h2 className="font-serif text-2xl sm:text-4xl font-normal text-stone-900">
                {viewFullCatalog 
                  ? `${selectedCategory === 'all' ? 'All Handcrafted Designs' : selectedCategory === 'gold' ? '18K Gold Vermeil' : selectedCategory === 'silver' ? 'Pure 925 Sterling Silver' : selectedCategory === 'rose_gold' ? 'Rose Gold Floral' : selectedCategory} Collection` 
                  : 'Our Most Loved Pieces'}
              </h2>
            </div>

            {/* Filter Pills ONLY appear if viewing full catalog */}
            {viewFullCatalog && (
              <div className="flex flex-wrap items-center gap-1.5">
                {selectedMaxPrice && (
                  <button
                    onClick={() => setSelectedMaxPrice(null)}
                    className="px-3 py-1.5 rounded-full text-xs font-semibold bg-[#7A152E] text-white flex items-center gap-1.5 shadow-xs hover:bg-[#590D1E] transition-colors cursor-pointer"
                  >
                    <span>Under ₹{selectedMaxPrice.toLocaleString('en-IN')}</span>
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
                {[
                  { id: 'all', label: 'All' },
                  { id: 'new_arrivals', label: 'Newly Launched' },
                  { id: 'bestseller', label: 'Bestsellers' },
                  { id: 'gold', label: '18K Gold' },
                  { id: 'silver', label: '925 Silver' },
                  { id: 'necklaces', label: 'Necklaces' },
                  { id: 'rings', label: 'Rings' },
                  { id: 'bracelets', label: 'Bracelets' },
                  { id: 'earrings', label: 'Earrings' },
                  { id: 'complete_sets', label: 'Gift Sets' }
                ].map((cat) => (
                  <button
                    key={cat.id}
                    onClick={() => {
                      setSelectedCategory(cat.id);
                    }}
                    className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors cursor-pointer ${
                      selectedCategory === cat.id
                        ? 'bg-[#7A152E] text-white shadow-xs'
                        : 'bg-stone-100 text-stone-700 hover:bg-stone-200'
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Grid: 4 in a row on Desktop (lg:grid-cols-4), 2 in a row on Mobile (grid-cols-2) */}
          <div
            ref={bestsellersScrollRef}
            className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 sm:gap-6"
          >
            {(viewFullCatalog ? filteredProducts : bestsellers).map((product) => (
              <div key={product.id} className="w-full">
                <ProductCard product={product} />
              </div>
            ))}
          </div>

          {/* Toggle Button: View All Designs */}
          {!viewFullCatalog && (
            <div className="mt-12 text-center">
              <button
                onClick={() => {
                  window.location.hash = '#/products';
                }}
                className="px-8 py-3.5 bg-white hover:bg-stone-50 text-[#7A152E] border border-stone-300 font-medium text-xs sm:text-sm rounded-xl transition-all shadow-sm hover:shadow-md cursor-pointer inline-flex items-center gap-2"
              >
                <span>Explore Full Catalog</span>
                <ArrowRight className="w-4 h-4 text-[#7A152E]" />
              </button>
            </div>
          )}

          {viewFullCatalog && (
            <div className="mt-12 text-center">
              <button
                onClick={() => setViewFullCatalog(false)}
                className="px-6 py-2.5 text-xs text-stone-500 hover:text-stone-900 underline cursor-pointer"
              >
                Collapse to Curated Pieces
              </button>
            </div>
          )}

        </div>
      </section>

      {/* ========================================================
          SHOP BY PRICE POINTS: ZAVYA-STYLE LUXURY GIFT BOX CARDS
          ======================================================== */}
      <section className="py-4 sm:py-6 bg-white border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-xl mx-auto mb-3 sm:mb-5">
            <span className="text-xs uppercase tracking-widest text-[#7A152E] font-semibold block mb-1">
              SHOP BY PRICE
            </span>
            <h2 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal">
              Shop by Price Points
            </h2>
            <p className="text-xs sm:text-sm text-stone-500 mt-1">
              Certified 925 silver & 18K gold vermeil for every budget and occasion.
            </p>
          </div>

          {/* 4 Beautiful Gift Box Cards with Ribbon Bows (All 4 in ONE Row on Mobile & PC) */}
          <div className="grid grid-cols-4 gap-2 xs:gap-2.5 sm:gap-4 md:gap-6 pt-1 sm:pt-2">
            
            {/* Gift Box 1: Under 999 */}
            <div
              onClick={() => handlePriceFilter(999)}
              className="group relative rounded-2xl sm:rounded-3xl p-2.5 xs:p-3 sm:p-6 bg-gradient-to-b from-[#FFFDF9] via-[#FAF5EE] to-[#F7EFE6] border-2 border-[#7A152E]/30 hover:border-[#7A152E] shadow-xs hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col items-center justify-center text-center aspect-square"
            >
              {/* Luxury Ribbon Bow on Top */}
              <div className="absolute -top-3.5 sm:-top-5 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                <svg className="w-9 xs:w-11 sm:w-16 h-3.5 xs:h-4.5 sm:h-6 transition-transform duration-300 group-hover:scale-115 drop-shadow-xs" viewBox="0 0 80 32" fill="none">
                  <path d="M40 16 C26 2, 8 4, 10 16 C12 24, 30 20, 40 16 Z" fill="#7A152E" />
                  <path d="M40 16 C54 2, 72 4, 70 16 C68 24, 50 20, 40 16 Z" fill="#7A152E" />
                  <path d="M37 17 L18 31 L28 21 Z" fill="#590D1E" />
                  <path d="M43 17 L62 31 L52 21 Z" fill="#590D1E" />
                  <circle cx="40" cy="16" r="4.5" fill="#D4AF37" />
                  <circle cx="40" cy="16" r="3" fill="#7A152E" />
                </svg>
              </div>
              <span className="font-sans text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase font-semibold text-stone-600 tracking-wider block">
                UNDER
              </span>
              <span className="font-sans font-bold text-sm xs:text-base sm:text-2xl md:text-3xl text-[#7A152E] tracking-tight block mt-0.5 sm:mt-1 group-hover:scale-105 transition-transform">
                ₹999
              </span>
              <span className="text-[7.5px] xs:text-[8.5px] sm:text-[11px] text-stone-400 group-hover:text-[#7A152E] font-medium tracking-wide block mt-1 sm:mt-2 transition-colors truncate max-w-full">
                Daily Picks
              </span>
            </div>

            {/* Gift Box 2: Under 1999 */}
            <div
              onClick={() => handlePriceFilter(1999)}
              className="group relative rounded-2xl sm:rounded-3xl p-2.5 xs:p-3 sm:p-6 bg-gradient-to-b from-[#FFFDF9] via-[#FAF5EE] to-[#F7EFE6] border-2 border-[#7A152E]/30 hover:border-[#7A152E] shadow-xs hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col items-center justify-center text-center aspect-square"
            >
              {/* Luxury Ribbon Bow on Top */}
              <div className="absolute -top-3.5 sm:-top-5 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                <svg className="w-9 xs:w-11 sm:w-16 h-3.5 xs:h-4.5 sm:h-6 transition-transform duration-300 group-hover:scale-115 drop-shadow-xs" viewBox="0 0 80 32" fill="none">
                  <path d="M40 16 C26 2, 8 4, 10 16 C12 24, 30 20, 40 16 Z" fill="#7A152E" />
                  <path d="M40 16 C54 2, 72 4, 70 16 C68 24, 50 20, 40 16 Z" fill="#7A152E" />
                  <path d="M37 17 L18 31 L28 21 Z" fill="#590D1E" />
                  <path d="M43 17 L62 31 L52 21 Z" fill="#590D1E" />
                  <circle cx="40" cy="16" r="4.5" fill="#D4AF37" />
                  <circle cx="40" cy="16" r="3" fill="#7A152E" />
                </svg>
              </div>
              <span className="font-sans text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase font-semibold text-stone-600 tracking-wider block">
                UNDER
              </span>
              <span className="font-sans font-bold text-sm xs:text-base sm:text-2xl md:text-3xl text-[#7A152E] tracking-tight block mt-0.5 sm:mt-1 group-hover:scale-105 transition-transform">
                ₹1,999
              </span>
              <span className="text-[7.5px] xs:text-[8.5px] sm:text-[11px] text-stone-400 group-hover:text-[#7A152E] font-medium tracking-wide block mt-1 sm:mt-2 transition-colors truncate max-w-full">
                Solitaires
              </span>
            </div>

            {/* Gift Box 3: Under 2999 */}
            <div
              onClick={() => handlePriceFilter(2999)}
              className="group relative rounded-2xl sm:rounded-3xl p-2.5 xs:p-3 sm:p-6 bg-gradient-to-b from-[#FFFDF9] via-[#FAF5EE] to-[#F7EFE6] border-2 border-[#7A152E]/30 hover:border-[#7A152E] shadow-xs hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col items-center justify-center text-center aspect-square"
            >
              {/* Luxury Ribbon Bow on Top */}
              <div className="absolute -top-3.5 sm:-top-5 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                <svg className="w-9 xs:w-11 sm:w-16 h-3.5 xs:h-4.5 sm:h-6 transition-transform duration-300 group-hover:scale-115 drop-shadow-xs" viewBox="0 0 80 32" fill="none">
                  <path d="M40 16 C26 2, 8 4, 10 16 C12 24, 30 20, 40 16 Z" fill="#7A152E" />
                  <path d="M40 16 C54 2, 72 4, 70 16 C68 24, 50 20, 40 16 Z" fill="#7A152E" />
                  <path d="M37 17 L18 31 L28 21 Z" fill="#590D1E" />
                  <path d="M43 17 L62 31 L52 21 Z" fill="#590D1E" />
                  <circle cx="40" cy="16" r="4.5" fill="#D4AF37" />
                  <circle cx="40" cy="16" r="3" fill="#7A152E" />
                </svg>
              </div>
              <span className="font-sans text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase font-semibold text-stone-600 tracking-wider block">
                UNDER
              </span>
              <span className="font-sans font-bold text-sm xs:text-base sm:text-2xl md:text-3xl text-[#7A152E] tracking-tight block mt-0.5 sm:mt-1 group-hover:scale-105 transition-transform">
                ₹2,999
              </span>
              <span className="text-[7.5px] xs:text-[8.5px] sm:text-[11px] text-stone-400 group-hover:text-[#7A152E] font-medium tracking-wide block mt-1 sm:mt-2 transition-colors truncate max-w-full">
                Statements
              </span>
            </div>

            {/* Gift Box 4: Premium Gifts */}
            <div
              onClick={() => handlePriceFilter(3999)}
              className="group relative rounded-2xl sm:rounded-3xl p-2.5 xs:p-3 sm:p-6 bg-gradient-to-b from-[#FFFDF9] via-[#FAF5EE] to-[#F7EFE6] border-2 border-[#7A152E]/30 hover:border-[#7A152E] shadow-xs hover:shadow-lg transition-all duration-300 cursor-pointer flex flex-col items-center justify-center text-center aspect-square"
            >
              {/* Luxury Ribbon Bow on Top */}
              <div className="absolute -top-3.5 sm:-top-5 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
                <svg className="w-9 xs:w-11 sm:w-16 h-3.5 xs:h-4.5 sm:h-6 transition-transform duration-300 group-hover:scale-115 drop-shadow-xs" viewBox="0 0 80 32" fill="none">
                  <path d="M40 16 C26 2, 8 4, 10 16 C12 24, 30 20, 40 16 Z" fill="#7A152E" />
                  <path d="M40 16 C54 2, 72 4, 70 16 C68 24, 50 20, 40 16 Z" fill="#7A152E" />
                  <path d="M37 17 L18 31 L28 21 Z" fill="#590D1E" />
                  <path d="M43 17 L62 31 L52 21 Z" fill="#590D1E" />
                  <circle cx="40" cy="16" r="4.5" fill="#D4AF37" />
                  <circle cx="40" cy="16" r="3" fill="#7A152E" />
                </svg>
              </div>
              <span className="font-sans text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase font-semibold text-stone-600 tracking-wider block">
                PREMIUM
              </span>
              <span className="font-sans font-bold text-xs xs:text-sm sm:text-xl md:text-2xl text-[#7A152E] tracking-tight block mt-0.5 sm:mt-1 group-hover:scale-105 transition-transform leading-snug">
                GIFTS
              </span>
              <span className="text-[7.5px] xs:text-[8.5px] sm:text-[11px] text-stone-400 group-hover:text-[#7A152E] font-medium tracking-wide block mt-1 sm:mt-2 transition-colors truncate max-w-full">
                Vault Sets
              </span>
            </div>

          </div>

        </div>
      </section>

      {/* ========================================================
          5. CURATED METALS: 18K GOLD & 925 SILVER
             ("FOR HIM / FOR HER" CARD ARCHITECTURE: BOTH IN ONE ROW ON MOBILE)
          ======================================================== */}
      <section className="py-4 sm:py-7 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Luxury Section Header - Max 2 Headlines */}
        <div className="text-center max-w-2xl mx-auto mb-3 sm:mb-5">
          <span className="text-[11px] uppercase tracking-widest text-[#7A152E] font-bold block mb-1">
            CURATED METALS
          </span>
          <h2 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal">
            18K Gold Vermeil & 925 Silver
          </h2>
        </div>

        {/* Both Cards In ONE Row on Mobile (grid-cols-2) & PC - Luxury Editorial Full-Bleed Design */}
        <div className="grid grid-cols-2 gap-3 sm:gap-6 lg:gap-8 max-w-4xl mx-auto">
          
          {/* Card 1: 18K Gold Vermeil (Authentic Luminous Gold Theme & Smooth Laser Border Loop) */}
          <div
            onClick={() => handleCategorySelect('gold')}
            className="laser-card-gold group relative rounded-2xl sm:rounded-3xl p-[2px] sm:p-[3.5px] transition-all duration-500 cursor-pointer flex flex-col aspect-[3/4.3] sm:aspect-[4/5]"
          >
            {/* Automatic Smooth Looped Gold Laser Border */}
            <div className="laser-beam-gold pointer-events-none" />

            {/* Inner Card Container (masks center, revealing only the animated laser border) */}
            <div className="relative w-full h-full rounded-[14px] sm:rounded-[20.5px] overflow-hidden bg-[#181109] flex flex-col justify-end p-2.5 xs:p-3.5 sm:p-5 z-10">
              {/* Full-bleed high fashion model portrait */}
              <img
                src="/solystra_assets/metals/gold_model.jpg"
                alt="18K Gold Vermeil Collection"
                className="absolute inset-0 w-full h-full object-cover object-top group-hover:scale-106 transition-transform duration-700 ease-out"
                loading="lazy"
              />

              {/* Warm Gold Ambient Luminance Overlay */}
              <div className="absolute inset-0 bg-gradient-to-tr from-[#D4AF37]/20 via-transparent to-[#E5C985]/15 pointer-events-none" />

              {/* Smooth High-Contrast Scrim Gradient for Razor-Sharp Typography */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/35 via-45% to-transparent pointer-events-none" />

              {/* Modern Luxury Studio Diffused Gold Sheen */}
              <div className="absolute inset-0 overflow-hidden pointer-events-none z-20">
                <div className="gold-modern-sheen" />
              </div>

              {/* Bottom Editorial Content with Real Brushed Metallic Gold CTA */}
              <div className="relative z-20 flex flex-col items-center text-center">
                <span className="text-[7px] xs:text-[8px] sm:text-[10px] uppercase tracking-[0.25em] font-semibold text-[#E5C378] block drop-shadow-xs">
                  SOLYSTRA ATELIER
                </span>
                <h3 className="font-serif text-[15px] xs:text-lg sm:text-2xl lg:text-3xl font-normal text-white mt-0.5 leading-tight drop-shadow-sm">
                  18K Gold Vermeil
                </h3>
                <p className="hidden sm:block text-[11px] text-stone-200/90 font-light mt-1">
                  2.5-Micron Thick Gold over Pure 925 Silver
                </p>
                
                <div className="mt-2 sm:mt-3.5 btn-real-gold inline-flex items-center justify-center gap-1 sm:gap-1.5 px-3 xs:px-3.5 sm:px-6 py-1 sm:py-2 rounded-full font-sans font-bold text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase tracking-wider whitespace-nowrap transition-all duration-300 group-hover:scale-103 shadow-md">
                  <span>Explore Gold</span>
                  <svg 
                    className="w-2.5 h-2.5 sm:w-3.5 sm:h-3.5 group-hover:translate-x-0.5 transition-transform duration-300 shrink-0" 
                    viewBox="0 0 16 16" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2.2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <path d="M2.5 8h10M8.5 4L12.5 8l-4 4" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Card 2: 925 Sterling Silver (Authentic Moonlit Platinum Theme & Smooth Laser Border Loop) */}
          <div
            onClick={() => handleCategorySelect('silver')}
            className="laser-card-silver group relative rounded-2xl sm:rounded-3xl p-[2px] sm:p-[3.5px] transition-all duration-500 cursor-pointer flex flex-col aspect-[3/4.3] sm:aspect-[4/5]"
          >
            {/* Automatic Smooth Looped Silver Laser Border */}
            <div className="laser-beam-silver pointer-events-none" />

            {/* Inner Card Container (masks center, revealing only the animated laser border) */}
            <div className="relative w-full h-full rounded-[14px] sm:rounded-[20.5px] overflow-hidden bg-[#0A101D] flex flex-col justify-end p-2.5 xs:p-3.5 sm:p-5 z-10">
              {/* Full-bleed high fashion model portrait */}
              <img
                src="/solystra_assets/metals/silver_model.jpg"
                alt="925 Sterling Silver Collection"
                className="absolute inset-0 w-full h-full object-cover object-top group-hover:scale-106 transition-transform duration-700 ease-out"
                loading="lazy"
              />

              {/* Cool Silver/Rhodium Ambient Lustre Overlay */}
              <div className="absolute inset-0 bg-gradient-to-tr from-slate-200/20 via-transparent to-white/15 pointer-events-none" />

              {/* Smooth High-Contrast Scrim Gradient for Razor-Sharp Typography */}
              <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/35 via-45% to-transparent pointer-events-none" />

              {/* Modern Luxury Studio Diffused Silver Sheen (Alternating Phase) */}
              <div className="absolute inset-0 overflow-hidden pointer-events-none z-20">
                <div className="silver-modern-sheen" />
              </div>

              {/* Bottom Editorial Content with Real Brushed Metallic Silver CTA */}
              <div className="relative z-20 flex flex-col items-center text-center">
                <span className="text-[7px] xs:text-[8px] sm:text-[10px] uppercase tracking-[0.25em] font-semibold text-slate-200 block drop-shadow-xs">
                  SOLYSTRA ATELIER
                </span>
                <h3 className="font-serif text-[15px] xs:text-lg sm:text-2xl lg:text-3xl font-normal text-white mt-0.5 leading-tight drop-shadow-sm">
                  925 Sterling Silver
                </h3>
                <p className="hidden sm:block text-[11px] text-stone-200/90 font-light mt-1">
                  Anti-Tarnish Mirror Rhodium Dipped Solid 925
                </p>
                
                <div className="mt-2 sm:mt-3.5 btn-real-silver inline-flex items-center justify-center gap-1 sm:gap-1.5 px-3 xs:px-3.5 sm:px-6 py-1 sm:py-2 rounded-full font-sans font-bold text-[8.5px] xs:text-[9.5px] sm:text-xs uppercase tracking-wider whitespace-nowrap transition-all duration-300 group-hover:scale-103 shadow-md">
                  <span>Explore Silver</span>
                  <svg 
                    className="w-2.5 h-2.5 sm:w-3.5 sm:h-3.5 group-hover:translate-x-0.5 transition-transform duration-300 shrink-0" 
                    viewBox="0 0 16 16" 
                    fill="none" 
                    stroke="currentColor" 
                    strokeWidth="2.2" 
                    strokeLinecap="round" 
                    strokeLinejoin="round"
                  >
                    <path d="M2.5 8h10M8.5 4L12.5 8l-4 4" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          6. NEWLY LAUNCHED DESIGNS
          ======================================================== */}
      <section className="py-4 sm:py-6 bg-[#FAF8F5] border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-3 pb-2 border-b border-[#EAE4DC] gap-3">
            <div>
              <span className="text-[10px] tracking-[0.25em] uppercase font-semibold text-[#7A152E] block mb-1">
                Fresh Drops &bull; Atelier Debut
              </span>
              <h2 className="font-serif text-2xl sm:text-4xl font-normal text-stone-900">
                Newly Launched Designs
              </h2>
            </div>

            <button
              onClick={() => {
                setViewFullCatalog(true);
                setSelectedCategory('new_arrivals');
                setSelectedMaxPrice(null);
                document.getElementById('bestsellers-showcase')?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#7A152E] hover:text-[#590D1E] group self-start sm:self-end transition-colors cursor-pointer"
            >
              <span>Explore All New Releases</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
          </div>

          {/* Mobile: Full-Sized Cards Carousel with Seamless Infinite Looping */}
          <div
            ref={newlyLaunchedScrollRef}
            onScroll={handleNewlyLaunchedScroll}
            className="flex sm:hidden gap-3.5 overflow-x-auto no-scrollbar py-2 px-1 -mx-1"
          >
            {tripleNewlyLaunched.map((product, idx) => (
              <div
                key={`newly-launched-m-${product.id}-${idx}`}
                data-product-card="true"
                className="w-[220px] xs:w-[240px] shrink-0 select-none"
              >
                <ProductCard product={product} />
              </div>
            ))}
          </div>

          {/* Desktop & Tablet: Generous Full-Sized Grid */}
          <div className="hidden sm:grid sm:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-7 pt-1">
            {newlyLaunchedProducts.slice(0, 4).map((product) => (
              <div key={`newly-launched-d-${product.id}`} className="w-full h-full">
                <ProductCard product={product} />
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* ========================================================
          8. TOP COLLECTIONS: ZAVYA-STYLE TALL PORTRAIT HORIZONTAL SLIDER
          ======================================================== */}
      <section className="py-4 sm:py-7 bg-white border-y border-[#EAE4DC] overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Header without dot */}
          <div className="mb-3 sm:mb-5">
            <span className="text-xs uppercase tracking-widest text-[#7A152E] font-semibold block mb-1">
              SIGNATURE EDITS
            </span>
            <h2 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal">
              Top Collections
            </h2>
          </div>

          {/* Center-Hero Coverflow Slider with Noticeably Smaller Left/Right Cards */}
          <div
            ref={topCollectionsScrollRef}
            {...topCollectionsDrag.dragProps}
            onScroll={handleTopCollectionsScroll}
            id="top-collections-scroll"
            className="flex items-center gap-2 sm:gap-4 overflow-x-auto hide-scrollbar py-6 sm:py-8 -mx-4 sm:-mx-6 lg:-mx-8 px-[17vw] sm:px-[calc(50%-130px)] md:px-[calc(50%-145px)] snap-x snap-mandatory cursor-grab active:cursor-grabbing select-none"
          >
            {TRIPLE_TOP_COLLECTIONS.map((col, idx) => {
              const isCenter = idx === activeCollectionIndex;
              return (
                <div
                  key={col.loopId}
                  data-collection-card="true"
                  onClick={topCollectionsDrag.handleItemClick(() => handleCollectionCardClick(col, idx))}
                  className={`w-[66vw] xs:w-[60vw] sm:w-[250px] md:w-[280px] aspect-[303/423] shrink-0 snap-center relative rounded-[24px] sm:rounded-[28px] p-[2.5px] sm:p-[3px] bg-gradient-to-b from-[#D4AF37] via-[#7A152E] to-[#590D1E] transition-all duration-500 ease-out cursor-pointer group select-none origin-center ${
                    isCenter
                      ? 'scale-100 sm:scale-105 opacity-100 z-20 shadow-[0_16px_40px_rgba(122,21,46,0.32)] ring-1 ring-[#D4AF37]/40'
                      : 'scale-[0.76] sm:scale-[0.80] opacity-55 hover:opacity-75 z-0 shadow-sm filter contrast-95'
                  }`}
                >
                  <div className="w-full h-full rounded-[21.5px] sm:rounded-[25px] overflow-hidden bg-[#FAF8F5] relative">
                    <img
                      src={col.img}
                      alt={col.title}
                      draggable="false"
                      className="w-full h-full object-cover scale-[1.095] block pointer-events-none transition-transform duration-500 group-hover:scale-[1.13]"
                      loading="lazy"
                    />
                  </div>
                </div>
              );
            })}
          </div>

        </div>
      </section>

      {/* ========================================================
          SHOP THE COMPLETE LOOK: COMPACT MULTI-COMBO SLIDER
          ======================================================== */}
      <section
        className="py-4 sm:py-6 bg-[#FAF8F5] border-b border-[#EAE4DC]"
        onMouseEnter={() => setIsComboPaused(true)}
        onMouseLeave={() => setIsComboPaused(false)}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          {/* Section Header with Carousel Navigation & Dot Indicators */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-2 pb-1 border-b border-[#EAE4DC] gap-3">
            <div>
              <span className="text-[11px] uppercase tracking-widest text-[#7A152E] font-bold block">
                CURATED LOOKS
              </span>
              <h2 className="font-serif text-2xl sm:text-3xl text-stone-900 font-normal mt-0.5">
                Shop the Complete Look
              </h2>
            </div>

            {/* Carousel Navigation Controls (Auto-slides every 5.5s) */}
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-stone-500">
                Combo {String(currentComboIndex + 1).padStart(2, '0')} / {String(STYLING_COMBOS.length).padStart(2, '0')}
              </span>

              {/* Dot Indicators */}
              <div className="flex items-center gap-1.5">
                {STYLING_COMBOS.map((_, idx) => (
                  <button
                    key={idx}
                    onClick={() => setCurrentComboIndex(idx)}
                    className={`h-1.5 rounded-full transition-all duration-300 cursor-pointer ${
                      idx === currentComboIndex ? 'w-5 bg-[#7A152E]' : 'w-1.5 bg-stone-300 hover:bg-stone-400'
                    }`}
                    aria-label={`Go to combo ${idx + 1}`}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Responsive 2-Column Balanced Combo View (Strict Equal Height Across All Combos) */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-stretch">
            
            {/* Left Column: Proportional Editorial Combo Photo with Delicate Glowing Hotspots */}
            <div className="lg:col-span-6 h-[380px] sm:h-[420px] lg:h-[430px] relative rounded-2xl overflow-hidden shadow-xs border border-[#EAE4DC] group bg-stone-900 select-none">
              <img
                src={activeCombo.editorialImg}
                alt={activeCombo.name}
                draggable="false"
                className={`w-full h-full object-cover ${activeCombo.imagePosition || 'object-[72%_center]'} group-hover:scale-102 transition-transform duration-700 block pointer-events-none`}
              />
              
              {/* Subtle ambient gradient strictly in lower 20% so jewellery and model are clear and radiant */}
              <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/80 via-black/25 to-transparent pointer-events-none" />

              {/* Delicate Glowing Pinpoint Hotspots (Directly on Jewellery Pieces, Clean Luxury Styling) */}
              {activeCombo.items.map((item) => {
                if (!item.hotspot) return null;
                const isHovered = activeHotspotId === item.id;
                const pcX = item.hotspot.pcX !== undefined ? item.hotspot.pcX : item.hotspot.x;
                const pcY = item.hotspot.pcY !== undefined ? item.hotspot.pcY : item.hotspot.y;
                return (
                  <div
                    key={item.id}
                    style={{
                      '--dot-x-mob': `${item.hotspot.x}%`,
                      '--dot-y-mob': `${item.hotspot.y}%`,
                      '--dot-x-pc': `${pcX}%`,
                      '--dot-y-pc': `${pcY}%`,
                    }}
                    className="combo-hotspot-pin absolute -translate-x-1/2 -translate-y-1/2 z-20"
                    onMouseEnter={() => setActiveHotspotId(item.id)}
                    onMouseLeave={() => setActiveHotspotId(null)}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (activeHotspotId === item.id) {
                        window.location.hash = `#/product/${item.productId}`;
                      } else {
                        setActiveHotspotId(item.id);
                      }
                    }}
                  >
                    {/* Delicate Luxury Pinpoint */}
                    <div className="relative group/hotspot cursor-pointer">
                      {/* Subtle micro pulse */}
                      <span className="absolute -inset-0.5 rounded-full bg-[#7A152E]/35 animate-ping pointer-events-none" />

                      {/* Small Proper Luxury Pinpoint (Delicate 12px, brand burgundy & gold) */}
                      <button
                        type="button"
                        className={`w-3 h-3 sm:w-3.5 sm:h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer ${
                          isHovered
                            ? 'scale-125 bg-[#7A152E] ring-2 ring-[#D4AF37]'
                            : 'bg-[#7A152E] hover:scale-115'
                        }`}
                        aria-label={`View ${item.name}`}
                      >
                        <span className="w-1 h-1 rounded-full bg-white shadow-xs" />
                      </button>

                      {/* Interactive Luxury Tooltip Popover */}
                      <div className={`absolute z-30 transition-all duration-300 pointer-events-auto ${
                        (item.hotspot.y > 55 || pcY > 55)
                          ? 'bottom-full mb-3'
                          : 'top-full mt-3'
                      } ${
                        (item.hotspot.x > 60 || pcX > 60)
                          ? 'right-0 sm:-right-4'
                          : 'left-0 sm:-left-4'
                      } ${
                        isHovered
                          ? 'opacity-100 scale-100 visible'
                          : 'opacity-0 scale-95 invisible'
                      } min-w-[210px] sm:min-w-[230px] p-2.5 rounded-xl bg-[#1C1819]/95 backdrop-blur-md border border-[#C5A059]/60 shadow-[0_15px_35px_rgba(0,0,0,0.6)]`}>
                        <div className="flex items-center gap-2.5">
                          <img
                            src={item.image}
                            alt={item.name}
                            className="w-11 h-11 rounded-lg object-cover bg-white/10 border border-white/20 shrink-0"
                          />
                          <div className="flex-1 min-w-0 text-left">
                            <span className="text-[9px] uppercase tracking-wider font-bold text-[#E5C985] block">
                              {item.type}
                            </span>
                            <h5 className="text-xs font-serif font-normal text-white truncate">
                              {item.name}
                            </h5>
                            <div className="text-[11px] font-bold text-[#E5C985] mt-0.5">
                              ₹{item.price.toLocaleString('en-IN')}
                            </div>
                          </div>
                        </div>
                        <div className="mt-2 pt-1.5 border-t border-white/10 flex items-center justify-between text-[9.5px] text-stone-300">
                          <span className="text-stone-400">Click to view piece</span>
                          <span className="text-[#E5C985] font-bold flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                            <span>Shop Piece</span>
                            <ArrowRight className="w-2.5 h-2.5" />
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}

              {/* Bottom Editorial Narrative (Clean luxury label, no awkward wrapping) */}
              <div className="absolute bottom-3 left-3 sm:bottom-4 sm:left-4 z-10 pointer-events-none max-w-[85%] sm:max-w-md">
                <span className="text-[8px] xs:text-[9px] sm:text-[10px] uppercase tracking-widest text-[#E5C985] font-bold block mb-0.5 drop-shadow-xs">
                  {activeCombo.tag}
                </span>
                <h3 className="font-serif text-sm xs:text-base sm:text-xl text-white font-normal leading-snug drop-shadow-sm whitespace-nowrap">
                  {activeCombo.name}
                </h3>
              </div>
            </div>

            {/* Right Column: Matched Pieces & Bundle Pricing (Identical Height & Layout) */}
            <div className="lg:col-span-6 h-[380px] sm:h-[420px] lg:h-[430px] flex flex-col justify-between bg-white rounded-2xl p-5 sm:p-6 border border-[#EAE4DC] shadow-xs">
              
              <div>
                <div className="flex items-start justify-between pb-3 border-b border-[#EAE4DC] gap-2">
                  <div>
                    <span className="text-[9.5px] text-[#7A152E] uppercase tracking-widest font-bold block">
                      {activeCombo.tag}
                    </span>
                    <h3 className="text-sm sm:text-base font-serif font-normal text-stone-900 leading-tight mt-0.5">
                      {activeCombo.name}
                    </h3>
                  </div>
                  <span className="text-[10.5px] text-[#7A152E] font-bold bg-[#7A152E]/8 px-2.5 py-1 rounded-full border border-[#7A152E]/20 uppercase tracking-wider shrink-0">
                    Save ₹{activeCombo.savings.toLocaleString('en-IN')}
                  </span>
                </div>

                {/* 2 Equal-Height Matched Pieces Cards */}
                <div className="space-y-2.5 mt-3.5">
                  {activeCombo.items.map((item) => (
                    <div
                      key={item.id}
                      onClick={() => {
                        window.location.hash = `#/product/${item.productId}`;
                      }}
                      onMouseEnter={() => setActiveHotspotId(item.id)}
                      onMouseLeave={() => setActiveHotspotId(null)}
                      className={`flex items-center gap-3.5 p-3 rounded-xl transition-all cursor-pointer group border ${
                        activeHotspotId === item.id
                          ? 'bg-[#7A152E]/5 border-[#7A152E] shadow-sm ring-1 ring-[#7A152E]/20'
                          : 'bg-[#FAF8F5]/80 border-[#EAE4DC] hover:border-[#7A152E]/60 hover:bg-white hover:shadow-2xs'
                      }`}
                      title="Click to view product details"
                    >
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-14 h-14 rounded-xl object-cover border border-[#EAE4DC] bg-white shrink-0 group-hover:scale-105 transition-transform"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="text-[9.5px] text-[#7A152E] uppercase font-bold tracking-wider block">
                            {item.type}
                          </span>
                          <span className="text-[9px] text-[#C5A059] opacity-0 group-hover:opacity-100 transition-opacity font-semibold">
                            View Piece ↗
                          </span>
                        </div>
                        <h4 className="font-serif text-sm font-normal text-stone-900 truncate group-hover:text-[#7A152E] transition-colors mt-0.5">
                          {item.name}
                        </h4>
                        <div className="text-[11px] text-stone-500 truncate mt-0.5">{item.metal}</div>
                      </div>
                      <div className="text-right shrink-0">
                        <div className="font-bold text-sm text-[#7A152E]">
                          ₹{item.price.toLocaleString('en-IN')}
                        </div>
                        <div className="text-[11px] text-stone-400 line-through">
                          ₹{item.mrp.toLocaleString('en-IN')}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Bundle Pricing & Action Bar */}
              <div className="pt-3.5 mt-3 border-t border-[#EAE4DC] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="text-[10px] text-stone-500 uppercase tracking-wider font-semibold">Complete Set Price</div>
                  <div className="flex items-baseline gap-2 mt-0.5">
                    <span className="font-serif text-2xl sm:text-3xl font-bold text-[#7A152E]">
                      ₹{activeCombo.bundlePrice.toLocaleString('en-IN')}
                    </span>
                    <span className="text-xs text-stone-400 line-through font-sans">
                      ₹{activeCombo.originalPrice.toLocaleString('en-IN')}
                    </span>
                    <span className="text-[10px] font-bold text-[#7A152E] uppercase bg-[#7A152E]/10 px-2 py-0.5 rounded-full border border-[#7A152E]/20">
                      Save ₹{activeCombo.savings.toLocaleString('en-IN')}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleAddCurrentComboToBag}
                  className="px-6 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer flex items-center justify-center gap-2 active:scale-98 shrink-0 group"
                >
                  <GoldShoppingBag className="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" />
                  <span className="leading-none">Add Look to Bag</span>
                </button>
              </div>

            </div>

          </div>
        </div>
      </section>


      {/* ========================================================
          8. VIDEO SIDE SCROLL OPTION (SOLYSTRA REELS IN MOTION)
          ======================================================== */}
      <section className="py-4 sm:py-6 bg-white border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-3 pb-2 border-b border-[#EAE4DC] gap-3">
            <div>
              <span className="text-[10px] tracking-[0.25em] uppercase font-semibold text-[#7A152E] block mb-1">
                The Atelier in Motion
              </span>
              <h2 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal">
                Pure Radiance Captured
              </h2>
            </div>
          </div>

          {/* Horizontal Video Reel Slider (Infinite Continuous Flow & Drag/Touch) */}
          <div
            ref={videoScrollRef}
            {...videoDrag.dragProps}
            onMouseDown={(e) => {
              isVideoInteracting.current = true;
              videoDrag.dragProps.onMouseDown(e);
            }}
            onMouseUp={(e) => {
              videoDrag.dragProps.onMouseUp(e);
              setTimeout(() => { isVideoInteracting.current = false; }, 300);
            }}
            className="flex flex-nowrap gap-4 sm:gap-5 overflow-x-auto hide-scrollbar pb-4 pt-1 cursor-grab active:cursor-grabbing select-none"
          >
            {TRIPLE_VIDEO_REELS.map((reel) => (
              <div
                key={reel.loopId}
                className="w-[205px] sm:w-[235px] md:w-[255px] shrink-0 group relative rounded-2xl overflow-hidden bg-white border border-[#EAE4DC] hover:border-[#7A152E]/60 shadow-xs hover:shadow-xl transition-all duration-300 flex flex-col"
              >
                {/* Clean Video Viewport - Balanced Aspect Ratio */}
                <div
                  onClick={videoDrag.handleItemClick(() => setActiveVideoModal(reel))}
                  className="aspect-[4/5] relative overflow-hidden bg-stone-950 cursor-pointer"
                >
                  <video
                    src={reel.videoSrc}
                    poster={reel.productImage}
                    autoPlay
                    muted
                    loop
                    playsInline
                    onLoadedData={(e) => {
                      e.target.play().catch(() => {});
                    }}
                    className="w-full h-full object-cover block group-hover:scale-105 transition-transform duration-500 pointer-events-none"
                  />

                  {/* Subtle clean hover overlay */}
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/15 transition-colors pointer-events-none" />
                </div>

                {/* Product Info & Action Buttons */}
                <div className="p-3 sm:p-3.5 bg-white flex flex-col gap-2.5">
                  <div className="flex items-center gap-2.5">
                    {/* Small Box with Product Image */}
                    <div
                      onClick={() => setActiveVideoModal(reel)}
                      className="w-11 h-11 sm:w-12 sm:h-12 rounded-xl bg-stone-50 border border-stone-200 overflow-hidden shrink-0 shadow-2xs cursor-pointer hover:opacity-90 transition-opacity"
                    >
                      <img
                        src={reel.productImage}
                        alt={reel.title}
                        className="w-full h-full object-cover"
                        loading="lazy"
                      />
                    </div>

                    {/* Product Name & Metal */}
                    <div className="min-w-0 flex-1">
                      <p
                        onClick={() => setActiveVideoModal(reel)}
                        className="text-xs sm:text-[12.5px] font-semibold text-stone-900 truncate cursor-pointer hover:text-[#7A152E] transition-colors leading-tight"
                        title={reel.title}
                      >
                        {reel.title}
                      </p>
                      <p className="text-[10px] sm:text-[10.5px] text-stone-500 font-medium truncate mt-0.5">
                        {reel.metal}
                      </p>
                    </div>

                    {/* Price */}
                    <div className="text-right shrink-0">
                      <span className="text-xs sm:text-[13px] font-bold text-[#7A152E] block">
                        ₹{reel.price.toLocaleString('en-IN')}
                      </span>
                      <span className="text-[9.5px] text-stone-400 line-through block -mt-0.5">
                        ₹{reel.mrp.toLocaleString('en-IN')}
                      </span>
                    </div>
                  </div>

                  {/* Single Action Button: Add to Cart Only */}
                  <div className="pt-2 border-t border-[#F0EBE3]">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAddVideoProduct(reel);
                      }}
                      className="w-full py-2 px-2.5 rounded-lg bg-[#7A152E] hover:bg-[#590D1E] text-white font-sans text-xs font-semibold flex items-center justify-center gap-1.5 transition-all duration-150 cursor-pointer active:scale-95 shadow-2xs group/video-cart"
                      title="Add to Cart"
                    >
                      <GoldShoppingBag className="w-3.5 h-3.5 shrink-0 -translate-y-px transition-transform duration-200 group-hover/video-cart:-translate-y-0.5" />
                      <span className="truncate tracking-wide leading-none">Add to Cart</span>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>


        </div>
      </section>

      {/* ========================================================
          VIDEO REEL MODAL PLAYER
          ======================================================== */}
      {activeVideoModal && (
        <div
          className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 sm:p-6"
          onClick={() => setActiveVideoModal(null)}
        >
          <div
            className="relative w-full max-w-2xl bg-stone-950 rounded-3xl overflow-hidden border border-stone-700 shadow-2xl flex flex-col sm:flex-row max-h-[90vh]"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Close Button */}
            <button
              onClick={() => setActiveVideoModal(null)}
              className="absolute top-3 right-3 z-30 w-9 h-9 rounded-full bg-[#7A152E]/80 hover:bg-[#7A152E] text-white flex items-center justify-center transition-colors cursor-pointer shadow-md"
              aria-label="Close video"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Video Player Column */}
            <div className="relative w-full sm:w-1/2 aspect-[9/16] sm:aspect-auto sm:min-h-[460px] bg-black flex items-center justify-center">
              <video
                src={activeVideoModal.videoSrc}
                autoPlay
                loop
                playsInline
                muted={isVideoMuted}
                className="w-full h-full object-cover"
                controls
              />
              {/* Mute Toggle */}
              <button
                onClick={() => setIsVideoMuted((prev) => !prev)}
                className="absolute bottom-4 left-4 z-20 w-8 h-8 rounded-full bg-[#7A152E]/80 hover:bg-[#7A152E] text-white flex items-center justify-center transition-colors cursor-pointer shadow-md"
              >
                {isVideoMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
              </button>
            </div>

            {/* Product Details Column */}
            <div className="p-6 sm:p-8 sm:w-1/2 flex flex-col justify-between bg-white text-stone-900">
              <div>
                <span className="text-[10.5px] uppercase tracking-widest text-[#7A152E] font-bold block mb-1">
                  {activeVideoModal.metal}
                </span>
                <div className="flex items-center gap-3 mb-2 p-2 rounded-xl bg-stone-50 border border-stone-200">
                  <img
                    src={activeVideoModal.productImage}
                    alt={activeVideoModal.title}
                    className="w-12 h-12 rounded-lg object-cover border border-stone-200 shrink-0"
                  />
                  <div className="min-w-0">
                    <h3 className="font-serif text-lg font-normal text-stone-900 truncate">
                      {activeVideoModal.title}
                    </h3>
                    <p className="text-[11px] text-stone-500 truncate">{activeVideoModal.metal}</p>
                  </div>
                </div>
                
                <div className="flex items-baseline gap-2 mt-2">
                  <span className="font-serif text-2xl font-bold text-[#7A152E]">
                    ₹{activeVideoModal.price.toLocaleString('en-IN')}
                  </span>
                  <span className="text-sm text-stone-400 line-through">
                    ₹{activeVideoModal.mrp.toLocaleString('en-IN')}
                  </span>
                  <span className="text-xs font-semibold text-emerald-700">
                    Verified Purity
                  </span>
                </div>

                <p className="text-xs text-stone-600 mt-4 leading-relaxed font-light">
                  {activeVideoModal.desc}
                </p>

                <div className="space-y-2 mt-5 pt-4 border-t border-stone-200 text-xs text-stone-600">
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-emerald-600" />
                    <span>Government BIS 925 Hallmark Guaranteed</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-emerald-600" />
                    <span>Double-Micron Rhodium Anti-Tarnish Clad</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-emerald-600" />
                    <span>Delivered in Royal Velvet Keepsake Vault</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-stone-200">
                <button
                  type="button"
                  onClick={() => {
                    handleAddVideoProduct(activeVideoModal);
                    setActiveVideoModal(null);
                  }}
                  className="w-full py-3.5 px-5 rounded-xl bg-[#7A152E] hover:bg-[#590D1E] text-white font-sans text-xs sm:text-sm font-bold uppercase tracking-wider rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer flex items-center justify-center gap-2 group"
                >
                  <GoldShoppingBag className="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" />
                  <span className="leading-none">Add to Bag &bull; ₹{activeVideoModal.price.toLocaleString('en-IN')}</span>
                </button>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* ========================================================
          9. VERIFIED CUSTOMER REVIEWS
          ======================================================== */}
      {/* ========================================================
          9. VERIFIED CUSTOMER REVIEWS (PATRON PERSPECTIVES)
          ======================================================== */}
      <section id="reviews-section" className="py-6 sm:py-10 bg-[#FAF8F5] border-y border-[#EAE4DC] relative overflow-hidden">
        {/* Soft Royal Ambient Hue */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-32 bg-gradient-to-b from-[#7A152E]/4 to-transparent pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          
          {/* Section Header */}
          <div className="text-center max-w-2xl mx-auto mb-5 sm:mb-8">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-white border border-[#EAE4DC] text-[#7A152E] mb-3 shadow-2xs">
              <Crown className="w-3.5 h-3.5 text-[#C5A059]" />
              <span className="text-[11px] uppercase tracking-[0.2em] font-bold">
                PATRON TESTIMONIALS
              </span>
            </div>

            <h2 className="font-serif text-2xl sm:text-4xl md:text-5xl text-stone-900 font-normal tracking-tight">
              Words from Our Atelier Clients
            </h2>

            <div className="flex flex-wrap items-center justify-center gap-2.5 sm:gap-4 mt-3.5">
              <div className="inline-flex items-center gap-1.5 bg-white px-3.5 py-1.5 rounded-full border border-[#EAE4DC] shadow-2xs">
                <div className="flex items-center gap-0.5 text-[#C5A059]">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-3.5 h-3.5 fill-[#C5A059] stroke-none" />
                  ))}
                </div>
                <span className="text-xs font-bold text-stone-900 font-sans">4.9 / 5.0</span>
                <span className="text-stone-300">&bull;</span>
                <span className="text-xs text-stone-600 font-medium">Over 1,200 Certified Buyers</span>
              </div>

              <div className="hidden sm:inline-flex items-center gap-1.5 bg-white/70 px-3 py-1.5 rounded-full border border-[#EAE4DC] text-xs text-stone-600 font-medium">
                <ShieldCheck className="w-3.5 h-3.5 text-[#7A152E]" />
                <span>100% BIS Hallmarked Purity</span>
              </div>
            </div>
          </div>

          {/* Luxury Editorial Review Cards (3 Curated Cards) */}
          <div className="flex md:grid md:grid-cols-3 gap-5 sm:gap-6 overflow-x-auto md:overflow-visible hide-scrollbar pb-3 px-1 snap-x snap-mandatory">
            {CUSTOMER_REVIEWS.slice(0, 3).map((review) => {
              const authorName = review.author || review.name || 'Verified Patron';
              const productName = review.productName || review.product || 'Fine Jewelry Suite';

              return (
                <div
                  key={review.id}
                  className="w-[85vw] sm:w-[70vw] md:w-auto shrink-0 snap-center relative rounded-2xl bg-white border border-[#EAE4DC] p-6 sm:p-7 flex flex-col justify-between shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:shadow-[0_12px_28px_rgba(122,21,46,0.08)] hover:border-[#C5A059]/60 transition-all duration-300 group"
                >
                  {/* Watermark Quote Mark */}
                  <span className="absolute top-4 right-5 font-serif text-5xl text-[#C5A059]/15 select-none pointer-events-none leading-none">
                    “
                  </span>

                  {/* Top Bar: Stars + Clean Verified Purchase Badge */}
                  <div>
                    <div className="flex items-center justify-between pb-3.5 border-b border-[#F0EBE3]">
                      <div className="flex items-center gap-1.5">
                        <div className="flex items-center gap-0.5 text-[#C5A059]">
                          {[...Array(review.rating || 5)].map((_, i) => (
                            <Star key={i} className="w-3.5 h-3.5 fill-[#C5A059] stroke-none" />
                          ))}
                        </div>
                        <span className="text-xs font-bold text-stone-900 font-sans">5.0</span>
                      </div>

                      <span className="inline-flex items-center gap-1 text-[10.5px] font-medium text-[#7A152E] bg-[#7A152E]/6 px-2.5 py-0.5 rounded-full border border-[#7A152E]/12">
                        <Check className="w-2.5 h-2.5 text-[#7A152E] stroke-[2.5]" />
                        <span>Verified Buyer</span>
                      </span>
                    </div>

                    {/* Headline Title */}
                    {review.title && (
                      <h4 className="font-serif text-base sm:text-[17px] font-medium text-stone-900 mt-4 leading-snug tracking-tight">
                        "{review.title}"
                      </h4>
                    )}

                    {/* Review Body */}
                    <p className="text-xs sm:text-[13px] text-stone-600 leading-relaxed font-normal mt-2.5">
                      {review.comment}
                    </p>
                  </div>

                  {/* Patron Info & Dedicated Piece Attribution Tag */}
                  <div className="mt-6 pt-4 border-t border-[#F0EBE3] flex items-center justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <div className="font-serif text-sm font-semibold text-stone-900 truncate">
                        {authorName}
                      </div>
                      <div className="text-[11px] text-stone-500 font-normal truncate mt-0.5">
                        {review.city} <span className="text-stone-300">&bull;</span> <span className="text-stone-400">{review.date}</span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <span className="text-[9px] uppercase tracking-widest text-stone-400 font-medium block">
                        Acquired Piece
                      </span>
                      <span className="text-xs font-semibold text-[#7A152E] block max-w-[145px] sm:max-w-[165px] truncate" title={productName}>
                        {productName}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

        </div>
      </section>

    </div>
  );
};
