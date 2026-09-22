import React, { useEffect } from 'react';
import { ArrowLeft, Sparkles, ArrowRight } from 'lucide-react';

export const ALL_CATEGORIES = [
  {
    id: 'necklaces',
    name: 'Necklaces & Pendants',
    shortName: 'Necklaces',
    count: '14 Designs',
    desc: 'Austrian crystal solitaires, layering lariats & choker suites.',
    img: 'solystra_assets/categories/zavya_style/necklaces.png'
  },
  {
    id: 'earrings',
    name: 'Earrings & Studs',
    shortName: 'Earrings',
    count: '10 Designs',
    desc: 'Classic studs, huggies, drops & statement chandelier earrings.',
    img: 'solystra_assets/categories/zavya_style/earrings.png'
  },
  {
    id: 'bracelets',
    name: 'Bracelets & Cuffs',
    shortName: 'Bracelets',
    count: '12 Designs',
    desc: 'Italian gold vermeil tennis links, kada cuffs & charm bracelets.',
    img: 'solystra_assets/categories/zavya_style/bracelets.png'
  },
  {
    id: 'rings',
    name: 'Rings & Bands',
    shortName: 'Rings',
    count: '8 Designs',
    desc: 'Eternity promise bands, cocktail solitaires & adjustable rings.',
    img: 'solystra_assets/categories/zavya_style/rings.png'
  },
  {
    id: 'anklets',
    name: 'Anklets & Payals',
    shortName: 'Anklets',
    count: '6 Designs',
    desc: 'Delicate pure 925 sterling silver payals & barefoot shimmer chains.',
    img: 'solystra_assets/categories/zavya_style/anklets.png'
  },
  {
    id: 'complete_sets',
    name: 'Gift Suites & Sets',
    shortName: 'Gift Suites',
    count: '6 Sets',
    desc: 'Complete necklace, earring & bracelet sets in velvet keepsake boxes.',
    img: 'solystra_assets/categories/zavya_style/complete_sets.png'
  },
  {
    id: 'chains',
    name: 'Classic Layering Chains',
    shortName: 'Chains',
    count: '8 Designs',
    desc: 'Timeless Italian curb, box & rope chains for everyday luxury.',
    img: 'solystra_assets/categories/zavya_style/chains.png'
  },
  {
    id: 'mangalsutras',
    name: 'Sacred Mangalsutras',
    shortName: 'Mangalsutra',
    count: '8 Designs',
    desc: 'Traditional auspicious black bead craftsmanship with contemporary flair.',
    img: 'solystra_assets/categories/zavya_style/mangalsutras.png'
  },
  {
    id: 'nose_pins',
    name: 'Solitaire Nose Pins',
    shortName: 'Nose Pins',
    count: '6 Designs',
    desc: 'Micro-prong Austrian crystal solitaires in solid 925 sterling silver.',
    img: 'solystra_assets/categories/zavya_style/nose_pins.png'
  },
  {
    id: 'mens_collection',
    name: "Men's Silver Collection",
    shortName: "Men's Silver",
    count: '7 Designs',
    desc: 'Bold kada cuffs, heavy link bracelets & minimalist signet rings.',
    img: 'solystra_assets/categories/zavya_style/mens.png'
  }
];

