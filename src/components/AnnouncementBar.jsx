import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const MESSAGES = [
  'Free Insured Express Delivery Across India • 10% Off with Code SOULY10',
  '100% Certified BIS 925 Hallmarked Pure Silver Jewelry',
  'Signature Velvet Gift Packaging with Certificate on Every Order'
];

export const AnnouncementBar = () => {
  const [currentIdx, setCurrentIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIdx(prev => (prev + 1) % MESSAGES.length);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="bg-[#7A152E] text-white py-1.5 sm:py-2 px-3 sm:px-4 border-b border-[#590D1E] font-sans text-xs">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Left: Brand Support */}
        <div className="hidden md:block text-[11px] text-white/80">
          <a href="mailto:care@solystrajewels.com" className="hover:text-white transition-colors">
            care@solystrajewels.com
          </a>
        </div>

        {/* Center: Message Ticker */}
        <div className="flex-1 flex items-center justify-center gap-2 text-center">
          <button
            onClick={() => setCurrentIdx(prev => (prev === 0 ? MESSAGES.length - 1 : prev - 1))}
            className="text-white/60 hover:text-white p-0.5 transition-colors hidden sm:inline-flex cursor-pointer"
            aria-label="Previous announcement"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
          </button>

          <span className="text-[10.5px] sm:text-xs font-normal tracking-wide text-white/95 transition-opacity duration-300 truncate max-w-[85vw] sm:max-w-none block sm:inline">
            {MESSAGES[currentIdx]}
          </span>

          <button
            onClick={() => setCurrentIdx(prev => (prev + 1) % MESSAGES.length)}
            className="text-white/60 hover:text-white p-0.5 transition-colors hidden sm:inline-flex cursor-pointer"
            aria-label="Next announcement"
          >
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Right: Currency Indicator */}
        <div className="hidden md:block text-[11px] text-white/80 font-medium">
          <span>INR (₹)</span>
        </div>

      </div>
    </div>
  );
};
