import React, { useState } from 'react';
import { useShop } from '../context/ShopContext';
import { CheckCircle2, ArrowRight, X, Crown, Copy, ChevronDown } from 'lucide-react';

export const Footer = () => {
  const { showToast } = useShop();
  const [email, setEmail] = useState('');
  const [isSuccessModalOpen, setIsSuccessModalOpen] = useState(false);
  const [subscribedEmail, setSubscribedEmail] = useState('');
  const [copiedCode, setCopiedCode] = useState(false);
  const [openMobileAccordion, setOpenMobileAccordion] = useState(null);

  const toggleMobileAccordion = (name) => {
    setOpenMobileAccordion((prev) => (prev === name ? null : name));
  };

  const handleNewsletter = (e) => {
    e.preventDefault();
    if (email) {
      setSubscribedEmail(email);
      setIsSuccessModalOpen(true);
      showToast('Welcome to the Solystra Club! Use code SOULY10 for 10% off.');
      setEmail('');
    }
  };

  return (
    <footer className="bg-[#F7F4EE] text-stone-800 pt-10 sm:pt-16 pb-10 sm:pb-12 border-t border-stone-200/80 font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Newsletter Box - Mobile Compact & High-End Desktop */}
        <div className="bg-white rounded-2xl p-5 sm:p-8 lg:p-10 border border-stone-200/70 mb-8 sm:mb-14 shadow-xs">
          <div className="flex flex-col lg:flex-row items-center justify-between gap-5 sm:gap-6">
            <div className="max-w-xl text-center lg:text-left">
              <div className="text-[11px] uppercase tracking-wider text-[#7A152E] font-bold mb-1">
                Newsletter
              </div>
              <h3 className="font-serif text-xl sm:text-2xl lg:text-3xl text-stone-900 font-normal">
                Join the Solystra Club
              </h3>
              <p className="text-xs sm:text-sm text-stone-600 mt-1 font-normal">
                Sign up for exclusive previews, jewelry care guides, and 10% off your first order with code <strong className="text-stone-900 font-mono">SOULY10</strong>.
              </p>
            </div>

            <form onSubmit={handleNewsletter} className="flex gap-2 w-full lg:w-auto max-w-md">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email address"
                className="flex-1 min-w-0 px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl text-xs text-stone-800 placeholder-stone-400 focus:outline-none focus:border-[#7A152E] focus:bg-white transition-all"
                required
              />
              <button
                type="submit"
                className="px-5 sm:px-6 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-xs transition-colors shrink-0 cursor-pointer active:scale-98"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>

        {/* ========================================================
            MOBILE STREAMLINED ACCORDION DIRECTORY (< sm)
            Saves ~1000px of scrolling on mobile screens
            ======================================================== */}
        <div className="sm:hidden space-y-3 pb-8 border-b border-stone-200 text-xs">
          {/* Brand Intro Card */}
          <div className="p-4 bg-white/70 rounded-2xl border border-stone-200/80 space-y-2">
            <div className="cursor-pointer" onClick={() => { window.location.hash = '#/'; }}>
              <img
                src="solystra_assets/solystra_logo.png"
                alt="Solystra Jewels"
                className="h-7 w-auto object-contain"
              />
            </div>
            <p className="text-stone-600 text-[11.5px] leading-relaxed">
              Certified 925 sterling silver &amp; 18K gold atelier. Handcrafted with dual-micron rhodium for enduring brilliance.
            </p>
            <div className="text-[11px] text-stone-500 pt-1 border-t border-stone-100 flex items-center justify-between">
              <span>care@solystrajewels.com</span>
              <span className="text-[#7A152E] font-semibold">Mon–Sat (10AM–7PM)</span>
            </div>
          </div>

          {/* Accordion 1: Collections */}
          <div className="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs">
            <button
              onClick={() => toggleMobileAccordion('collections')}
              className="w-full px-4 py-3 flex items-center justify-between text-left font-semibold text-stone-900 uppercase tracking-wider text-[11px] cursor-pointer"
            >
              <span>Collections</span>
              <ChevronDown className={`w-4 h-4 text-stone-500 transition-transform duration-200 ${openMobileAccordion === 'collections' ? 'rotate-180 text-[#7A152E]' : ''}`} />
            </button>
            {openMobileAccordion === 'collections' && (
              <ul className="px-4 pb-3.5 space-y-2 text-stone-600 text-[11.5px] border-t border-stone-100 pt-2.5">
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">925 Sterling Silver Necklaces</a></li>
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">Solitaire and Stacking Rings</a></li>
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">Tennis Bracelets and Cuffs</a></li>
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">Earrings and Huggies</a></li>
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">Dainty Anklets</a></li>
                <li><a href="#/" onClick={() => { window.location.hash = '#/'; }} className="block hover:text-[#7A152E]">18K Italian Gold Vermeil</a></li>
              </ul>
            )}
          </div>

          {/* Accordion 2: Customer Care */}
          <div className="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs">
            <button
              onClick={() => toggleMobileAccordion('care')}
              className="w-full px-4 py-3 flex items-center justify-between text-left font-semibold text-stone-900 uppercase tracking-wider text-[11px] cursor-pointer"
            >
              <span>Customer Care &amp; Guides</span>
              <ChevronDown className={`w-4 h-4 text-stone-500 transition-transform duration-200 ${openMobileAccordion === 'care' ? 'rotate-180 text-[#7A152E]' : ''}`} />
            </button>
            {openMobileAccordion === 'care' && (
              <ul className="px-4 pb-3.5 space-y-2 text-stone-600 text-[11.5px] border-t border-stone-100 pt-2.5">
                <li><a href="#/" className="block hover:text-[#7A152E]">Track Your Order</a></li>
                <li><a href="#/terms" className="block hover:text-[#7A152E]">Shipping and Delivery</a></li>
                <li><a href="#/terms" className="block hover:text-[#7A152E]">15-Day Easy Returns</a></li>
                <li><a href="#/" className="block hover:text-[#7A152E]">Ring Sizing Guide</a></li>
                <li><a href="#/terms" className="block hover:text-[#7A152E]">Jewelry Care Guide</a></li>
                <li><a href="#/terms" className="block hover:text-[#7A152E]">BIS Hallmark Verification</a></li>
              </ul>
            )}
          </div>

          {/* Accordion 3: Our Promise */}
          <div className="bg-white rounded-xl border border-stone-200/80 overflow-hidden shadow-2xs">
            <button
              onClick={() => toggleMobileAccordion('promise')}
              className="w-full px-4 py-3 flex items-center justify-between text-left font-semibold text-stone-900 uppercase tracking-wider text-[11px] cursor-pointer"
            >
              <span>Our Purity Guarantee</span>
              <ChevronDown className={`w-4 h-4 text-stone-500 transition-transform duration-200 ${openMobileAccordion === 'promise' ? 'rotate-180 text-[#7A152E]' : ''}`} />
            </button>
            {openMobileAccordion === 'promise' && (
              <div className="px-4 pb-3.5 space-y-2 text-stone-700 text-[11.5px] border-t border-stone-100 pt-2.5">
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-[#C5A059] shrink-0" /><span>100% BIS Hallmarked 925 Silver</span></div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-[#C5A059] shrink-0" /><span>AAA+ Austrian Solitaire Crystals</span></div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-[#C5A059] shrink-0" /><span>Anti-Tarnish Dual Micron Rhodium</span></div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-[#C5A059] shrink-0" /><span>Free Insured Express Delivery</span></div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3.5 h-3.5 text-[#C5A059] shrink-0" /><span>Signature Velvet Keepsake Box</span></div>
                <div className="pt-2">
                  <a href="#/terms" className="text-[11px] text-[#7A152E] font-semibold underline">
                    Read Full Purity Terms &amp; Guarantee &rarr;
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ========================================================
            DESKTOP 4-COLUMN DIRECTORY (sm+)
            Preserves the expansive 4-column atelier layout
            ======================================================== */}
        <div className="hidden sm:grid sm:grid-cols-2 lg:grid-cols-4 gap-10 pb-12 border-b border-stone-200 text-xs">
          
          {/* Column 1: Brand Info with Official Logo */}
          <div className="space-y-4">
            <div className="cursor-pointer" onClick={() => { window.location.hash = '#/'; }}>
              <img
                src="solystra_assets/solystra_logo.png"
                alt="Solystra Jewels"
                className="h-9 w-auto object-contain"
              />
            </div>
            <p className="text-stone-600 leading-relaxed text-xs">
              Handcrafted fine jewelry in certified 925 sterling silver and 18K gold vermeil. Finished with dual-micron rhodium for enduring brilliance and hypoallergenic comfort.
            </p>
            <div className="pt-1 text-xs text-stone-600 space-y-1">
              <div>
                <strong className="text-stone-800">Email:</strong> care@solystrajewels.com
              </div>
              <div className="text-stone-500">
                Monday to Saturday (10:00 AM to 7:00 PM IST)
              </div>
            </div>
          </div>

          {/* Column 2: Collections */}
          <div>
            <h4 className="font-semibold text-stone-900 uppercase tracking-wider mb-4 text-xs">
              Collections
            </h4>
            <ul className="space-y-2.5 text-stone-600">
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  925 Sterling Silver Necklaces
                </a>
              </li>
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  Solitaire and Stacking Rings
                </a>
              </li>
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  Tennis Bracelets and Cuffs
                </a>
              </li>
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  Earrings and Huggies
                </a>
              </li>
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  Dainty Anklets
                </a>
              </li>
              <li>
                <a href="#/" onClick={() => { window.location.hash = '#/'; }} className="hover:text-[#7A152E] transition-colors">
                  18K Italian Gold Vermeil
                </a>
              </li>
            </ul>
          </div>

          {/* Column 3: Customer Care */}
          <div>
            <h4 className="font-semibold text-stone-900 uppercase tracking-wider mb-4 text-xs">
              Customer Care
            </h4>
            <ul className="space-y-2.5 text-stone-600">
              <li>
                <a href="#/" className="hover:text-[#7A152E] transition-colors">
                  Track Your Order
                </a>
              </li>
              <li>
                <a href="#/terms" className="hover:text-[#7A152E] transition-colors">
                  Shipping and Delivery
                </a>
              </li>
              <li>
                <a href="#/terms" className="hover:text-[#7A152E] transition-colors">
                  15-Day Easy Returns
                </a>
              </li>
              <li>
                <a href="#/" className="hover:text-[#7A152E] transition-colors">
                  Ring Sizing Guide
                </a>
              </li>
              <li>
                <a href="#/terms" className="hover:text-[#7A152E] transition-colors">
                  Jewelry Care Guide
                </a>
              </li>
              <li>
                <a href="#/terms" className="hover:text-[#7A152E] transition-colors">
                  BIS Hallmark Verification
                </a>
              </li>
            </ul>
          </div>

          {/* Column 4: Our Promise */}
          <div>
            <h4 className="font-semibold text-stone-900 uppercase tracking-wider mb-4 text-xs">
              Our Promise
            </h4>
            <div className="space-y-2.5 text-stone-700">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>100% BIS Hallmarked 925 Silver</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>AAA+ Austrian Solitaire Crystals</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>Anti-Tarnish Dual Micron Rhodium</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>Free Insured Express Delivery</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>Signature Velvet Keepsake Box</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-stone-200">
              <a
                href="#/terms"
                className="text-xs text-[#7A152E] font-semibold hover:underline inline-flex items-center gap-1 transition-colors"
              >
                <span>Read Full Purity Terms &amp; Guarantee &rarr;</span>
              </a>
            </div>
          </div>

        </div>

        {/* Bottom Bar: Legal & Payment Icons */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-stone-500">
          <div className="flex items-center gap-2 flex-wrap text-center sm:text-left justify-center sm:justify-start">
            <span>&copy; {new Date().getFullYear()} Solystra Jewels. All rights reserved.</span>
            <span className="text-stone-300 hidden sm:inline">&bull;</span>
            <a href="#/terms" className="hover:text-[#7A152E] transition-colors underline font-medium">
              Terms &amp; Conditions &amp; Purity Standards
            </a>
          </div>
          <div className="flex items-center gap-1.5 sm:gap-2 flex-wrap justify-center font-sans">
            <span className="text-stone-400 mr-1 text-[10.5px] sm:text-[11px]">100% Secure Checkout:</span>
            <span className="px-2 py-0.5 bg-white rounded text-stone-700 border border-stone-200 font-medium text-[10px]">UPI</span>
            <span className="px-2 py-0.5 bg-white rounded text-stone-700 border border-stone-200 font-medium text-[10px]">VISA</span>
            <span className="px-2 py-0.5 bg-white rounded text-stone-700 border border-stone-200 font-medium text-[10px]">Mastercard</span>
            <span className="px-2 py-0.5 bg-white rounded text-stone-700 border border-stone-200 font-medium text-[10px]">RuPay</span>
            <span className="px-2 py-0.5 bg-white rounded text-stone-700 border border-stone-200 font-medium text-[10px]">NetBanking</span>
          </div>
        </div>

      </div>

      {/* Luxury Newsletter Privilege Success Popup Modal with Royal Crown Emblem */}
      {isSuccessModalOpen && (
        <div
          className="fixed inset-0 z-50 overflow-y-auto bg-black/65 backdrop-blur-md flex items-center justify-center p-4 font-sans animate-fadeIn"
          onClick={() => setIsSuccessModalOpen(false)}
        >
          <div
            className="relative w-full max-w-lg bg-[#FAF8F5] rounded-3xl border border-[#EAE4DC] shadow-2xl overflow-hidden p-6 sm:p-8 animate-slide-up text-stone-900"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Ambient Gold & Burgundy Halos */}
            <div className="absolute -top-16 -right-16 w-44 h-44 rounded-full bg-[#C5A059]/20 blur-3xl pointer-events-none" />
            <div className="absolute -bottom-16 -left-16 w-44 h-44 rounded-full bg-[#7A152E]/15 blur-3xl pointer-events-none" />

            {/* Close Button */}
            <button
              onClick={() => setIsSuccessModalOpen(false)}
              className="absolute top-4 right-4 p-2 rounded-full bg-white/90 hover:bg-[#7A152E] text-stone-500 hover:text-white transition-all shadow-xs border border-stone-200 cursor-pointer"
              aria-label="Close privilege modal"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Luxury Crest Badge - Changed from Star/Sparkles to Royal Crown Emblem */}
            <div className="w-14 h-14 rounded-full bg-gradient-to-tr from-[#590D1E] via-[#7A152E] to-[#9B1D3D] border-2 border-[#C5A059] flex items-center justify-center shadow-lg mx-auto mb-3.5 text-[#F3DFB0]">
              <Crown className="w-7 h-7 stroke-[1.8]" />
            </div>

            {/* Header */}
            <span className="text-[10px] uppercase tracking-[0.25em] text-[#7A152E] font-bold block text-center mb-1">
              ATELIER PRIVILEGE &bull; SOLYSTRA CLUB
            </span>
            <h3 className="font-serif text-2xl sm:text-3xl font-normal text-stone-900 text-center tracking-tight">
              Welcome to the Inner Circle
            </h3>
            <p className="text-xs text-stone-600 mt-2 text-center max-w-sm mx-auto font-light leading-relaxed">
              Thank you for subscribing{subscribedEmail ? ` with ${subscribedEmail}` : ''}. Your personal welcome privilege is ready to claim:
            </p>

            {/* Interactive Voucher Card */}
            <div className="mt-5 p-4 sm:p-5 rounded-2xl bg-white border-2 border-dashed border-[#C5A059] shadow-xs relative overflow-hidden">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <span className="text-[9.5px] uppercase tracking-wider text-stone-500 font-semibold block">
                    EXCLUSIVE WELCOME PRIVILEGE
                  </span>
                  <div className="font-mono text-2xl sm:text-3xl font-extrabold tracking-widest text-[#7A152E] mt-0.5">
                    SOULY10
                  </div>
                  <span className="text-[10px] sm:text-[10.5px] text-stone-500 font-light block mt-0.5">
                    Flat 10% off &bull; Valid across all pure 925 silver &amp; 18K gold
                  </span>
                </div>

                <button
                  type="button"
                  onClick={() => {
                    navigator.clipboard.writeText('SOULY10');
                    setCopiedCode(true);
                    showToast('Voucher code SOULY10 copied to clipboard!');
                    setTimeout(() => setCopiedCode(false), 2500);
                  }}
                  className="px-4 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold rounded-xl transition-all shadow-xs flex items-center justify-center gap-2 cursor-pointer active:scale-95"
                >
                  <Copy className="w-3.5 h-3.5 text-[#C5A059]" />
                  <span>{copiedCode ? 'Copied!' : 'Copy Code'}</span>
                </button>
              </div>
            </div>

            {/* Privilege Benefits List */}
            <div className="mt-5 pt-4 border-t border-stone-200/80 space-y-2 text-stone-700 text-xs">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>Auto-applied to your next checkout upon pasting</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>Complimentary insured express priority shipping</span>
              </div>
              <div className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-[#C5A059] shrink-0" />
                <span>VIP concierge support on WhatsApp for ring &amp; wrist sizing</span>
              </div>
            </div>

            {/* Action CTA */}
            <div className="mt-6">
              <button
                type="button"
                onClick={() => setIsSuccessModalOpen(false)}
                className="w-full py-3 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-md transition-all cursor-pointer active:scale-98"
              >
                Start Exploring the Atelier
              </button>
            </div>

          </div>
        </div>
      )}

    </footer>
  );
};
