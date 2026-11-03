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
      borderColor: '#CEBDA7',
      borderWidth: '1',
      innerRingColor: '#61532E',
      filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
      codeTextClass: 'text-[#61532E]',
      subTextClass: 'text-[#61532E]',
      stops: [
        { offset: '0%', color: '#FAF8F5' },
        { offset: '100%', color: '#FAF8F5' }
      ]
    };
  }

  if (isGold) {
    return {
      type: 'gold',
      code: '18K',
      metal: 'GOLD',
      label: '18K Gold Vermeil',
      borderColor: '#CEBDA7',
      borderWidth: '1',
      innerRingColor: '#61532E',
      filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
      codeTextClass: 'text-[#61532E]',
      subTextClass: 'text-[#61532E]',
      stops: [
        { offset: '0%', color: '#FAF8F5' },
        { offset: '100%', color: '#FAF8F5' }
      ]
    };
  }

  // Pure 925 Silver
  return {
    type: 'silver',
    code: '925',
    metal: 'SILVER',
    label: 'Pure 925 Silver',
    borderColor: '#CEBDA7',
    borderWidth: '1',
    innerRingColor: '#61532E',
    filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
    codeTextClass: 'text-[#61532E]',
    subTextClass: 'text-[#61532E]',
    stops: [
      { offset: '0%', color: '#FAF8F5' },
      { offset: '100%', color: '#FAF8F5' }
    ]
  };
};

/**
 * Luxury Emerald-Cut Ingot Hallmark Seal Badge
 * Features a minimalist, creative emerald-cut beveled octagonal silhouette
 * inspired by classic fine jewelry diamond cuts and Swiss/French bullion assay hallmarks.
 * Avoids generic circle (copyright) and ornate floral petals (overdesigned).
 */
export const MetalPurityBadge = ({ product, selectedMetal = null, size = 'rating', className = '' }) => {
  const reactId = useId();
  const safeId = reactId.replace(/[^a-zA-Z0-9_-]/g, '');
  const gradientId = `emerald-badge-grad-${safeId}`;

  const info = getMetalBadgeInfo(product, selectedMetal);

  // Rating-adjacent hallmark badge variant
  if (size === 'rating') {
    return (
      <div
        className={`inline-flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded-lg border shadow-2xs select-none transition-transform duration-200 shrink-0 ${className}`}
        style={{
          background: `linear-gradient(135deg, ${info.stops[0].color} 0%, ${info.stops[1].color} 30%, ${info.stops[2].color} 70%, ${info.stops[3].color} 100%)`,
          borderColor: info.borderColor,
          boxShadow: '0 1px 2px rgba(0,0,0,0.04)',
        }}
        title={info.label}
      >
        <span className={`font-serif font-bold tracking-tight text-[10px] sm:text-[11px] leading-none ${info.codeTextClass}`}>
          {info.code}
        </span>
        <span className={`font-sans font-bold uppercase tracking-wider text-[7.5px] sm:text-[8.5px] leading-none ${info.subTextClass}`}>
          {info.metal}
        </span>
      </div>
    );
  }

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
