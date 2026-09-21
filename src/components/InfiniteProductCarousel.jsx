import React, { useRef, useEffect, useCallback } from 'react';
import { ProductCard } from './ProductCard';

/**
 * InfiniteProductCarousel
 * - Renders products with seamless, infinite bidirectional looping (left & right).
 * - Displays exactly 2.5 products visible on mobile viewports so users immediately perceive horizontal swipeability.
 * - Scales to 4-5 products on tablet/desktop with responsive chevrons.
 * - Does not display any design count.
 */
export const InfiniteProductCarousel = ({
  products = [],
  id,
  title,
  subtitle,
  pill,
  code,
  onCopyCode,
  copiedCode
}) => {
  const scrollRef = useRef(null);

  // Triple products array to create seamless buffer sets on both left & right
  const loopProducts = [...products, ...products, ...products];

  // Set initial scroll position to the exact start of the middle set
  const centerCarousel = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const singleSetWidth = el.scrollWidth / 3;
    if (singleSetWidth > 0) {
      el.scrollLeft = singleSetWidth;
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(centerCarousel, 40);
    window.addEventListener('resize', centerCarousel);
    return () => {
      clearTimeout(timer);
      window.removeEventListener('resize', centerCarousel);
    };
  }, [centerCarousel, products]);

  // Seamless boundary wrap on scroll (touch swipe or button animated scroll)
  const handleScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    const singleSetWidth = el.scrollWidth / 3;
    if (singleSetWidth <= 0) return;

    // Teleport seamlessly if approaching outer boundaries
    if (el.scrollLeft < 20) {
      el.scrollLeft += singleSetWidth;
    } else if (el.scrollLeft >= singleSetWidth * 2 - 20) {
      el.scrollLeft -= singleSetWidth;
    }
  };


  const isCopied = code && copiedCode === code;

  return (
    <section id={id} className="py-6 sm:py-9 bg-white border-b border-[#EAE4DC] scroll-mt-36 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-[#EAE4DC]/80">
          <div>
            <div className="flex items-center gap-2 mb-1">
              {pill && (
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#7A152E] text-white tracking-wide shadow-2xs">
                  {pill}
                </span>
              )}
              {code ? (
                <span className="text-[11px] font-mono font-semibold text-stone-600 tracking-wider">
                  CODE: <strong className="text-[#7A152E]">{code}</strong>
                </span>
              ) : (
                <span className="text-[11px] font-sans font-medium text-emerald-700">
                  AUTOMATIC PRICING
                </span>
              )}
            </div>

            <h2 className="font-serif text-xl sm:text-2xl lg:text-3xl text-stone-900 font-normal tracking-tight">
              {title}
            </h2>
            {subtitle && (
              <p className="text-[11.5px] sm:text-xs text-stone-500 font-light mt-0.5">
                {subtitle}
              </p>
            )}
          </div>

          {/* Action Controls: 1-Click Code Copy */}
          <div className="flex items-center justify-between sm:justify-end gap-2.5">
            {code && onCopyCode && (
              <button
                type="button"
                onClick={() => onCopyCode(code)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-medium tracking-wide transition-all cursor-pointer shadow-2xs active:scale-95 ${
                  isCopied
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-800 font-semibold'
                    : 'bg-[#FAF8F5] hover:bg-[#7A152E] hover:text-white border-[#EAE4DC] text-stone-800 hover:border-[#7A152E]'
                }`}
                title={`Copy code ${code}`}
              >
                {isCopied ? (
                  <>
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-ping" />
                    <span className="font-bold text-emerald-700">COPIED!</span>
                  </>
                ) : (
                  <>
                    <span>Copy <strong>{code}</strong></span>
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* 2.5 Products Visible Carousel with Infinite Loop */}
        <div
          ref={scrollRef}
          onScroll={handleScroll}
          className="flex gap-2.5 sm:gap-4 overflow-x-auto no-scrollbar py-1.5 px-0.5 -mx-0.5"
          style={{
            scrollBehavior: 'smooth',
            WebkitOverflowScrolling: 'touch'
          }}
        >
          {loopProducts.map((product, index) => (
            <div
              key={`${product.id}-loop-${index}`}
              data-product-card="true"
              className="w-[calc((100vw-3.25rem)/2.5)] sm:w-[220px] md:w-[245px] lg:w-[270px] shrink-0 select-none"
            >
              <ProductCard product={product} />
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
