import React from 'react';

/**
 * Accurately determines metal hallmark information from product data.
 * Produces 925 Silver, 18K Gold Vermeil, or 18K Rose Gold.
 */
export const getMetalBadgeInfo = (product) => {
  if (!product) {
    return {
      code: '925',
      metal: 'SILVER',
      label: 'Pure 925 Silver',
      badgeClass: 'bg-gradient-to-br from-white/95 via-slate-100/95 to-slate-200/90 border-slate-300/85 text-slate-800 ring-slate-400/20 shadow-[0_3px_10px_rgba(0,0,0,0.09),inset_0_1px_1px_rgba(255,255,255,0.95)]',
      subTextClass: 'text-slate-600'
    };
  }

  const nameLower = (product.name || '').toLowerCase();
  const puritySpec = (product.specs?.['Metal Purity'] || '').toLowerCase();

  const isRose = nameLower.includes('rose') || puritySpec.includes('rose');
  const isGold = !isRose && (nameLower.includes('gold') || nameLower.includes('vermeil') || puritySpec.includes('gold') || puritySpec.includes('vermeil'));

  if (isRose) {
    return {
      code: '18K',
      metal: 'ROSE',
      label: '18K Rose Gold',
      badgeClass: 'bg-gradient-to-br from-[#FFF9F9]/95 via-[#FDECEE]/95 to-[#F9D5D9]/90 border-[#EBB6BC]/85 text-[#7A152E] ring-[#B76E79]/25 shadow-[0_3px_10px_rgba(180,90,100,0.14),inset_0_1px_1px_rgba(255,255,255,0.95)]',
      subTextClass: 'text-[#9A2D45]'
    };
  }

  if (isGold) {
    return {
      code: '18K',
      metal: 'GOLD',
      label: '18K Gold Vermeil',
      badgeClass: 'bg-gradient-to-br from-[#FFFDF7]/95 via-[#FDF5E6]/95 to-[#F5E2B8]/90 border-[#E5C985]/85 text-[#6B4E1B] ring-[#D4AF37]/25 shadow-[0_3px_10px_rgba(180,130,50,0.14),inset_0_1px_1px_rgba(255,255,255,0.95)]',
      subTextClass: 'text-[#8C6826]'
    };
  }

  return {
    code: '925',
    metal: 'SILVER',
    label: 'Pure 925 Silver',
    badgeClass: 'bg-gradient-to-br from-white/95 via-slate-100/95 to-slate-200/90 border-slate-300/85 text-slate-800 ring-slate-400/20 shadow-[0_3px_10px_rgba(0,0,0,0.09),inset_0_1px_1px_rgba(255,255,255,0.95)]',
    subTextClass: 'text-slate-600'
  };
};

/**
 * Luxury Circular Hallmark Medallion Badge
 * Placed at the top-left of product cards replacing raw percentage off.
 * Features luminous metallic gradients, fine hairline rings, and crisp atelier typography.
 */
export const MetalPurityBadge = ({ product, size = 'md', className = '' }) => {
  const info = getMetalBadgeInfo(product);

  const sizeClasses = size === 'lg'
    ? 'w-11 h-11 sm:w-12 sm:h-12 text-[12px] sm:text-[13px]'
    : size === 'sm'
    ? 'w-8 h-8 text-[9.5px]'
    : 'w-[38px] h-[38px] sm:w-[42px] sm:h-[42px] text-[10.5px] sm:text-[11.5px]';

  const subSizeClasses = size === 'lg'
    ? 'text-[7px] sm:text-[7.5px]'
    : size === 'sm'
    ? 'text-[6px]'
    : 'text-[6.5px] sm:text-[7px]';

  return (
    <div
      className={`${sizeClasses} rounded-full border ring-1 ring-inset flex flex-col items-center justify-center text-center select-none backdrop-blur-xs transition-transform duration-300 group-hover:scale-105 pointer-events-none ${info.badgeClass} ${className}`}
      title={info.label}
    >
      <span className="font-serif font-bold leading-none tracking-tight">
        {info.code}
      </span>
      <span className={`${subSizeClasses} font-semibold uppercase tracking-[0.14em] leading-none mt-0.5 ${info.subTextClass}`}>
        {info.metal}
      </span>
    </div>
  );
};
