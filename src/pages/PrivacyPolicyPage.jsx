import React, { useEffect } from 'react';
import {
  ShieldCheck,
  Award,
  RefreshCw,
  ArrowLeft,
  Lock,
  EyeOff,
  FileText,
  Mail,
  Phone,
  CheckCircle2,
  PackageCheck
} from 'lucide-react';

export const PrivacyPolicyPage = ({ onBackToStore }) => {
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
    <div className="min-h-screen bg-[#FAF8F5] text-stone-800 font-sans">
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
              Legal &amp; Trust
            </span>
          </div>

          <div className="max-w-3xl">
            <span className="text-xs uppercase tracking-widest text-[#7A152E] font-bold block mb-2">
              ATELIER PRIVACY &amp; SECURITY PROTOCOLS
            </span>
            <h1 className="font-serif text-3xl sm:text-5xl text-stone-900 font-normal leading-tight">
              Privacy &amp; Policy
            </h1>
            <p className="text-xs sm:text-sm text-stone-600 mt-3 font-light leading-relaxed">
              Last Updated: {new Date().getFullYear()} &bull; Solystra Jewels Private Limited
            </p>
            <p className="text-sm sm:text-base text-stone-700 mt-3 leading-relaxed">
              At Solystra Jewels, we treat your personal privacy with the same uncompromising precision we apply to our fine jewelry craftsmanship. Below are our official commitments regarding data protection, payment encryption, discreet packaging, and your rights as our valued patron.
            </p>
          </div>

        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14 space-y-12">

        {/* ========================================================
            ATELIER TRUST ASSURANCE STRIP (MOVED FROM HOMEPAGE)
            ======================================================== */}
        <section className="bg-white rounded-3xl p-6 sm:p-8 border border-[#EAE4DC] shadow-xs">
          <div className="mb-6">
            <span className="text-[10.5px] uppercase tracking-widest text-[#7A152E] font-bold block mb-1">
              PATRON ASSURANCE &amp; INTEGRITY
            </span>
            <h2 className="font-serif text-xl sm:text-2xl text-stone-900 font-normal">
              Official Craftsmanship &amp; Purchase Guarantees
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6">
            {/* Guarantee 1 */}
            <div className="flex items-center gap-3.5 bg-[#FAF8F5] p-4 rounded-2xl border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-colors shadow-2xs">
              <div className="w-10 h-10 rounded-full bg-[#7A152E]/10 flex items-center justify-center shrink-0 text-[#7A152E]">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs sm:text-sm font-bold text-stone-900">Government BIS Hallmarked</p>
                <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5">Official 925 purity engraved on every piece</p>
              </div>
            </div>

            {/* Guarantee 2 */}
            <div className="flex items-center gap-3.5 bg-[#FAF8F5] p-4 rounded-2xl border border-[#EAE4DC] hover:border-[#C5A059]/60 transition-colors shadow-2xs">
              <div className="w-10 h-10 rounded-full bg-[#C5A059]/15 flex items-center justify-center shrink-0 text-[#C5A059]">
                <Award className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs sm:text-sm font-bold text-stone-900">Austrian Hand-Cut Crystals</p>
                <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5">57-facet diamond brilliance under all lighting</p>
              </div>
            </div>

            {/* Guarantee 3 */}
            <div className="flex items-center gap-3.5 bg-[#FAF8F5] p-4 rounded-2xl border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-colors shadow-2xs">
              <div className="w-10 h-10 rounded-full bg-[#7A152E]/10 flex items-center justify-center shrink-0 text-[#7A152E]">
                <RefreshCw className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs sm:text-sm font-bold text-stone-900">15-Day Hassle-Free Returns</p>
                <p className="text-[11px] sm:text-xs text-stone-500 mt-0.5">Doorstep pickup with full purchase guarantee</p>
              </div>
            </div>
          </div>
        </section>

        {/* Detailed Privacy Policy Articles */}
        <div className="space-y-8">

          {/* Section 1 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-lg sm:text-xl text-stone-900 font-medium mb-3 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                1
              </span>
              <span>Information We Collect &amp; Purpose</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                1.1 When you browse our boutique, acquire fine jewelry, or join the Solystra Club, we collect essential operational information including your full name, shipping/billing address, phone number, and email address solely to process, verify, and deliver your orders.
              </p>
              <p>
                1.2 We do not collect unnecessary personal metrics, and we never collect or process personal data without your explicit knowledge and consent.
              </p>
            </div>
          </div>

          {/* Section 2 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-lg sm:text-xl text-stone-900 font-medium mb-3 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                2
              </span>
              <span>Bank-Grade Payment Security &amp; Zero Card Storage</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                2.1 Solystra Jewels <strong>never stores, caches, or logs your credit/debit card numbers, CVVs, or UPI PINs</strong> on any of our servers.
              </p>
              <p>
                2.2 All payment interactions are routed through RBI-authorized, PCI-DSS Level 1 certified payment processors using 256-bit AES end-to-end encryption.
              </p>
            </div>
          </div>

          {/* Section 3 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-lg sm:text-xl text-stone-900 font-medium mb-3 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                3
              </span>
              <span>Discreet &amp; Secure Packaging Protocol</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                3.1 We recognize that jewelry purchases are often confidential surprises or high-value gifts. All orders are dispatched in plain, tamper-evident, unmarked outer transport cartons without outward jewelry descriptions or price disclosures on the exterior.
              </p>
              <p>
                3.2 High-value parcels require OTP authentication at doorstep handoff to prevent misplacement or unauthorized delivery.
              </p>
            </div>
          </div>

          {/* Section 4 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-lg sm:text-xl text-stone-900 font-medium mb-3 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                4
              </span>
              <span>No-Spam Policy &amp; Third-Party Non-Disclosure</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                4.1 Solystra strictly maintains an <strong>anti-monetization data policy</strong>. We never sell, rent, monetize, or disclose your contact details to third-party marketing brokers or advertising networks.
              </p>
              <p>
                4.2 You may opt out of atelier preview newsletters at any time with a single click in any email or by notifying our concierge.
              </p>
            </div>
          </div>

          {/* Section 5 */}
          <div className="bg-white rounded-2xl p-6 sm:p-8 border border-[#EAE4DC]">
            <h3 className="font-serif text-lg sm:text-xl text-stone-900 font-medium mb-3 flex items-center gap-3">
              <span className="w-7 h-7 rounded-full bg-[#7A152E]/10 text-[#7A152E] text-xs font-bold flex items-center justify-center">
                5
              </span>
              <span>Your Data Rights &amp; Information Access</span>
            </h3>
            <div className="space-y-3 text-xs sm:text-sm text-stone-600 leading-relaxed font-light">
              <p>
                5.1 You have the absolute right to inspect the personal data we maintain associated with your account, correct discrepancies, or request the permanent deletion of your profile and historical records upon order completion.
              </p>
              <p>
                5.2 To request data inspection or account purging, contact our Data Protection Officer at <strong>care@solystrajewels.com</strong>. Requests are executed within 48 business hours.
              </p>
            </div>
          </div>

        </div>

        {/* Atelier Concierge Contact Banner */}
        <div className="rounded-3xl p-8 bg-gradient-to-r from-[#7A152E] to-[#4A0D1C] text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl">
          <div>
            <span className="text-xs text-[#F5E6CC] font-bold uppercase tracking-widest block mb-1">
              PRIVACY OR COMPLIANCE INQUIRIES?
            </span>
            <h3 className="font-serif text-2xl sm:text-3xl font-normal">
              Solystra Atelier Concierge
            </h3>
            <p className="text-xs sm:text-sm text-stone-200 mt-1 max-w-xl font-light">
              Our trust and security desk is available Monday through Saturday to answer questions regarding our privacy practices, hallmarking, or order confidentiality.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <a
              href="mailto:solystrajewels.official@gmail.com"
              className="px-5 py-2.5 rounded-xl bg-white text-[#7A152E] text-xs font-bold hover:bg-stone-100 transition-colors shadow-sm inline-flex items-center gap-2"
            >
              <Mail className="w-4 h-4" />
              <span>Email Privacy Desk</span>
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
