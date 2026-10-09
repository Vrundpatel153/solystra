import React from 'react';

// 1. Luxury Insured Express Delivery Icon (Refined 1.1px fine line art)
export const DeliveryIcon = ({ className = "w-5 h-5" }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.1"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {/* Van cargo trailer */}
    <rect x="3.4" y="6.4" width="10.4" height="8.8" rx="0.8" />
    <path d="M13.8 9.2h2.8l2.4 2.8v3.2h-5.2V9.2z" />
    {/* Wheels */}
    <circle cx="6.8" cy="17.0" r="1.8" />
    <circle cx="16.4" cy="17.0" r="1.8" />
    {/* Insured Protection Shield - Mathematically dead-centered inside the cargo box (center: 8.6, 10.8) */}
    <path
      d="M8.6 8.4L6.7 9.3v1.9c0 1.4.8 2.6 1.9 3.0 1.1-.4 1.9-1.6 1.9-3.0V9.3L8.6 8.4z"
      fill="rgba(20, 92, 89, 0.08)"
      stroke="#145C59"
      strokeWidth="0.85"
    />
    {/* Centered Checkmark inside the shield */}
    <path d="M7.6 10.8l0.7 0.7 1.4-1.4" stroke="#145C59" strokeWidth="0.9" />
  </svg>
);

// 2. BIS 925 Hallmark Certified Shield Icon (Scaled down to visually match the optical mass of other icons)
export const HallmarkIcon = ({ className = "w-5 h-5" }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.1"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {/* Shield outline - Balanced height and width matching truck and circular badges */}
    <path d="M12 4.6L6.8 6.8v4.6c0 3.7 2.2 6.9 5.2 7.8 3.0-.9 5.2-4.1 5.2-7.8V6.8L12 4.6z" />
    {/* Hallmark Diamond Accent */}
    <path d="M12 7.2l.6.6-.6.6-.6-.6.6-.6z" fill="#145C59" stroke="none" />
    {/* Verification Checkmark */}
    <path d="M9.3 12.3l1.8 1.8 3.6-3.8" stroke="#145C59" strokeWidth="1.2" />
  </svg>
);

// 3. 7-Day Doorstep Exchange Icon (Fine circular arrows with dainty, legible 7D badge)
export const ExchangeIcon = ({ className = "w-5 h-5" }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.1"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {/* Clockwise top arrow */}
    <path d="M19 11a7.5 7.5 0 0 0-13-3.2" />
    <path d="M6 4.2v3.6h3.6" />
    {/* Counter-clockwise bottom arrow */}
    <path d="M5 13a7.5 7.5 0 0 0 13 3.2" />
    <path d="M18 19.8v-3.6h-3.6" />
    {/* Delicate inner seal with crisp 7D text */}
    <circle cx="12" cy="12" r="3.6" fill="rgba(20, 92, 89, 0.04)" stroke="#145C59" strokeWidth="0.7" strokeOpacity="0.3" />
    <text
      x="12"
      y="13.3"
      textAnchor="middle"
      fill="#145C59"
      stroke="none"
      fontSize="3.6"
      fontWeight="600"
      fontFamily="system-ui, -apple-system, sans-serif"
      letterSpacing="0.2px"
    >
      7D
    </text>
  </svg>
);

// 4. 1-Year Warranty Medal Icon (Fine rosette medal with dainty, legible 1Y badge)
export const WarrantyIcon = ({ className = "w-5 h-5" }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.1"
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {/* Circular seal */}
    <circle cx="12" cy="9.4" r="5.6" />
    {/* Ribbon tails */}
    <path d="M9.0 14.2L7.6 20.6l4.4-1.7 4.4 1.7-1.4-6.4" strokeWidth="1.0" />
    {/* Inner subtle ring */}
    <circle cx="12" cy="9.4" r="3.7" strokeOpacity="0.25" strokeWidth="0.6" />
    {/* Center 1Y text */}
    <text
      x="12"
      y="10.7"
      textAnchor="middle"
      fill="#145C59"
      stroke="none"
      fontSize="3.6"
      fontWeight="600"
      fontFamily="system-ui, -apple-system, sans-serif"
      letterSpacing="0.2px"
    >
      1Y
    </text>
  </svg>
);

const TRUST_BADGES = [
  {
    id: 'delivery',
    title: 'Insured Delivery',
    mobileTitle: 'Insured Delivery',
    Icon: DeliveryIcon,
  },
  {
    id: 'hallmark',
    title: 'BIS 925 Hallmark',
    mobileTitle: 'BIS 925 Hallmark',
    Icon: HallmarkIcon,
  },
  {
    id: 'exchange',
    title: '7-Day Exchanges',
    mobileTitle: '7-Day Exchanges',
    Icon: ExchangeIcon,
  },
  {
    id: 'warranty',
    title: '1-Year Warranty',
    mobileTitle: '1-Year Warranty',
    Icon: WarrantyIcon,
  },
];

export const TrustBadgesRow = ({ variant = 'home', className = '' }) => {
  if (variant === 'product') {
    return (
      <div className={`grid grid-cols-4 gap-2 sm:gap-3.5 py-1 ${className}`}>
        {TRUST_BADGES.map((badge) => {
          const Icon = badge.Icon;
          return (
            <div
              key={badge.id}
              className="flex flex-col items-center justify-start text-center cursor-default group"
            >
              <div className="w-9 h-9 sm:w-10 sm:h-10 md:w-11 md:h-11 rounded-full bg-white border border-[#EAE4DC] flex items-center justify-center text-[#145C59] shadow-2xs mb-1.5 transition-colors group-hover:border-[#145C59]/30">
                <Icon className="w-6 h-6 sm:w-6.5 sm:h-6.5 md:w-7 md:h-7 text-[#145C59]" />
              </div>
              <span className="text-[10px] sm:text-xs md:text-[13px] font-medium text-stone-800 leading-snug">
                {badge.title}
              </span>
            </div>
          );
        })}
      </div>
    );
  }

  // Home Page Variant - Generous Luxury Sizing on PC, Single-Line Compact on Mobile
  return (
    <div className={`grid grid-cols-4 items-center ${className}`}>
      {TRUST_BADGES.map((badge, idx) => {
        const Icon = badge.Icon;
        return (
          <div
            key={badge.id}
            className={`flex flex-col sm:flex-row items-center justify-center text-center sm:text-left px-0.5 min-[360px]:px-1 sm:px-3 md:px-5 lg:px-6 py-2 sm:py-3.5 md:py-4 gap-1.5 sm:gap-3.5 md:gap-4 cursor-default relative ${
              idx > 0 ? 'border-l border-[#EAE4DC]/60' : ''
            }`}
          >
            <div className="w-8.5 h-8.5 min-[360px]:w-9 min-[360px]:h-9 min-[400px]:w-9.5 min-[400px]:h-9.5 sm:w-12 sm:h-12 md:w-13 md:h-13 lg:w-14 lg:h-14 rounded-full bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#145C59] shrink-0 shadow-2xs">
              <Icon className="w-5.5 h-5.5 min-[360px]:w-6 min-[360px]:h-6 sm:w-8 sm:h-8 md:w-9 md:h-9 lg:w-9.5 lg:h-9.5 text-[#145C59]" />
            </div>
            <div className="w-full min-w-0 flex items-center justify-center sm:justify-start">
              <h5 className="font-serif text-[9px] min-[360px]:text-[10px] min-[400px]:text-[11px] sm:text-sm md:text-[15.5px] lg:text-[17px] font-medium text-stone-900 leading-tight tracking-tight sm:tracking-normal whitespace-nowrap text-center sm:text-left">
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

