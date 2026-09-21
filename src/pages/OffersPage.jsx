import React, { useState } from 'react';
import { PRODUCTS } from '../data/catalog';
import { useShop } from '../context/ShopContext';
import { InfiniteProductCarousel } from '../components/InfiniteProductCarousel';
import {
  Tag,
  ShieldCheck,
  Truck,
  RotateCcw,
  Award,
  ArrowRight,
  ArrowLeft
} from 'lucide-react';

// Offer Tiers Configuration
const OFFER_TIERS = [
  {
    id: 'offer-royal15',
    code: 'ROYAL15',
    pill: '15% OFF',
    title: 'The Royal Festive Vault',
    subtitle: 'Orders above ₹4,999 • Pure 925 Sterling Silver & Solitaires',
    filter: (products) => products.slice(0, 6)
  },
  {
    id: 'offer-b2g1',
    code: 'B2G1',
    pill: 'BUY 2 GET 1 FREE',
    title: 'Curate Your Silver Stack',
    subtitle: 'Everyday silver rings, huggies & minimalist studs',
    filter: (products) =>
      products
        .filter((p) => p.category === 'rings' || p.category === 'earrings' || p.price < 4000)
        .slice(0, 6)
  },
  {
    id: 'offer-under2999',
    code: null,
    pill: 'UNDER ₹2,999',
    title: 'Accessible Luxury Essentials',
    subtitle: 'Certified pure 925 silver • No coupon needed',
    filter: (products) => products.filter((p) => p.price <= 3200).slice(0, 6)
  },
  {
    id: 'offer-vermeil10',
    code: 'VERMEIL10',
    pill: '10% OFF GOLD',
    title: '18K Italian Gold Vermeil Suite',
    subtitle: 'Layered tennis bracelets, cuffs & mirror chains',
    filter: (products) =>
      products
        .filter(
          (p) =>
            p.category === 'bracelets' ||
            (p.metals && p.metals.some((m) => m.toLowerCase().includes('gold')))
        )
        .slice(0, 6)
  },
  {
    id: 'offer-vault1500',
    code: 'VAULT1500',
    pill: 'SAVE ₹1,500',
    title: 'Bridal & Milestone Gift Sets',
    subtitle: 'Complete heirloom suites in keepsake velvet vault',
    filter: (products) =>
      products
        .filter((p) => p.category === 'complete_sets' || p.category === 'necklaces' || p.price > 5000)
        .slice(0, 6)
  }
];

