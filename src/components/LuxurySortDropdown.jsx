import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';

export const LuxurySortDropdown = ({ value, onChange, options, isMobile = false }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Close when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Close on Escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') setIsOpen(false);
    };
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  const currentOption = options.find((opt) => opt.id === value) || options[0];

  return (
    <div className={`relative ${isMobile ? 'w-full' : ''}`} ref={dropdownRef}>
      {/* Trigger Button styled with brand luxury theme */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full flex items-center justify-between gap-2 bg-[#FAF8F5] hover:bg-[#F5F0EA] border text-stone-800 text-xs font-semibold rounded-xl transition-all cursor-pointer shadow-2xs ${
          isOpen ? 'border-[#7A152E] ring-1 ring-[#7A152E]/30 bg-white' : 'border-[#EAE4DC]'
        } ${isMobile ? 'py-2 px-3 justify-center' : 'px-3.5 py-1.5 min-w-[140px]'}`}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
      >
        <span className="truncate">{currentOption?.label || 'Sort'}</span>
        <ChevronDown
          className={`w-3.5 h-3.5 transition-transform duration-200 shrink-0 ${
            isOpen ? 'rotate-180 text-[#7A152E]' : 'text-stone-500'
          }`}
        />
      </button>

      {/* Luxury Theme Dropdown Menu (No native OS select, No bright blue highlight) */}
      {isOpen && (
        <div
          className={`absolute z-50 mt-1.5 bg-white border border-[#EAE4DC] rounded-xl shadow-xl py-1 overflow-hidden animate-in fade-in zoom-in-95 duration-150 ${
            isMobile
              ? 'left-0 right-0 w-full'
              : 'right-0 w-52'
          }`}
          role="listbox"
        >
          {/* Atelier Sort Header */}
          <div className="px-3.5 py-1 text-[10px] uppercase tracking-wider font-semibold text-stone-400 border-b border-[#EAE4DC]/60 mb-0.5">
            Sort Creations By
          </div>

          <div className="py-0.5">
            {options.map((opt) => {
              const isSelected = opt.id === value;
              return (
                <button
                  key={opt.id}
                  type="button"
                  onClick={() => {
                    onChange(opt.id);
                    setIsOpen(false);
                  }}
                  className={`w-full px-3.5 py-2 text-xs flex items-center justify-between transition-colors text-left cursor-pointer ${
                    isSelected
                      ? 'bg-[#7A152E]/10 text-[#7A152E] font-bold'
                      : 'text-stone-700 hover:bg-[#FAF8F5] hover:text-[#7A152E]'
                  }`}
                  role="option"
                  aria-selected={isSelected}
                >
                  <span className="tracking-wide">{opt.label}</span>
                  {isSelected && (
                    <Check className="w-3.5 h-3.5 text-[#7A152E] shrink-0 ml-2" />
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
