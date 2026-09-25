import React, { useId } from 'react';

/**
 * Accurately determines metal hallmark information from product data or selected variant.
 * Produces Pure 925 Silver, 18K Gold Vermeil, or 18K Rose Gold.
 */
export const getMetalBadgeInfo = (product, selectedMetal = null) => {
  const chosen = (selectedMetal || '').toLowerCase();

  const idLower = (product?.id || '').toLowerCase();
  const nameLower = (product?.name || '').toLowerCase();
  const shortLower = (product?.shortName || '').toLowerCase();
  const descLower = (product?.desc || '').toLowerCase();
  const puritySpec = (product?.specs?.['Metal Purity'] || '').toLowerCase();
  const primaryMetal = (product?.metals && product.metals[0] ? product.metals[0] : (product?.metal || '')).toLowerCase();
  const categoryLower = (product?.category || '').toLowerCase();
  const tagLower = (product?.tag || '').toLowerCase();

  const metalType = product?.metalType;

  // 1. Check Rose Gold
  const isRose =
    chosen.includes('rose') ||
    (!chosen && metalType === 'rose') ||
    (!chosen && !metalType && (
      primaryMetal.includes('rose') ||
      nameLower.includes('rose') ||
      idLower.includes('rose') ||
      shortLower.includes('rose') ||
      puritySpec.includes('rose') ||
      tagLower.includes('rose')
    ));

  // 2. Check 18K Gold (Yellow / Vermeil)
  const isGold =
    !isRose && (
      chosen.includes('gold') ||
      chosen.includes('vermeil') ||
      chosen.includes('yellow') ||
      (!chosen && metalType === 'gold') ||
      (!chosen && !metalType && (
        primaryMetal.includes('gold') ||
        primaryMetal.includes('vermeil') ||
        primaryMetal.includes('yellow') ||
        nameLower.includes('gold') ||
        nameLower.includes('golden') ||
        nameLower.includes('vermeil') ||
        shortLower.includes('gold') ||
        shortLower.includes('golden') ||
        shortLower.includes('vermeil') ||
        idLower.includes('gold') ||
        idLower.includes('golden') ||
        idLower.includes('vermeil') ||
        puritySpec.includes('gold') ||
        puritySpec.includes('vermeil') ||
        categoryLower === 'gold' ||
        tagLower.includes('gold') ||
        product?.isGold === true
      ))
    );

  if (isRose) {
    return {
      type: 'rose',
      code: '18K',
      metal: 'ROSE',
      label: '18K Rose Gold',
      borderColor: '#DF9FA9',
      borderWidth: '1.4',
      innerRingColor: '#C47585',
      filter: 'drop-shadow(0 2px 4px rgba(180, 80, 100, 0.22))',
      codeTextClass: 'text-[#7A152E]',
      subTextClass: 'text-[#9E2A44]',
      stops: [
        { offset: '0%', color: '#FFF9FA' },
        { offset: '30%', color: '#FDECEF' },
        { offset: '70%', color: '#F9D4DA' },
        { offset: '100%', color: '#EBB6C0' }
      ]
    };
  }

  if (isGold) {
    return {
      type: 'gold',
      code: '18K',
      metal: 'GOLD',
      label: '18K Gold Vermeil',
      // Warm champagne gold shade
      borderColor: '#CBA64E',
      borderWidth: '1.5',
      innerRingColor: '#BF973A',
      filter: 'drop-shadow(0 2px 5px rgba(180, 130, 40, 0.25))',
      codeTextClass: 'text-[#6B4B13]',
      subTextClass: 'text-[#8A641E]',
      stops: [
        { offset: '0%', color: '#FFFDF7' },
        { offset: '25%', color: '#FEF8E7' },
        { offset: '65%', color: '#F7E5BA' },
        { offset: '100%', color: '#ECCF86' }
      ]
    };
  }

  // Pure 925 Silver (Crisp White Silver Style)
  return {
    type: 'silver',
    code: '925',
    metal: 'SILVER',
    label: 'Pure 925 Silver',
    borderColor: '#CBD5E1',
    borderWidth: '1.35',
    innerRingColor: '#94A3B8',
    filter: 'drop-shadow(0 2px 4px rgba(15, 23, 42, 0.12))',
    codeTextClass: 'text-[#1E293B]',
    subTextClass: 'text-[#64748B]',
    stops: [
      { offset: '0%', color: '#FFFFFF' },
      { offset: '30%', color: '#F8FAFC' },
      { offset: '70%', color: '#EDF2F7' },
      { offset: '100%', color: '#E2E8F0' }
    ]
  };
};