export const OffersPage = ({ onBackToStore }) => {
  const { showToast, applyCoupon } = useShop();
  const [copiedCode, setCopiedCode] = useState(null);

  const handleCopyCode = (code) => {
    navigator.clipboard?.writeText(code);
    setCopiedCode(code);
    if (applyCoupon) {
      applyCoupon(code);
    } else {
      showToast(`Privilege code ${code} copied & applied to your bag!`);
    }
    setTimeout(() => {
      setCopiedCode(null);
    }, 3000);
  };

  const scrollToSection = (id, code) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    if (code) {
      handleCopyCode(code);
    }
  };

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] font-sans pb-24 lg:pb-16">
      
      {/* ========================================================
          1. SLEEK LUXURY EDITORIAL CAMPAIGN BANNER
          (High-fashion Vogue jewelry photography in compact scale)
          ======================================================== */}
      <section className="relative overflow-hidden bg-stone-900 border-b border-[#EAE4DC]">
        <div className="relative w-full h-36 xs:h-40 sm:h-48 md:h-56">
          <img
            src="solystra_assets/banners/offers_editorial_banner.jpg"
            alt="Solystra Fine Jewelry Offers Campaign"
            className="w-full h-full object-cover object-center"
          />

          {/* Luxury Editorial Scrim */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/85 via-black/55 to-black/30" />

          {/* Banner Content */}
          <div className="absolute inset-0 z-10 flex items-center">
            <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
              
              <button
                type="button"
                onClick={() => {
                  if (onBackToStore) onBackToStore();
                  else window.location.hash = '#/';
                }}
                className="hidden sm:inline-flex items-center gap-1.5 text-xs text-stone-300 hover:text-white transition-colors cursor-pointer mb-1.5 sm:mb-2 group"
              >
                <ArrowLeft className="w-3.5 h-3.5 group-hover:-translate-x-0.5 transition-transform" />
                <span>Return to Boutique</span>
              </button>

              <div className="max-w-xl">
                <span className="text-[9.5px] sm:text-[10.5px] uppercase tracking-[0.25em] text-[#EAD7AE] font-semibold block mb-0.5 sm:mb-1">
                  ATELIER PRIVILEGE VAULT
                </span>
                <h1 className="font-serif text-xl xs:text-2xl sm:text-3xl md:text-4xl text-white font-normal tracking-tight drop-shadow-md">
                  Exclusive Offers &amp; Rewards
                </h1>
                <p className="text-[11px] sm:text-xs md:text-sm text-stone-200 mt-1 font-light drop-shadow-sm max-w-md line-clamp-1 sm:line-clamp-none">
                  Certified pure 925 silver &amp; 18K Italian gold vermeil with keepsake velvet packaging.
                </p>
              </div>

            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          2. STICKY QUICK-JUMP FILTER PILLS
          ======================================================== */}
      <nav className="sticky top-0 z-30 bg-[#FAF8F5]/95 backdrop-blur-md border-b border-[#EAE4DC] py-2.5 px-4 sm:px-6 lg:px-8 shadow-xs">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
          <span className="text-[11px] uppercase tracking-wider font-bold text-stone-500 hidden sm:inline-block shrink-0">
            QUICK JUMP:
          </span>

          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5 w-full sm:w-auto">
            {OFFER_TIERS.map((tier) => (
              <button
                key={tier.id}
                type="button"
                onClick={() => scrollToSection(tier.id, tier.code)}
                className="shrink-0 px-3 py-1 rounded-full text-[11px] font-medium border border-[#EAE4DC] bg-white hover:bg-[#7A152E] hover:text-white hover:border-[#7A152E] text-stone-700 transition-all cursor-pointer shadow-2xs flex items-center gap-1 active:scale-95"
              >
                <Tag className="w-3 h-3 text-[#7A152E] group-hover:text-white" />
                <span>{tier.pill}</span>
                {tier.code && <span className="font-mono text-[9.5px] opacity-75">({tier.code})</span>}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* ========================================================
          3. THE 5 INFINITE LOOP PRODUCT CAROUSELS
          (Exactly 2.5 products visible on mobile for intuitive swiping)
          ======================================================== */}
      <div className="divide-y divide-[#EAE4DC]">
        {OFFER_TIERS.map((tier) => {
          const products = tier.filter(PRODUCTS);
          return (
            <InfiniteProductCarousel
              key={tier.id}
              id={tier.id}
              code={tier.code}
              pill={tier.pill}
              title={tier.title}
              subtitle={tier.subtitle}
              products={products}
              onCopyCode={handleCopyCode}
              copiedCode={copiedCode}
            />
          );
        })}
      </div>

      {/* ========================================================
          4. LUXURY TRUST ASSURANCE RIBBON
          ======================================================== */}
      <section className="py-8 bg-white border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="p-2.5">
              <ShieldCheck className="w-5 h-5 text-[#7A152E] mx-auto mb-1.5 stroke-[1.75]" />
              <h5 className="font-serif text-xs sm:text-sm font-semibold text-stone-900">BIS 925 Hallmarked</h5>
              <p className="text-[11px] text-stone-500 font-light mt-0.5">Government certified stamp</p>
            </div>
            <div className="p-2.5">
              <Truck className="w-5 h-5 text-[#7A152E] mx-auto mb-1.5 stroke-[1.75]" />
              <h5 className="font-serif text-xs sm:text-sm font-semibold text-stone-900">Insured Delivery</h5>
              <p className="text-[11px] text-stone-500 font-light mt-0.5">Free express across India</p>
            </div>
            <div className="p-2.5">
              <RotateCcw className="w-5 h-5 text-[#7A152E] mx-auto mb-1.5 stroke-[1.75]" />
              <h5 className="font-serif text-xs sm:text-sm font-semibold text-stone-900">7-Day Exchanges</h5>
              <p className="text-[11px] text-stone-500 font-light mt-0.5">Hassle-free doorstep pickup</p>
            </div>
            <div className="p-2.5">
              <Award className="w-5 h-5 text-[#7A152E] mx-auto mb-1.5 stroke-[1.75]" />
              <h5 className="font-serif text-xs sm:text-sm font-semibold text-stone-900">1-Year Warranty</h5>
              <p className="text-[11px] text-stone-500 font-light mt-0.5">Anti-tarnish replating guarantee</p>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          5. BOTTOM CALL TO ACTION: EXPLORE FULL CATALOG
          ======================================================== */}
      <section className="py-10 bg-[#FAF8F5] text-center">
        <div className="max-w-xl mx-auto px-4">
          <h2 className="font-serif text-xl sm:text-2xl text-stone-900 font-normal">
            Looking for something specific?
          </h2>
          <p className="text-xs text-stone-600 mt-1.5 font-light">
            Explore our complete collection with filters for price, category, and metal purities.
          </p>
          <div className="mt-4">
            <button
              onClick={() => {
                window.location.hash = '#/products';
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }}
              className="px-6 py-3 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs sm:text-sm font-medium rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer inline-flex items-center gap-2"
            >
              <span>Explore All Products</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

    </div>
  );
};
