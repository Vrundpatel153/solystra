import React from 'react';
import { X, MapPin, Clock, Phone, Calendar, ArrowUpRight } from 'lucide-react';

const BOUTIQUES = [
  {
    city: 'New Delhi',
    name: 'South Extension Flagship Atelier',
    address: 'E-14, Main Ring Road, South Extension Part II, New Delhi 110049',
    timing: 'Mon – Sun: 10:30 AM – 8:30 PM',
    phone: '+91 11 4987 6500',
    type: 'Flagship Atelier',
    highlight: 'Private Solitaire Suite & Hallmarking Assay Desk'
  },
  {
    city: 'Mumbai',
    name: 'Bandra West Studio',
    address: 'Plot 42, Waterfield Road, Bandra West, Mumbai 400050',
    timing: 'Mon – Sun: 11:00 AM – 9:00 PM',
    phone: '+91 22 2640 8820',
    type: 'Boutique & Studio',
    highlight: 'Bespoke Ring Suite & Laser Engraving Desk'
  },
  {
    city: 'Bengaluru',
    name: 'Indiranagar Galleria',
    address: '100 Feet Road, HAL 2nd Stage, Indiranagar, Bengaluru 560038',
    timing: 'Mon – Sun: 10:30 AM – 8:30 PM',
    phone: '+91 80 4122 3340',
    type: 'Fine Jewels Galleria',
    highlight: 'Complimentary Ultrasonic Cleaning & Polishing Bar'
  }
];

export const BoutiqueModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/65 backdrop-blur-sm flex items-center justify-center p-3 sm:p-6 font-sans">
      <div className="bg-[#FAF8F5] w-full max-w-xl rounded-2xl shadow-2xl border border-[#EAE4DC] overflow-hidden animate-slide-up flex flex-col max-h-[90vh]">
        
        {/* Modal Header */}
        <div className="p-4 sm:p-5 bg-white border-b border-[#EAE4DC] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-[#7A152E]/10 flex items-center justify-center text-[#7A152E] shrink-0">
              <MapPin className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-serif font-normal text-stone-900 leading-tight">
                Solystra Boutiques &amp; Lounges
              </h2>
              <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5">
                Visit our private ateliers across India
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-stone-400 hover:text-stone-800 rounded-full hover:bg-stone-100 transition-colors cursor-pointer"
            aria-label="Close boutiques modal"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body: Stores List */}
        <div className="p-3.5 sm:p-5 overflow-y-auto space-y-3.5">
          
          {/* Virtual Concierge Card (Fully responsive, no right cut-off) */}
          <div className="bg-[#7A152E]/5 border border-[#7A152E]/15 rounded-xl p-3.5 sm:p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-start gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#7A152E]/10 flex items-center justify-center text-[#7A152E] shrink-0 mt-0.5">
                <Calendar className="w-4 h-4" />
              </div>
              <div>
                <div className="text-[11px] font-bold text-[#7A152E] uppercase tracking-wider">
                  Virtual Atelier Concierge
                </div>
                <div className="text-xs text-stone-600 mt-0.5 leading-snug">
                  Prefer a 1-on-1 private walkthrough from home?
                </div>
              </div>
            </div>
            <a
              href="https://wa.me/919876543210?text=Hi%20Solystra,%20I%20would%20like%20to%20book%20a%20private%20virtual%20jewellery%20consultation."
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-4 py-2 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all shrink-0 flex items-center justify-center gap-1.5 shadow-xs cursor-pointer active:scale-98"
            >
              <span>Book Consult</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </a>
          </div>

          {/* Boutique Cards */}
          <div className="space-y-3">
            {BOUTIQUES.map((boutique, idx) => (
              <div
                key={idx}
                className="bg-white p-4 rounded-xl border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all shadow-2xs space-y-2.5"
              >
                {/* Header: City Tag + Store Type + Directions Link */}
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#7A152E]/8 border border-[#7A152E]/20 px-2 py-0.5 rounded-md">
                      {boutique.city}
                    </span>
                    <span className="text-[11px] text-stone-500 font-medium">
                      {boutique.type}
                    </span>
                  </div>

                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(boutique.address)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-0.5 text-xs text-[#7A152E] hover:text-[#590D1E] font-semibold transition-colors shrink-0"
                  >
                    <span>Directions</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </a>
                </div>

                {/* Name */}
                <h3 className="font-serif text-base font-normal text-stone-900 leading-snug">
                  {boutique.name}
                </h3>

                {/* Contact & Hours Info */}
                <div className="space-y-1.5 text-xs text-stone-600">
                  <div className="flex items-start gap-2">
                    <MapPin className="w-3.5 h-3.5 text-[#C5A059] shrink-0 mt-0.5" />
                    <span className="leading-snug text-stone-700">{boutique.address}</span>
                  </div>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-stone-500 pt-0.5">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-stone-400 shrink-0" />
                      <span>{boutique.timing}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Phone className="w-3.5 h-3.5 text-stone-400 shrink-0" />
                      <a href={`tel:${boutique.phone}`} className="hover:text-[#7A152E] font-medium text-stone-700">
                        {boutique.phone}
                      </a>
                    </div>
                  </div>
                </div>

                {/* Highlight Service Tag */}
                <div className="pt-2 border-t border-stone-100 flex items-center gap-2 text-[11px] text-stone-500">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#C5A059] shrink-0" />
                  <span>{boutique.highlight}</span>
                </div>
              </div>
            ))}
          </div>

        </div>

        {/* Modal Footer */}
        <div className="p-3.5 sm:p-4 bg-white border-t border-[#EAE4DC] flex items-center justify-between text-xs text-stone-500">
          <span className="text-[11px] text-stone-600">
            100% BIS Hallmarked 925 Silver &bull; Walk-ins Welcome
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 bg-stone-100 hover:bg-stone-200 text-stone-800 text-xs font-semibold rounded-xl transition-colors cursor-pointer"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