/**
 * Luxury Emerald-Cut Ingot Hallmark Seal Badge
 * Features a minimalist, creative emerald-cut beveled octagonal silhouette
 * inspired by classic fine jewelry diamond cuts and Swiss/French bullion assay hallmarks.
 * Avoids generic circle (copyright) and ornate floral petals (overdesigned).
 */
export const MetalPurityBadge = ({ product, selectedMetal = null, size = 'md', className = '' }) => {
  const reactId = useId();
  const safeId = reactId.replace(/[^a-zA-Z0-9_-]/g, '');
  const gradientId = `emerald-badge-grad-${safeId}`;

  const info = getMetalBadgeInfo(product, selectedMetal);

  // Sizing matrix for container and typography
  const sizeClasses =
    size === 'lg'
      ? 'w-12 h-12 sm:w-14 sm:h-14'
      : size === 'sm'
      ? 'w-[33px] h-[33px] sm:w-[35px] sm:h-[35px]'
      : 'w-[38px] h-[38px] sm:w-[41px] sm:h-[41px]';

  const codeSizeClasses =
    size === 'lg'
      ? 'text-[12.5px] sm:text-[14px]'
      : size === 'sm'
      ? 'text-[8.5px] sm:text-[9.5px]'
      : 'text-[10px] sm:text-[11px]';

  const subSizeClasses =
    size === 'lg'
      ? 'text-[6.5px] sm:text-[7.5px]'
      : size === 'sm'
      ? 'text-[5px] sm:text-[5.5px]'
      : 'text-[5.5px] sm:text-[6.5px]';

  return (
    <div
      className={`${sizeClasses} relative flex items-center justify-center select-none pointer-events-none transition-transform duration-300 group-hover:scale-105 ${className}`}
      title={info.label}
    >
      {/* Rounded-Edge Cushion Hallmark Silhouette with Metallic Satin Gradient */}
      <svg
        viewBox="0 0 100 100"
        className="absolute inset-0 w-full h-full overflow-visible pointer-events-none"
        style={{ filter: info.filter }}
      >
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            {info.stops.map((stop, i) => (
              <stop key={i} offset={stop.offset} stopColor={stop.color} />
            ))}
          </linearGradient>
        </defs>

        {/* Outer Rounded-Edge Cushion Hallmark Ingot */}
        <rect
          x="7"
          y="7"
          width="86"
          height="86"
          rx="20"
          ry="20"
          fill={`url(#${gradientId})`}
          stroke={info.borderColor}
          strokeWidth={info.borderWidth}
        />

        {/* Concentric Inner Hairline Frame for Authentic Assay Stamp Ingot Feel */}
        <rect
          x="14"
          y="14"
          width="72"
          height="72"
          rx="14"
          ry="14"
          fill="none"
          stroke={info.innerRingColor}
          strokeWidth="0.75"
          opacity="0.45"
        />
      </svg>

      {/* Centered Hallmark Typography */}
      <div className="relative z-10 flex flex-col items-center justify-center text-center leading-none pointer-events-none mt-[-0.5px]">
        <span className={`font-serif font-bold tracking-tight ${codeSizeClasses} ${info.codeTextClass}`}>
          {info.code}
        </span>
        <span className={`font-sans font-bold uppercase tracking-[0.16em] ${subSizeClasses} ${info.subTextClass} mt-[1px]`}>
          {info.metal}
        </span>
      </div>
    </div>
  );
};
