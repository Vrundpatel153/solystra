import React from 'react';

// 1. Custom Insured Delivery Icon (Active Driving Suspension, Spinning Wheels & Moving Road Track)
export const DeliveryIcon = ({ className = "w-5 h-5" }) => (
  <svg className={`${className} overflow-hidden`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
    {/* Moving Road Track */}
    <line x1="1" y1="21.5" x2="23" y2="21.5" stroke="#E0D7CC" strokeWidth="1.5" className="animate-road-move" />

    {/* Truck Main Body with Road Drive Suspension */}
    <g className="animate-truck-body">
      {/* Cargo trailer */}
      <rect x="1.5" y="4" width="12.5" height="11.5" rx="1.5" stroke="currentColor" strokeWidth="1.6" fill="rgba(122, 21, 46, 0.05)" />
      {/* Front cab */}
      <path d="M14 7.5h4l3 3.5v4.5h-7V7.5z" stroke="currentColor" strokeWidth="1.6" fill="rgba(122, 21, 46, 0.05)" />
      {/* Cab window */}
      <path d="M15 9h2.8l1.8 2H15V9z" stroke="#7A152E" strokeWidth="1" fill="rgba(122, 21, 46, 0.18)" />
      {/* Speed Wind Streaks on Cargo Body */}
      <line x1="4.5" y1="8" x2="9.5" y2="8" stroke="#7A152E" strokeWidth="1.4" className="animate-wind" />
      <line x1="3.5" y1="11" x2="7.5" y2="11" stroke="#7A152E" strokeWidth="1.4" className="animate-wind" style={{ animationDelay: '0.25s' }} />
    </g>

    {/* Rotating Wheels with Visible Spokes (Back & Front) */}
    <g className="animate-wheel-back">
      <circle cx="5.5" cy="18" r="2.5" stroke="currentColor" strokeWidth="1.6" fill="#FAF8F5" />
      <line x1="5.5" y1="15.5" x2="5.5" y2="20.5" stroke="#7A152E" strokeWidth="1" />
      <line x1="3" y1="18" x2="8" y2="18" stroke="#7A152E" strokeWidth="1" />
      <circle cx="5.5" cy="18" r="0.75" fill="#7A152E" stroke="none" />
    </g>

    <g className="animate-wheel-front">
      <circle cx="17.5" cy="18" r="2.5" stroke="currentColor" strokeWidth="1.6" fill="#FAF8F5" />
      <line x1="17.5" y1="15.5" x2="17.5" y2="20.5" stroke="#7A152E" strokeWidth="1" />
      <line x1="15" y1="18" x2="20" y2="18" stroke="#7A152E" strokeWidth="1" />
      <circle cx="17.5" cy="18" r="0.75" fill="#7A152E" stroke="none" />
    </g>
  </svg>
);

// 2. Custom BIS 925 Hallmark Certified Shield (Bold High-Contrast Checkmark with Verification Pulse)
export const HallmarkIcon = ({ className = "w-5 h-5" }) => (
  <svg className={`${className} overflow-hidden`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
    {/* Outer Shield with Gentle Certification Heartbeat */}
    <g className="animate-shield-pulse">
      <path
        d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"
        stroke="currentColor"
        strokeWidth="1.6"
        fill="rgba(122, 21, 46, 0.05)"
      />
      {/* Inner Hallmark Inset Contour Line */}
      <path
        d="M12 19.5s5.8-2.8 5.8-7.5V6.5l-5.8-2-5.8 2V12c0 4.7 5.8 7.5 5.8 7.5z"
        stroke="#E0D7CC"
        strokeWidth="0.8"
        strokeDasharray="2 1.5"
      />
    </g>

    {/* Purity Diamond Sparkle at Top of Shield */}
    <g className="animate-sparkle-shine">
      <polygon points="12 4.8 12.7 6.3 14.2 7 12.7 7.7 12 9.2 11.3 7.7 9.8 7 11.3 6.3" fill="#7A152E" stroke="none" />
    </g>

    {/* The Animated Checkmark in the Middle - BOLD, DEEP BURGUNDY, CRISP & 100% VISIBLE (ZERO YELLOW!) */}
    <g className="animate-hallmark-tick">
      <path
        d="M8.5 12.2l2.5 2.5 4.8-5"
        stroke="#7A152E"
        strokeWidth="2.4"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </g>
  </svg>
);

// 3. Custom 7-Day Doorstep Exchange (360-Degree Continuous Cycling Arrows with Stable Bold Center "7")
export const ExchangeIcon = ({ className = "w-5 h-5" }) => (
  <svg className={`${className} overflow-hidden`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
    {/* Outer Circular Exchange Ring Cycling Continuously */}
    <g className="animate-exchange-ring">
      <path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" stroke="currentColor" strokeWidth="1.6" />
      <polygon points="3 3 3 8 8 8" fill="currentColor" stroke="currentColor" strokeWidth="1" />
      
      <path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16" stroke="currentColor" strokeWidth="1.6" />
      <polygon points="21 21 21 16 16 16" fill="currentColor" stroke="currentColor" strokeWidth="1" />
    </g>

    {/* Center High-Contrast Bold "7" - Deep Burgundy & Crisp, with Subtle Breath Pulse */}
    <g className="animate-exchange-number">
      <circle cx="12" cy="12" r="4.2" fill="#FAF8F5" stroke="#E0D7CC" strokeWidth="0.8" />
      <text
        x="12"
        y="14.6"
        textAnchor="middle"
        fill="#7A152E"
        stroke="none"
        fontSize="7.8"
        fontWeight="800"
        fontFamily="serif"
      >
        7
      </text>
    </g>
  </svg>
);

// 4. Custom 1-Year Plating Warranty Medal (Clock Hand Sweeps Around Dial & Ribbon Gently Flutters)
export const WarrantyIcon = ({ className = "w-5 h-5" }) => (
  <svg className={`${className} overflow-hidden`} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round">
    {/* Medal Ribbon Tails with Subtle Flutter */}
    <g className="animate-ribbon">
      <path
        d="M8.2 13.8L7 22l5-2.5 5 2.5-1.2-8.2"
        stroke="currentColor"
        strokeWidth="1.6"
        fill="rgba(122, 21, 46, 0.06)"
      />
    </g>

    {/* Medal Round Face */}
    <g className="animate-medal">
      <circle cx="12" cy="9" r="6.5" stroke="currentColor" strokeWidth="1.6" fill="#FAF8F5" />
      {/* Inner dial marker ring */}
      <circle cx="12" cy="9" r="4.8" stroke="#E0D7CC" strokeWidth="0.8" strokeDasharray="1.5 1.5" />
      {/* Center Pivot Dot */}
      <circle cx="12" cy="9" r="1.2" fill="#7A152E" stroke="none" />
      
      {/* Precision 1-Year Sweeping Clock Hand */}
      <g className="animate-clock-hand">
        <line x1="12" y1="9" x2="12" y2="5" stroke="#7A152E" strokeWidth="1.8" strokeLinecap="round" />
      </g>
      {/* Fixed Hour Hand at 3 o'clock */}
      <line x1="12" y1="9" x2="14.5" y2="9" stroke="#7A152E" strokeWidth="1.5" strokeLinecap="round" />
    </g>
  </svg>
);

const TRUST_BADGES = [
  {
    id: 'delivery',
    title: 'Insured Delivery',
    mobileTitle: 'Insured Delivery',
    subtitle: 'Free BlueDart express across India',
    mobileSubtitle: 'BlueDart Express',
    Icon: DeliveryIcon,
  },
  {
    id: 'hallmark',
    title: 'BIS 925 Hallmark',
    mobileTitle: 'BIS 925 Hallmark',
    subtitle: 'Government tested purity',
    mobileSubtitle: 'Tested Purity',
    Icon: HallmarkIcon,
  },
  {
    id: 'exchange',
    title: '7-Day Exchanges',
    mobileTitle: '7-Day Exchanges',
    subtitle: 'Hassle-free doorstep pickup',
    mobileSubtitle: 'Doorstep Pickup',
    Icon: ExchangeIcon,
  },
  {
    id: 'warranty',
    title: '1-Year Plating Warranty',
    mobileTitle: '1-Year Warranty',
    subtitle: 'Anti-tarnish micron guarantee',
    mobileSubtitle: 'Plating Guarantee',
    Icon: WarrantyIcon,
  },
];

export const TrustBadgesRow = ({ variant = 'home', className = '' }) => {
  if (variant === 'product') {
    return (
      <div className={`grid grid-cols-4 divide-x divide-stone-200 bg-white rounded-xl border border-stone-200 shadow-2xs overflow-hidden ${className}`}>
        {TRUST_BADGES.map((badge) => {
          const Icon = badge.Icon;
          return (
            <div
              key={badge.id}
              className="flex flex-col sm:flex-row items-center justify-center sm:justify-start text-center sm:text-left gap-1 sm:gap-2.5 p-2 sm:p-3"
            >
              <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shrink-0 shadow-2xs">
                <Icon className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              </div>
              <div className="min-w-0">
                <span className="block font-medium text-stone-800 text-[9.5px] sm:text-xs leading-tight">
                  <span className="sm:hidden">{badge.mobileTitle}</span>
                  <span className="hidden sm:inline">{badge.title}</span>
                </span>
                <span className="hidden md:block text-[10px] text-stone-500 leading-tight mt-0.5">
                  {badge.mobileSubtitle}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  // Home Page Variant
  return (
    <div className={`grid grid-cols-4 divide-x divide-[#EAE4DC]/80 items-center ${className}`}>
      {TRUST_BADGES.map((badge) => {
        const Icon = badge.Icon;
        return (
          <div
            key={badge.id}
            className="flex flex-col sm:flex-row items-center justify-center sm:justify-start text-center sm:text-left px-0.5 sm:px-4 py-1 sm:py-2.5 gap-1 sm:gap-3.5 group cursor-default"
          >
            <div className="w-7 h-7 sm:w-11 sm:h-11 rounded-lg sm:rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shrink-0 shadow-2xs group-hover:border-[#7A152E]/40 group-hover:bg-white group-hover:shadow-xs transition-all">
              <Icon className="w-3.5 h-3.5 sm:w-5.5 sm:h-5.5" />
            </div>
            <div className="min-w-0 max-w-full">
              <h5 className="font-serif text-[9.5px] xs:text-[11px] sm:text-base md:text-[17px] lg:text-lg font-semibold sm:font-medium text-stone-900 leading-tight sm:leading-snug tracking-tight whitespace-nowrap">
                <span className="sm:hidden">{badge.mobileTitle}</span>
                <span className="hidden sm:inline">{badge.title}</span>
              </h5>
            </div>
          </div>
        );
      })}
    </div>
  );
};