export const CategoriesPage = ({ onSelectCategory, onBackToStore }) => {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleCategoryClick = (catId) => {
    if (onSelectCategory) {
      onSelectCategory(catId);
    } else {
      window.location.hash = `#/products?category=${catId}`;
    }
  };

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] font-sans pb-24 lg:pb-16">
      
      {/* ========================================================
          1. SLEEK LUXURY EDITORIAL CATEGORY BANNER
          ======================================================== */}
      <section className="relative overflow-hidden bg-stone-900 border-b border-[#EAE4DC]">
        <div className="relative w-full h-36 xs:h-40 sm:h-48 md:h-56">
          <img
            src="solystra_assets/banners/explore_editorial_banner.jpg"
            alt="Solystra Jewelry Categories Archive"
            className="w-full h-full object-cover object-center"
          />

          {/* Luxury Editorial Scrim */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/60 to-black/25" />

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
                <span className="text-[9.5px] sm:text-[10.5px] uppercase tracking-[0.25em] text-[#EAD7AE] font-semibold block mb-0.5 sm:mb-1 flex items-center gap-1.5">
                  <Sparkles className="w-3 h-3 text-[#EAD7AE]" />
                  <span>ATELIER CATEGORY ARCHIVE</span>
                </span>
                <h1 className="font-serif text-xl xs:text-2xl sm:text-3xl md:text-4xl text-white font-normal tracking-tight drop-shadow-md">
                  Explore by Category
                </h1>
                <p className="text-[11px] sm:text-xs md:text-sm text-stone-200 mt-1 font-light drop-shadow-sm max-w-md line-clamp-1 sm:line-clamp-none">
                  Discover handcrafted 925 sterling silver, Austrian solitaires &amp; 18K gold suites curated by master artisans.
                </p>
              </div>

            </div>
          </div>
        </div>
      </section>

      {/* ========================================================
          2. FULL-SIZE CATEGORIES GRID
          ======================================================== */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        
        {/* Section Intro Header */}
        <div className="flex items-center justify-between pb-3 sm:pb-4 mb-6 border-b border-[#EAE4DC]">
          <div>
            <span className="text-[10.5px] uppercase tracking-widest text-[#7A152E] font-semibold block mb-0.5">
              ALL ATELIER SILHOUETTES
            </span>
            <h2 className="font-serif text-xl sm:text-2xl text-stone-900 font-normal">
              Curated Collections &amp; Designs ({ALL_CATEGORIES.length})
            </h2>
          </div>
          
          <button
            onClick={() => {
              window.location.hash = '#/products';
            }}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#7A152E] hover:text-[#590D1E] group transition-colors cursor-pointer"
          >
            <span>Explore All Catalog</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>

        {/* Full-Size Category Cards Grid: 2 cols on mobile, 3 on tablet, 4 on desktop, 5 on xl */}
        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3.5 sm:gap-5 lg:gap-6">
          {ALL_CATEGORIES.map((cat) => (
            <div
              key={cat.id}
              onClick={() => handleCategoryClick(cat.id)}
              className="group bg-white rounded-2xl sm:rounded-3xl border border-[#EAE4DC] hover:border-[#7A152E]/30 p-2.5 sm:p-3.5 transition-all duration-500 hover:shadow-lg flex flex-col cursor-pointer hover:-translate-y-1"
            >
              {/* Squircle Image Card with Gradient Halo */}
              <div className="relative w-full aspect-square rounded-xl sm:rounded-2xl p-[2px] bg-gradient-to-tr from-[#7A152E]/80 via-[#D4AF37] to-[#F6E3B8] group-hover:from-[#D4AF37] group-hover:via-[#F6E3B8] group-hover:to-[#7A152E] transition-all duration-500 shadow-2xs">
                <div className="w-full h-full rounded-[10px] sm:rounded-[14px] overflow-hidden bg-white relative flex items-center justify-center">
                  <img
                    src={cat.img}
                    alt={cat.name}
                    className="w-full h-full object-cover group-hover:scale-108 transition-transform duration-700"
                    loading="lazy"
                  />
                  {/* Subtle Specular Ambient Sheen */}
                  <div className="absolute inset-0 bg-gradient-to-t from-[#7A152E]/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
              </div>

              {/* Text Info */}
              <div className="pt-3 sm:pt-4 flex-1 flex flex-col justify-between text-center">
                <div>
                  <h3 className="font-serif text-sm sm:text-base lg:text-lg font-semibold text-stone-900 group-hover:text-[#7A152E] transition-colors leading-snug">
                    {cat.name}
                  </h3>
                  <p className="text-[10px] sm:text-[11px] text-stone-400 font-light mt-1 line-clamp-2 leading-relaxed hidden sm:block">
                    {cat.desc}
                  </p>
                </div>

                <div className="pt-2 sm:pt-3 mt-auto border-t border-[#EAE4DC]/60 flex items-center justify-between text-[10px] sm:text-xs text-stone-500">
                  <span className="font-medium text-stone-600">{cat.count}</span>
                  <span className="inline-flex items-center gap-1 font-semibold text-[#7A152E] group-hover:underline">
                    <span>Shop</span>
                    <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

      </section>

    </div>
  );
};
