import React, { useEffect } from 'react';
import {
  Shield,
  Layers,
  Award,
  RefreshCw,
  ArrowLeft,
  CheckCircle2,
  Lock,
  Truck,
  RotateCcw,
  Mail,
  Phone,
  HelpCircle,
  FileText
} from 'lucide-react';

export const TermsPage = ({ onBackToStore }) => {
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const handleBack = () => {
    if (onBackToStore) {
      onBackToStore();
    } else {
      window.location.hash = '#/';
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF8F5] text-stone-800">
      {/* Editorial Header */}
      <header className="bg-white border-b border-[#EAE4DC] py-12 sm:py-16">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="hidden sm:flex items-center gap-2 mb-6">
            <button
              onClick={handleBack}
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#7A152E] hover:text-[#590D1E] transition-colors cursor-pointer group"
            >
              <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
              <span>Back to Boutique</span>
            </button>
            <span className="text-stone-300">/</span>
            <span className="text-xs text-stone-500 uppercase tracking-widest font-medium">
              Terms &amp; Purity Standards
            </span>
            <span className="text-stone-300">&bull;</span>
            <a href="#/privacy" className="text-xs text-[#7A152E] hover:underline font-semibold">
              View Privacy &amp; Policy &rarr;
            </a>
          </div>

          <div className="max-w-3xl">
            <span className="text-xs uppercase tracking-widest text-[#7A152E] font-bold block mb-2">
              OFFICIAL ATELIER STANDARDS
            </span>
            <h1 className="font-serif text-3xl sm:text-5xl text-stone-900 font-normal leading-tight">
              Terms & Conditions & Purity Standards
            </h1>
            <p className="text-xs sm:text-sm text-stone-600 mt-3 font-light leading-relaxed">
              Effective Date: {new Date().getFullYear()} | Solystra Jewels Private Limited
            </p>
            <p className="text-sm sm:text-base text-stone-700 mt-3 leading-relaxed">
              Welcome to Solystra Jewels. We believe high jewelry should never compromise on metal honesty, elemental purity, or customer trust. Below are our official terms of service, craftsmanship guarantees, and the complete Solystra Purity Promise.
            </p>
          </div>

        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-16">
        
        {/* ========================================================
            THE SOLYSTRA PURITY PROMISE (MOVED FROM HOME PAGE)
            ======================================================== */}
        <section id="purity-promise" className="bg-white rounded-3xl p-6 sm:p-10 border border-[#EAE4DC] shadow-sm">
          <div className="text-center max-w-2xl mx-auto mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#7A152E]/10 border border-[#7A152E]/20 text-[#7A152E] text-[10.5px] font-bold uppercase tracking-wider mb-2">
              <Shield className="w-3.5 h-3.5" />
              <span>Government Recognized Standards</span>
            </div>
            <h2 className="font-serif text-2xl sm:text-4xl text-stone-900 font-normal">
              The Solystra Purity Promise
            </h2>
            <p className="text-xs sm:text-sm text-stone-500 mt-2">
              We reject hollow castings and flash platings. Every millimeter reflects honest materials, verified certifications, and lasting resilience.
            </p>
          </div>

          {/* 4 Pillars Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            
            {/* Pillar 1: BIS 925 Hallmark */}
            <div className="relative bg-[#FAF8F5] rounded-2xl border border-[#EAE4DC] p-6 flex flex-col justify-between items-center text-center hover:border-[#7A152E]/50 transition-colors">
              <div className="flex flex-col items-center w-full">
                <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-white text-[#7A152E] border border-[#EAE4DC] mb-4">
                  Govt. Recognized
                </span>

                <div className="w-14 h-14 rounded-2xl bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mb-4 shadow-2xs">
                  <Shield className="w-7 h-7 stroke-[1.5] text-[#7A152E]" />
                </div>

                <h3 className="font-serif text-base sm:text-lg text-stone-900 font-semibold leading-snug">
                  BIS 925 Hallmark Certified
                </h3>

                <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white border border-[#EAE4DC] text-[11px] font-medium text-[#8C6D23] my-3">
                  <span>Purity: 92.5% Fine Silver</span>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed font-light">
                  Every clasp and band is laser-inscribed with the official government BIS stamp, guaranteeing genuine 92.5% elemental purity with 100% hypoallergenic, nickel-free comfort.
                </p>
              </div>

              <div className="w-full pt-3 mt-4 border-t border-[#EAE4DC] flex items-center justify-center gap-1.5 text-[11px] text-[#7A152E] font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                <span>Laser-Stamped Purity Seal</span>
              </div>
            </div>

            {/* Pillar 2: Double-Micron Rhodium Shield */}
            <div className="relative bg-[#FAF8F5] rounded-2xl border border-[#EAE4DC] p-6 flex flex-col justify-between items-center text-center hover:border-[#7A152E]/50 transition-colors">
              <div className="flex flex-col items-center w-full">
                <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-white text-[#7A152E] border border-[#EAE4DC] mb-4">
                  10x Industry Standard
                </span>

                <div className="w-14 h-14 rounded-2xl bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mb-4 shadow-2xs">
                  <Layers className="w-7 h-7 stroke-[1.5] text-[#C5A059]" />
                </div>

                <h3 className="font-serif text-base sm:text-lg text-stone-900 font-semibold leading-snug">
                  Double-Micron Rhodium Shield
                </h3>

                <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white border border-[#EAE4DC] text-[11px] font-medium text-[#8C6D23] my-3">
                  <span>Thickness: 2.0µm Barrier</span>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed font-light">
                  Electro-clad with a heavy 2.0-micron barrier of platinum-family rhodium — 10x thicker than regular flash plating. Locks out moisture, sweat, and tarnishing.
                </p>
              </div>

              <div className="w-full pt-3 mt-4 border-t border-[#EAE4DC] flex items-center justify-center gap-1.5 text-[11px] text-[#7A152E] font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                <span>Zero Skin Discoloration</span>
              </div>
            </div>

            {/* Pillar 3: AAA+ Austrian Solitaires */}
            <div className="relative bg-[#FAF8F5] rounded-2xl border border-[#EAE4DC] p-6 flex flex-col justify-between items-center text-center hover:border-[#7A152E]/50 transition-colors">
              <div className="flex flex-col items-center w-full">
                <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-white text-[#7A152E] border border-[#EAE4DC] mb-4">
                  Hearts & Arrows Cut
                </span>

                <div className="w-14 h-14 rounded-2xl bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mb-4 shadow-2xs">
                  <Award className="w-7 h-7 stroke-[1.5] text-[#7A152E]" />
                </div>

                <h3 className="font-serif text-base sm:text-lg text-stone-900 font-semibold leading-snug">
                  AAA+ Austrian Solitaires
                </h3>

                <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white border border-[#EAE4DC] text-[11px] font-medium text-[#8C6D23] my-3">
                  <span>57-Facet Diamond Refraction</span>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed font-light">
                  Laboratory-crafted 57-facet Austrian crystals calibrated to mirror mined diamond fire. Individually hand-seated under microscopic loupes into solid prongs.
                </p>
              </div>

              <div className="w-full pt-3 mt-4 border-t border-[#EAE4DC] flex items-center justify-center gap-1.5 text-[11px] text-[#7A152E] font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                <span>Micro-Prong Precision Setting</span>
              </div>
            </div>

            {/* Pillar 4: 1-Year Plating Warranty */}
            <div className="relative bg-[#FAF8F5] rounded-2xl border border-[#EAE4DC] p-6 flex flex-col justify-between items-center text-center hover:border-[#7A152E]/50 transition-colors">
              <div className="flex flex-col items-center w-full">
                <span className="text-[10px] uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-white text-[#7A152E] border border-[#EAE4DC] mb-4">
                  Complimentary Renewal
                </span>

                <div className="w-14 h-14 rounded-2xl bg-white border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mb-4 shadow-2xs">
                  <RefreshCw className="w-7 h-7 stroke-[1.5] text-[#C5A059]" />
                </div>

                <h3 className="font-serif text-base sm:text-lg text-stone-900 font-semibold leading-snug">
                  1-Year Plating Warranty
                </h3>

                <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-white border border-[#EAE4DC] text-[11px] font-medium text-[#8C6D23] my-3">
                  <span>Free Doorstep Pickup & Spa</span>
                </div>

                <p className="text-xs text-stone-600 leading-relaxed font-light">
                  Our master artisans stand behind every piece. Enjoy 1 full year of complimentary doorstep pickup, deep ultrasonic cleaning, and full rhodium/vermeil replating.
                </p>
              </div>

              <div className="w-full pt-3 mt-4 border-t border-[#EAE4DC] flex items-center justify-center gap-1.5 text-[11px] text-[#7A152E] font-medium">
                <span className="w-1.5 h-1.5 rounded-full bg-[#7A152E]" />
                <span>Doorstep Pickup Included</span>
              </div>
            </div>

          </div>
        </section>

        {/* ========================================================
            DETAILED LEGAL & ATELIER TERMS
            ======================================================== */}
        <div className="space-y-10">

          {/* Section 1 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-medium mb-4 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                1
              </span>
              <span>Authentic Atelier Materials & BIS Hallmarking</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                1.1 All sterling silver pieces offered on Solystra Jewels are crafted from verified 92.5% pure silver alloy meeting Bureau of Indian Standards (BIS) Hallmarking criteria. Class A clasps, rings, and earring posts carry the certified laser stamp.
              </p>
              <p>
                1.2 18K Gold Vermeil pieces consist of a heavy minimum 2.5-micron layer of genuine 18-karat Italian gold bonded over a solid 925 sterling silver core (not brass, pot metal, or nickel-base alloys).
              </p>
              <p>
                1.3 Solystra certifies that all jewelry sold is 100% hypoallergenic, nickel-free, and lead-free, ensuring comfortable everyday wear even for sensitive skin.
              </p>
            </div>
          </div>

          {/* Section 2 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-medium mb-4 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                2
              </span>
              <span>1-Year Atelier Warranty & Replating Policy</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                2.1 Every purchase from Solystra Jewels is protected under our <strong>1-Year Atelier Warranty</strong> against premature tarnishing, peeling of plating, or stone setting looseness resulting from normal everyday wear.
              </p>
              <p>
                2.2 Under this warranty, customers may request up to one complimentary renewal session, which includes doorstep reverse pickup, microscopic claw inspection, ultrasonic jewelry bath, and fresh micron-rhodium or 18K vermeil replenishment.
              </p>
              <p>
                2.3 The warranty excludes physical breakage caused by excessive force, unauthorized third-party repairs, intentional damage, or severe acid/bleach exposure.
              </p>
            </div>
          </div>

          {/* Section 3 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-medium mb-4 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                3
              </span>
              <span>15-Day Easy Return & Exchange Terms</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                3.1 We offer a hassle-free 15-day return and exchange window from the confirmed date of delivery.
              </p>
              <p>
                3.2 To be eligible for a full refund or exchange, items must remain in original, unworn condition with intact security tags and the original royal suede velvet keepsake vault packaging.
              </p>
              <p>
                3.3 Our logistics team will arrange a free insured reverse pickup from your doorstep across 19,000+ pin codes in India. Refunds are processed back to the original payment method within 48 business hours after workshop verification.
              </p>
            </div>
          </div>

          {/* Section 4 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-medium mb-4 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                4
              </span>
              <span>Shipping, Transit Insurance & Delivery</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                4.1 All orders placed on Solystra Jewels include complimentary insured express delivery via tier-1 air logistics partners (BlueDart, Delhivery, Smartr).
              </p>
              <p>
                4.2 Every parcel is sealed in a tamper-evident security polybag with an OTP-verified delivery protocol. In the unlikely event of transit damage or loss, Solystra guarantees an immediate replacement or 100% refund.
              </p>
              <p>
                4.3 Typical delivery time is 2-4 business days for metro cities and 3-6 business days for the rest of India.
              </p>
            </div>
          </div>

          {/* Section 5 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-xl sm:text-2xl text-stone-900 font-medium mb-4 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                5
              </span>
              <span>Pricing, Payments & Security</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                5.1 All prices displayed on our website are in Indian Rupees (INR) and are inclusive of all applicable GST taxes.
              </p>
              <p>
                5.2 We accept UPI (Google Pay, PhonePe, Paytm), Visa, Mastercard, RuPay, NetBanking, and verified Cash on Delivery (COD) on eligible orders.
              </p>
              <p>
                5.3 All online transactions are processed through bank-grade 256-bit SSL encrypted gateways complying with RBI and PCI-DSS Level 1 certifications.
              </p>
            </div>
          </div>

        </div>

        {/* Contact Concierge Banner */}
        <div className="rounded-3xl p-8 bg-gradient-to-r from-[#7A152E] to-[#4A0D1C] text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
          <div>
            <span className="text-xs text-[#F5E6CC] font-bold uppercase tracking-widest block mb-1">
              HAVE QUESTIONS ABOUT OUR PURITY OR WARRANTY?
            </span>
            <h3 className="font-serif text-2xl sm:text-3xl font-normal">
              Speak with a Solystra Gemologist
            </h3>
            <p className="text-xs sm:text-sm text-stone-200 mt-1 max-w-xl font-light">
              Our dedicated atelier concierge is available 7 days a week to answer questions regarding hallmarking, certifications, or order support.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <a
              href="mailto:solystrajewels.official@gmail.com"
              className="px-5 py-2.5 rounded-xl bg-white text-[#7A152E] text-xs font-bold hover:bg-stone-100 transition-colors shadow-sm inline-flex items-center gap-2"
            >
              <Mail className="w-4 h-4" />
              <span>Email Atelier</span>
            </a>
            <a
              href="tel:+919122166904"
              className="px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white text-xs font-bold transition-colors inline-flex items-center gap-2"
            >
              <Phone className="w-4 h-4" />
              <span>+91 91221 66904</span>
            </a>
          </div>
        </div>

      </main>
    </div>
  );
};
