import React, { useState, useEffect, useMemo } from 'react';
import { useShop } from '../context/ShopContext';
import {
  ShieldCheck,
  Lock,
  ArrowLeft,
  CheckCircle2,
  Truck,
  CreditCard,
  QrCode,
  Building2,
  Banknote,
  Tag,
  ChevronDown,
  ChevronUp,
  Download,
  ExternalLink,
  Package,
  Award,
  Clock,
  Phone,
  Mail,
  MapPin,
  Check,
  AlertCircle
} from 'lucide-react';

const PINCODE_MAP = {
  '400001': { city: 'Mumbai', state: 'Maharashtra', hub: 'Mumbai Central Air Hub' },
  '400050': { city: 'Mumbai (Bandra)', state: 'Maharashtra', hub: 'Bandra Flagship Hub' },
  '110001': { city: 'New Delhi', state: 'Delhi', hub: 'Connaught Place Hub' },
  '560001': { city: 'Bengaluru', state: 'Karnataka', hub: 'Indiranagar Hub' },
  '500001': { city: 'Hyderabad', state: 'Telangana', hub: 'Banjara Hills Hub' },
  '302001': { city: 'Jaipur', state: 'Rajasthan', hub: 'Jaipur Bench Atelier' },
  '600001': { city: 'Chennai', state: 'Tamil Nadu', hub: 'Chennai Air Cargo Hub' },
  '700001': { city: 'Kolkata', state: 'West Bengal', hub: 'Kolkata Central Hub' },
  '380001': { city: 'Ahmedabad', state: 'Gujarat', hub: 'Ahmedabad Express Hub' },
  '411001': { city: 'Pune', state: 'Maharashtra', hub: 'Pune Deccan Hub' }
};

export const CheckoutPage = ({ onBackToStore }) => {
  const {
    cart,
    cartSubtotal,
    cartMrpTotal,
    totalSavings,
    discountAmount,
    appliedCoupon,
    shippingFee,
    cartTotal,
    applyCoupon,
    removeCoupon,
    clearCart,
    showToast,
    lastOrder,
    setLastOrder,
    isGiftPackagingAdded,
    setIsGiftPackagingAdded
  } = useShop();

  // Multi-step checkout states: 1 = Address, 2 = Payment, 3 = Confirmation
  const [currentStep, setCurrentStep] = useState(1);
  const [isMobileSummaryOpen, setIsMobileSummaryOpen] = useState(false);

  // Address form
  const [formData, setFormData] = useState({
    email: 'vrund.solystra@gmail.com',
    phone: '9876543210',
    firstName: 'Vrund',
    lastName: 'Shah',
    address: 'Boutique Residence 402, High Street',
    locality: 'Heritage Enclave',
    pincode: '400001',
    city: 'Mumbai',
    state: 'Maharashtra',
    deliveryMethod: 'bluedart_express', // 'bluedart_express' or 'same_day_whiteglove'
    discretePackaging: true
  });

  const [formErrors, setFormErrors] = useState({});

  // Payment method: 'upi', 'card', 'netbanking', 'cod'
  const [paymentMethod, setPaymentMethod] = useState('upi');

  // UPI State
  const [upiApp, setUpiApp] = useState('gpay');
  const [upiId, setUpiId] = useState('');
  const [upiTimer, setUpiTimer] = useState(600); // 10 minutes countdown

  // Card State
  const [cardData, setCardData] = useState({
    number: '',
    name: 'VRUND SHAH',
    expiry: '09/29',
    cvv: '925',
    saveCard: true
  });

  // Netbanking State
  const [selectedBank, setSelectedBank] = useState('HDFC');

  // COD State
  const [codOtpSent, setCodOtpSent] = useState(false);
  const [codOtp, setCodOtp] = useState('');
  const [codVerified, setCodVerified] = useState(false);

  // Processing Overlay Simulation
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStepText, setProcessingStepText] = useState('');

  // Promo Code input inside Checkout
  const [couponCodeInput, setCouponCodeInput] = useState('');

  // Track BlueDart modal in Confirmation
  const [showBlueDartTracking, setShowBlueDartTracking] = useState(false);

  // Auto detect city/state on pincode change
  useEffect(() => {
    if (formData.pincode.length === 6) {
      if (PINCODE_MAP[formData.pincode]) {
        const match = PINCODE_MAP[formData.pincode];
        setFormData(prev => ({ ...prev, city: match.city, state: match.state }));
        showToast(`PIN Code verified for ${match.city}, ${match.state}`);
      } else {
        // Generic fallback for any valid 6-digit PIN
        setFormData(prev => ({
          ...prev,
          city: prev.city || 'Metro City',
          state: prev.state || 'India'
        }));
      }
    }
  }, [formData.pincode]);

  // UPI Countdown timer
  useEffect(() => {
    if (currentStep === 2 && paymentMethod === 'upi') {
      const interval = setInterval(() => {
        setUpiTimer(prev => (prev > 0 ? prev - 1 : 600));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [currentStep, paymentMethod]);

  const formattedUpiTime = useMemo(() => {
    const mins = Math.floor(upiTimer / 60);
    const secs = upiTimer % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }, [upiTimer]);

  // Card Brand Detection
  const cardBrand = useMemo(() => {
    const clean = cardData.number.replace(/\s+/g, '');
    if (clean.startsWith('4')) return 'Visa';
    if (clean.startsWith('5')) return 'MasterCard';
    if (clean.startsWith('60') || clean.startsWith('65') || clean.startsWith('81') || clean.startsWith('82')) return 'RuPay';
    if (clean.startsWith('34') || clean.startsWith('37')) return 'Amex';
    return 'Card';
  }, [cardData.number]);

  const handleCardNumberChange = (e) => {
    let val = e.target.value.replace(/\D/g, '').slice(0, 16);
    val = val.replace(/(.{4})/g, '$1 ').trim();
    setCardData(prev => ({ ...prev, number: val }));
  };

  const handleExpiryChange = (e) => {
    let val = e.target.value.replace(/\D/g, '').slice(0, 4);
    if (val.length >= 2) {
      val = `${val.slice(0, 2)}/${val.slice(2)}`;
    }
    setCardData(prev => ({ ...prev, expiry: val }));
  };

  const handlePrefillDemoCard = () => {
    setCardData({
      number: '4532 8921 5400 9250',
      name: 'VRUND SHAH',
      expiry: '11/29',
      cvv: '925',
      saveCard: true
    });
    showToast('Demo Visa Platinum card prefilled');
  };

  // Address validation
  const validateAddressStep = () => {
    const errors = {};
    if (!formData.firstName.trim()) errors.firstName = 'First name is required';
    if (!formData.lastName.trim()) errors.lastName = 'Last name is required';
    if (!formData.email.trim() || !formData.email.includes('@')) errors.email = 'Valid email is required';
    if (!formData.phone.trim() || formData.phone.length < 10) errors.phone = 'Valid 10-digit mobile number is required';
    if (!formData.address.trim()) errors.address = 'Street address is required';
    if (!formData.pincode.trim() || formData.pincode.length !== 6) errors.pincode = '6-digit PIN code is required';

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleProceedToPayment = (e) => {
    e.preventDefault();
    if (validateAddressStep()) {
      setCurrentStep(2);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      showToast('Please fill all required delivery details', 'info');
    }
  };

  const handleApplyCoupon = (e) => {
    e.preventDefault();
    if (couponCodeInput) {
      applyCoupon(couponCodeInput);
      setCouponCodeInput('');
    }
  };

  // Process and finalize payment
  const handleCompleteOrder = () => {
    setIsProcessing(true);
    setProcessingStepText('Authorizing 256-Bit Payment Gateway...');

    setTimeout(() => {
      setProcessingStepText('Allocating Certified BIS 925 Hallmark Vault Piece...');
    }, 800);

    setTimeout(() => {
      setProcessingStepText('Generating BlueDart Insured Air Consignment...');
    }, 1400);

    setTimeout(() => {
      const generatedOrder = {
        orderId: `SLY-2026-${Math.floor(10000 + Math.random() * 90000)}`,
        date: new Date().toLocaleDateString('en-IN', {
          day: 'numeric',
          month: 'short',
          year: 'numeric'
        }),
        estimatedDelivery: new Date(Date.now() + 3 * 86400000).toLocaleDateString('en-IN', {
          weekday: 'long',
          day: 'numeric',
          month: 'short'
        }),
        waybillNumber: `BD-AIR-${Math.floor(100000000 + Math.random() * 900000000)}`,
        items: [...cart],
        subtotal: cartSubtotal,
        discount: discountAmount,
        coupon: appliedCoupon?.code,
        shippingFee: shippingFee,
        total: cartTotal,
        customer: { ...formData },
        paymentMethod: paymentMethod === 'upi' ? `UPI (${upiApp.toUpperCase()})` : paymentMethod === 'card' ? `${cardBrand} Ending •••• ${cardData.number.slice(-4) || '9250'}` : paymentMethod === 'netbanking' ? `NetBanking (${selectedBank})` : 'Cash on Delivery (Verified)'
      };

      setLastOrder(generatedOrder);
      setIsProcessing(false);
      setCurrentStep(3);
      clearCart();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 2200);
  };

  // Mock Tax Invoice Download
  const handleDownloadInvoice = () => {
    const invoiceContent = `=====================================================
          SOLYSTRA ATELIER JEWELS - OFFICIAL TAX INVOICE
=====================================================
Order Ref: ${lastOrder?.orderId || 'SLY-2026-94821'}
Date: ${lastOrder?.date || '15 Sep 2026'}
GSTIN: 27AABCS9821Q1Z4  |  HSN Code: 7113 (Silver Jewellery)
BIS Assay Registration: BIS-JAIPUR-MUMBAI-925

BILL TO & DELIVER TO:
${lastOrder?.customer?.firstName} ${lastOrder?.customer?.lastName}
${lastOrder?.customer?.address}, ${lastOrder?.customer?.locality}
${lastOrder?.customer?.city}, ${lastOrder?.customer?.state} - ${lastOrder?.customer?.pincode}
Phone: +91 ${lastOrder?.customer?.phone}

ITEMIZED CONSIGNMENT:
${lastOrder?.items?.map((item, idx) => `${idx + 1}. ${item.name} (${item.metal}) x${item.quantity} - INR ${(item.price * item.quantity).toLocaleString('en-IN')}`).join('\n')}

Subtotal: INR ${lastOrder?.subtotal?.toLocaleString('en-IN')}
Discount: -INR ${lastOrder?.discount?.toLocaleString('en-IN')}
BlueDart Express Insured Air: FREE (Complimentary)
TOTAL PAID: INR ${lastOrder?.total?.toLocaleString('en-IN')} (Inclusive of 3% GST)

Payment Mode: ${lastOrder?.paymentMethod}
Status: Confirmed & Hallmarked
=====================================================`;

    const blob = new Blob([invoiceContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Invoice_${lastOrder?.orderId || 'Solystra'}.txt`;
    a.click();
    showToast('Tax invoice downloaded successfully!');
  };

  // If cart is empty and not on confirmation step
  if (cart.length === 0 && currentStep !== 3) {
    return (
      <div className="min-h-[70vh] bg-[#FAF8F5] flex items-center justify-center p-6 text-center font-sans">
        <div className="max-w-md bg-white p-8 rounded-3xl border border-[#EAE4DC] shadow-xl">
          <div className="w-16 h-16 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] mx-auto mb-4">
            <Package className="w-8 h-8" />
          </div>
          <h2 className="font-serif text-2xl text-stone-900 font-normal">
            Your Shopping Bag is Empty
          </h2>
          <p className="text-xs text-stone-500 mt-2 leading-relaxed">
            Please add your favorite certified 925 sterling silver or 18K gold vermeil pieces before proceeding to checkout.
          </p>
          <button
            onClick={() => {
              if (onBackToStore) onBackToStore();
              else window.location.hash = '#/';
            }}
            className="mt-6 px-8 py-3.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold uppercase tracking-wider rounded-xl shadow-md transition-all cursor-pointer"
          >
            Explore Atelier Catalog
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#FAF8F5] min-h-screen text-[#231F20] font-sans pb-20">
      
      {/* ========================================================
          CHECKOUT LUXURY HEADER
          ======================================================== */}
      <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-[#EAE4DC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 sm:h-20 flex items-center justify-between">
          
          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (currentStep === 2) setCurrentStep(1);
                else if (onBackToStore) onBackToStore();
                else window.location.hash = '#/';
              }}
              className="p-2 rounded-xl hover:bg-stone-100 text-stone-600 transition-colors cursor-pointer flex items-center gap-1.5 text-xs font-medium"
            >
              <ArrowLeft className="w-4 h-4" />
              <span className="hidden sm:inline">Back</span>
            </button>

            <a href="#/" className="flex items-center gap-2.5">
              <img
                src="solystra_assets/solystra_logo.png"
                alt="Solystra Jewels"
                className="h-7 sm:h-9 w-auto object-contain"
              />
              <span className="text-[10px] uppercase tracking-widest text-[#C5A059] font-sans font-bold border-l border-stone-300 pl-2.5 hidden sm:inline">
                Secure Checkout
              </span>
            </a>
          </div>

          {/* Stepper Progress Indicator */}
          <div className="hidden md:flex items-center gap-3 text-xs">
            <div className={`flex items-center gap-1.5 ${currentStep >= 1 ? 'text-[#7A152E] font-bold' : 'text-stone-400'}`}>
              <span className="w-5 h-5 rounded-full bg-[#7A152E] text-white text-[10px] flex items-center justify-center">1</span>
              <span>Delivery</span>
            </div>
            <span className="text-stone-300">&bull;&bull;&bull;</span>
            <div className={`flex items-center gap-1.5 ${currentStep >= 2 ? 'text-[#7A152E] font-bold' : 'text-stone-400'}`}>
              <span className={`w-5 h-5 rounded-full text-[10px] flex items-center justify-center ${currentStep >= 2 ? 'bg-[#7A152E] text-white' : 'bg-stone-200 text-stone-600'}`}>2</span>
              <span>Payment</span>
            </div>
            <span className="text-stone-300">&bull;&bull;&bull;</span>
            <div className={`flex items-center gap-1.5 ${currentStep === 3 ? 'text-[#7A152E] font-bold' : 'text-stone-400'}`}>
              <span className={`w-5 h-5 rounded-full text-[10px] flex items-center justify-center ${currentStep === 3 ? 'bg-[#7A152E] text-white' : 'bg-stone-200 text-stone-600'}`}>3</span>
              <span>Confirmation</span>
            </div>
          </div>

          {/* Understated Luxury Security Indicator */}
          <div className="flex items-center gap-2 text-[11px] font-medium text-stone-700 bg-stone-100/90 border border-[#EAE4DC] px-3.5 py-1.5 rounded-full shadow-2xs">
            <Lock className="w-3.5 h-3.5 text-[#C5A059]" />
            <span className="tracking-wide text-[11px] uppercase font-semibold text-stone-800">256-Bit Encrypted</span>
            <span className="text-stone-300">&bull;</span>
            <span className="text-stone-500 font-sans text-[10.5px]">RBI Compliant</span>
          </div>

        </div>
      </header>

      {/* ========================================================
          MOBILE ACCORDION ORDER SUMMARY (COLLAPSIBLE)
          ======================================================== */}
      {currentStep !== 3 && (
        <div className="lg:hidden bg-white border-b border-[#EAE4DC] px-4 py-3">
          <button
            onClick={() => setIsMobileSummaryOpen(prev => !prev)}
            className="w-full flex items-center justify-between text-xs text-stone-800 font-medium"
          >
            <div className="flex items-center gap-2">
              <span className="text-[#7A152E] font-bold">
                {isMobileSummaryOpen ? 'Hide Order Summary' : 'Show Order Summary'}
              </span>
              {isMobileSummaryOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </div>
            <span className="font-serif text-sm font-bold text-[#7A152E]">
              ₹{cartTotal.toLocaleString('en-IN')}
            </span>
          </button>

          {isMobileSummaryOpen && (
            <div className="pt-4 border-t border-stone-100 mt-3 space-y-3">
              {cart.map(item => (
                <div key={item.variantKey} className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-lg overflow-hidden border border-stone-200 shrink-0 bg-stone-50">
                    <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                  </div>
                  <div className="flex-1 min-w-0 text-xs">
                    <div className="font-medium text-stone-900 truncate">{item.name}</div>
                    <div className="text-[11px] text-stone-500">{item.metal} &bull; Qty: {item.quantity}</div>
                  </div>
                  <div className="font-bold text-xs text-stone-900">
                    ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ========================================================
          MAIN CHECKOUT CONTENT CONTAINER
          ======================================================== */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 sm:pt-10">
        
        {/* STEP 3: ORDER SUCCESS CONFIRMATION SCREEN WITH CELEBRATION ANIMATIONS */}
        {currentStep === 3 && lastOrder ? (
          <div className="max-w-3xl mx-auto bg-white rounded-3xl border border-[#EAE4DC] shadow-2xl overflow-hidden animate-fadeIn relative">
            
            {/* Celebratory Confetti Shower */}
            <div className="absolute inset-x-0 top-0 h-96 overflow-hidden pointer-events-none z-20">
              {[
                { left: '5%', delay: '0.1s', bg: '#C5A059', size: 'w-2.5 h-3.5', rotate: 'rotate-12' },
                { left: '12%', delay: '0.5s', bg: '#7A152E', size: 'w-3 h-2', rotate: '-rotate-45' },
                { left: '19%', delay: '0.2s', bg: '#C5A059', size: 'w-2.5 h-2.5 rounded-full', rotate: 'rotate-0' },
                { left: '27%', delay: '0.7s', bg: '#CBD5E1', size: 'w-2 h-3', rotate: 'rotate-45' },
                { left: '34%', delay: '0.3s', bg: '#C5A059', size: 'w-3 h-2', rotate: 'rotate-12' },
                { left: '42%', delay: '0.9s', bg: '#E89895', size: 'w-2 h-2.5', rotate: '-rotate-12' },
                { left: '49%', delay: '0.15s', bg: '#C5A059', size: 'w-2.5 h-2.5 rounded-full', rotate: 'rotate-0' },
                { left: '56%', delay: '0.6s', bg: '#7A152E', size: 'w-3 h-2', rotate: 'rotate-30' },
                { left: '64%', delay: '0.35s', bg: '#C5A059', size: 'w-2 h-3', rotate: '-rotate-30' },
                { left: '72%', delay: '0.8s', bg: '#CBD5E1', size: 'w-2.5 h-2.5 rounded-full', rotate: 'rotate-12' },
                { left: '79%', delay: '0.25s', bg: '#FFFFFF', size: 'w-2 h-3', rotate: 'rotate-45' },
                { left: '86%', delay: '0.65s', bg: '#E89895', size: 'w-3 h-2', rotate: '-rotate-45' },
                { left: '93%', delay: '0.4s', bg: '#C5A059', size: 'w-2.5 h-3', rotate: 'rotate-12' },
                { left: '8%', delay: '1.2s', bg: '#C5A059', size: 'w-2 h-2.5', rotate: 'rotate-30' },
                { left: '23%', delay: '1.4s', bg: '#7A152E', size: 'w-2.5 h-2.5 rounded-full', rotate: 'rotate-0' },
                { left: '39%', delay: '1.1s', bg: '#C5A059', size: 'w-3 h-2', rotate: '-rotate-12' },
                { left: '53%', delay: '1.5s', bg: '#CBD5E1', size: 'w-2 h-3', rotate: 'rotate-45' },
                { left: '68%', delay: '1.3s', bg: '#C5A059', size: 'w-2.5 h-2.5 rounded-full', rotate: 'rotate-0' },
                { left: '83%', delay: '1.6s', bg: '#E89895', size: 'w-3 h-2', rotate: 'rotate-12' },
                { left: '96%', delay: '1.25s', bg: '#7A152E', size: 'w-2 h-3', rotate: '-rotate-30' }
              ].map((conf, idx) => (
                <div
                  key={idx}
                  className={`confetti-piece ${conf.size} ${conf.rotate}`}
                  style={{
                    left: conf.left,
                    backgroundColor: conf.bg,
                    animationDelay: conf.delay
                  }}
                />
              ))}
            </div>

            {/* Celebratory Banner */}
            <div className="bg-gradient-to-r from-[#7A152E] via-[#590D1E] to-[#380A15] p-8 sm:p-12 text-white text-center relative overflow-hidden">
              <div className="absolute top-0 right-0 -mr-10 -mt-10 w-48 h-48 rounded-full bg-white/5 pointer-events-none" />
              
              {/* Pulsing halo and animated SVG drawing checkmark */}
              <div className="relative mx-auto mb-5 w-20 h-20 flex items-center justify-center">
                <div className="absolute inset-0 rounded-full bg-[#C5A059]/25 celebration-halo" />
                <div className="relative w-16 h-16 rounded-full bg-gradient-to-tr from-[#590D1E] to-[#8B1E3F] border-2 border-white/80 flex items-center justify-center shadow-xl">
                  <svg
                    className="w-9 h-9 text-white"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polyline points="20 6 9 17 4 12" className="animate-draw-check" />
                  </svg>
                </div>
              </div>

              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#590D1E]/80 backdrop-blur-md border border-white/30 mb-3">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-[10.5px] uppercase tracking-widest text-white font-bold">
                  PAYMENT CONFIRMED &amp; SEALED
                </span>
              </div>

              <h1 className="font-serif text-3xl sm:text-5xl font-normal text-white tracking-tight">
                Thank You, {lastOrder.customer.firstName}!
              </h1>
              <p className="text-xs sm:text-sm text-stone-200 mt-2 max-w-md mx-auto font-light leading-relaxed">
                Your heirloom jewellery has been assigned to our master bench artisans. An official invoice and tracking link have been dispatched to <strong>{lastOrder.customer.email}</strong>.
              </p>

              <div className="inline-flex items-center gap-2 mt-4 px-3.5 py-1.5 rounded-full bg-[#590D1E]/80 backdrop-blur-md border border-white/20 text-xs font-mono text-stone-200">
                <span>Order Ref: {lastOrder.orderId}</span>
              </div>
            </div>

            <div className="p-6 sm:p-10 space-y-8">
              
              {/* BlueDart Real-time Air Tracking Progress */}
              <div className="p-6 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC]">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-[#EAE4DC] gap-2">
                  <div>
                    <div className="text-[10px] text-stone-500 uppercase font-bold tracking-wider">
                      BlueDart Insured Air Consignment
                    </div>
                    <div className="text-sm font-bold text-stone-900 font-mono mt-0.5">
                      Waybill: {lastOrder.waybillNumber}
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-xs text-stone-500">Estimated Delivery:</span>
                    <div className="font-bold text-xs sm:text-sm text-[#7A152E]">
                      {lastOrder.estimatedDelivery} (By 7:00 PM)
                    </div>
                  </div>
                </div>

                {/* Tracking Progress Steps */}
                <div className="grid grid-cols-4 gap-2 pt-6 text-center text-[10px] sm:text-xs">
                  <div className="flex flex-col items-center">
                    <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold mb-2 shadow-xs">
                      ✓
                    </div>
                    <span className="font-bold text-stone-900">Confirmed</span>
                    <span className="text-[10px] text-stone-400">Paid & Assayed</span>
                  </div>

                  <div className="flex flex-col items-center">
                    <div className="w-8 h-8 rounded-full bg-[#7A152E] text-white flex items-center justify-center font-bold mb-2 animate-pulse">
                      2
                    </div>
                    <span className="font-bold text-stone-900">Hallmark Assay</span>
                    <span className="text-[10px] text-stone-400">Ultrasonic Spa</span>
                  </div>

                  <div className="flex flex-col items-center opacity-60">
                    <div className="w-8 h-8 rounded-full bg-stone-200 text-stone-600 flex items-center justify-center font-bold mb-2">
                      3
                    </div>
                    <span className="font-bold text-stone-800">Air Express</span>
                    <span className="text-[10px] text-stone-400">BlueDart Courier</span>
                  </div>

                  <div className="flex flex-col items-center opacity-60">
                    <div className="w-8 h-8 rounded-full bg-stone-200 text-stone-600 flex items-center justify-center font-bold mb-2">
                      4
                    </div>
                    <span className="font-bold text-stone-800">Delivered</span>
                    <span className="text-[10px] text-stone-400">Doorstep Handover</span>
                  </div>
                </div>
              </div>

              {/* Order Details & Address Summary */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-xs">
                <div className="p-5 rounded-2xl bg-white border border-[#EAE4DC] space-y-2">
                  <div className="text-[10.5px] uppercase font-bold text-[#7A152E] tracking-wider">
                    Shipping Address
                  </div>
                  <div className="font-bold text-stone-900 text-sm">
                    {lastOrder.customer.firstName} {lastOrder.customer.lastName}
                  </div>
                  <div className="text-stone-600 leading-relaxed">
                    {lastOrder.customer.address}, {lastOrder.customer.locality}<br />
                    {lastOrder.customer.city}, {lastOrder.customer.state} - {lastOrder.customer.pincode}
                  </div>
                  <div className="text-stone-500 pt-1">
                    Phone: +91 {lastOrder.customer.phone}
                  </div>
                </div>

                <div className="p-5 rounded-2xl bg-white border border-[#EAE4DC] space-y-2">
                  <div className="text-[10.5px] uppercase font-bold text-[#7A152E] tracking-wider">
                    Payment & Guarantees
                  </div>
                  <div className="font-bold text-stone-900 text-sm">
                    {lastOrder.paymentMethod}
                  </div>
                  <div className="text-stone-600 leading-relaxed">
                    Amount Paid: <strong className="text-stone-900">₹{lastOrder.total.toLocaleString('en-IN')}</strong><br />
                    BIS 925 Hallmark Certificate: <span className="text-emerald-700 font-semibold">Included in Vault</span>
                  </div>
                  <div className="inline-flex items-center gap-1.5 text-stone-500 pt-1 text-[11px]">
                    <ShieldCheck className="w-4 h-4 text-[#C5A059]" />
                    <span>1-Year Atelier Plating Warranty</span>
                  </div>
                </div>
              </div>

              {/* Items Breakdown */}
              <div className="border border-[#EAE4DC] rounded-2xl overflow-hidden">
                <div className="bg-[#FAF8F5] px-5 py-3 border-b border-[#EAE4DC] text-xs font-bold text-stone-800">
                  Consignment Pieces ({lastOrder.items.length})
                </div>
                <div className="divide-y divide-[#EAE4DC] p-2">
                  {lastOrder.items.map((item) => (
                    <div key={item.variantKey} className="p-3 flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <img src={item.image} alt={item.name} className="w-12 h-12 rounded-lg object-cover border border-stone-200 bg-stone-50" />
                        <div>
                          <div className="font-medium text-xs text-stone-900">{item.name}</div>
                          <div className="text-[11px] text-stone-500">{item.metal} &bull; Qty {item.quantity}</div>
                        </div>
                      </div>
                      <div className="font-bold text-xs text-stone-900">
                        ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3 pt-2">
                <button
                  onClick={handleDownloadInvoice}
                  className="flex-1 py-3.5 px-4 rounded-xl border border-stone-300 hover:border-[#7A152E] bg-white hover:bg-stone-50 text-stone-800 text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer shadow-xs"
                >
                  <Download className="w-4 h-4 text-[#7A152E]" />
                  <span>Download Tax Invoice (Mock PDF)</span>
                </button>

                <button
                  onClick={() => setShowBlueDartTracking(true)}
                  className="flex-1 py-3.5 px-4 rounded-xl border border-stone-300 hover:border-[#7A152E] bg-white hover:bg-stone-50 text-stone-800 text-xs font-semibold flex items-center justify-center gap-2 transition-all cursor-pointer shadow-xs"
                >
                  <Truck className="w-4 h-4 text-[#C5A059]" />
                  <span>Track Consignment on BlueDart</span>
                </button>
              </div>

              <div className="pt-2 text-center">
                <button
                  onClick={() => {
                    setCurrentStep(1);
                    if (onBackToStore) onBackToStore();
                    else window.location.hash = '#/';
                  }}
                  className="px-8 py-3.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs uppercase tracking-widest font-semibold rounded-xl shadow-lg transition-all cursor-pointer"
                >
                  Continue Shopping Atelier
                </button>
              </div>

            </div>
          </div>
        ) : (
          /* STEP 1 & 2: CHECKOUT MAIN 2-COLUMN VIEW */
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
            
            {/* LEFT COLUMN: INTERACTIVE FORM & GATEWAY (7 COLS) */}
            <div className="lg:col-span-7 space-y-8">
              
              {/* STEP 1: CONTACT & DELIVERY ADDRESS */}
              <div className={`bg-white rounded-3xl border border-[#EAE4DC] p-6 sm:p-8 shadow-md transition-all ${currentStep === 1 ? 'ring-2 ring-[#7A152E]/10' : 'opacity-80'}`}>
                
                <div className="flex items-center justify-between pb-6 border-b border-[#EAE4DC]">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-[#7A152E] text-white text-xs font-bold flex items-center justify-center">
                      1
                    </div>
                    <div>
                      <h2 className="font-serif text-lg sm:text-xl font-normal text-stone-900">
                        Contact & Delivery Address
                      </h2>
                      <p className="text-xs text-stone-500 mt-0.5">
                        Shipped via BlueDart Insured Air Express with BIS Hallmark Certification.
                      </p>
                    </div>
                  </div>

                  {currentStep === 2 && (
                    <button
                      onClick={() => setCurrentStep(1)}
                      className="text-xs font-bold text-[#7A152E] hover:underline cursor-pointer"
                    >
                      Edit
                    </button>
                  )}
                </div>

                {currentStep === 1 ? (
                  <form onSubmit={handleProceedToPayment} className="mt-6 space-y-4 text-xs">
                    
                    {/* Contact details */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">
                          Email Address <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <input
                            type="email"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            placeholder="your.email@example.com"
                            className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50"
                          />
                          <Mail className="w-4 h-4 text-stone-400 absolute right-3 top-3" />
                        </div>
                        {formErrors.email && <span className="text-[11px] text-red-500">{formErrors.email}</span>}
                      </div>

                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">
                          Mobile Number <span className="text-red-500">*</span>
                        </label>
                        <div className="relative flex">
                          <span className="inline-flex items-center px-3 rounded-l-xl border border-r-0 border-stone-200 bg-stone-100 text-stone-600 font-mono text-xs">
                            +91
                          </span>
                          <input
                            type="tel"
                            maxLength={10}
                            value={formData.phone}
                            onChange={(e) => setFormData({ ...formData, phone: e.target.value.replace(/\D/g, '') })}
                            placeholder="98765 43210"
                            className="w-full px-3.5 py-2.5 rounded-r-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50 font-mono"
                          />
                        </div>
                        {formErrors.phone && <span className="text-[11px] text-red-500">{formErrors.phone}</span>}
                      </div>
                    </div>

                    {/* Name */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">
                          First Name <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          value={formData.firstName}
                          onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                          placeholder="First Name"
                          className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50"
                        />
                        {formErrors.firstName && <span className="text-[11px] text-red-500">{formErrors.firstName}</span>}
                      </div>

                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">
                          Last Name <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          value={formData.lastName}
                          onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                          placeholder="Last Name"
                          className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50"
                        />
                        {formErrors.lastName && <span className="text-[11px] text-red-500">{formErrors.lastName}</span>}
                      </div>
                    </div>

                    {/* Street Address */}
                    <div>
                      <label className="block text-stone-700 font-semibold mb-1">
                        Flat / House No. & Building Name <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={formData.address}
                        onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                        placeholder="Apartment, Studio, Floor, Building"
                        className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50"
                      />
                      {formErrors.address && <span className="text-[11px] text-red-500">{formErrors.address}</span>}
                    </div>

                    <div>
                      <label className="block text-stone-700 font-semibold mb-1">
                        Street, Area & Landmark
                      </label>
                      <input
                        type="text"
                        value={formData.locality}
                        onChange={(e) => setFormData({ ...formData, locality: e.target.value })}
                        placeholder="Near Landmark / Road"
                        className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50"
                      />
                    </div>

                    {/* PIN code, City & State with Auto-Detection */}
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">
                          PIN Code (6-Digits) <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="text"
                          maxLength={6}
                          value={formData.pincode}
                          onChange={(e) => setFormData({ ...formData, pincode: e.target.value.replace(/\D/g, '') })}
                          placeholder="e.g. 400001"
                          className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 focus:border-[#7A152E] focus:outline-none bg-stone-50/50 font-mono font-bold text-stone-900"
                        />
                        {formErrors.pincode && <span className="text-[11px] text-red-500">{formErrors.pincode}</span>}
                      </div>

                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">City</label>
                        <input
                          type="text"
                          value={formData.city}
                          onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                          placeholder="City"
                          className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-stone-100 text-stone-800"
                        />
                      </div>

                      <div>
                        <label className="block text-stone-700 font-semibold mb-1">State</label>
                        <input
                          type="text"
                          value={formData.state}
                          onChange={(e) => setFormData({ ...formData, state: e.target.value })}
                          placeholder="State"
                          className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-stone-100 text-stone-800"
                        />
                      </div>
                    </div>

                    {/* Delivery Method Selection */}
                    <div className="pt-2">
                      <label className="block text-stone-800 font-bold mb-2">
                        Select Delivery Speed
                      </label>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <label
                          className={`p-3.5 rounded-xl border cursor-pointer flex items-center justify-between transition-all ${
                            formData.deliveryMethod === 'bluedart_express'
                              ? 'border-[#7A152E] bg-[#FAF8F5] ring-1 ring-[#7A152E]'
                              : 'border-stone-200 bg-white hover:border-stone-300'
                          }`}
                        >
                          <div className="flex items-center gap-2.5">
                            <input
                              type="radio"
                              name="deliveryMethod"
                              checked={formData.deliveryMethod === 'bluedart_express'}
                              onChange={() => setFormData({ ...formData, deliveryMethod: 'bluedart_express' })}
                              className="text-[#7A152E] focus:ring-[#7A152E]"
                            />
                            <div>
                              <div className="font-bold text-stone-900">BlueDart Air Express</div>
                              <div className="text-[11px] text-stone-500">2-3 Business Days &bull; Insured</div>
                            </div>
                          </div>
                          <span className="font-bold text-emerald-700 text-xs">FREE</span>
                        </label>

                        <label
                          className={`p-3.5 rounded-xl border cursor-pointer flex items-center justify-between transition-all ${
                            formData.deliveryMethod === 'same_day_whiteglove'
                              ? 'border-[#7A152E] bg-[#FAF8F5] ring-1 ring-[#7A152E]'
                              : 'border-stone-200 bg-white hover:border-stone-300'
                          }`}
                        >
                          <div className="flex items-center gap-2.5">
                            <input
                              type="radio"
                              name="deliveryMethod"
                              checked={formData.deliveryMethod === 'same_day_whiteglove'}
                              onChange={() => setFormData({ ...formData, deliveryMethod: 'same_day_whiteglove' })}
                              className="text-[#7A152E] focus:ring-[#7A152E]"
                            />
                            <div>
                              <div className="font-bold text-stone-900">White-Glove Courier</div>
                              <div className="text-[11px] text-stone-500">Next-Day Priority Handover</div>
                            </div>
                          </div>
                          <span className="font-bold text-stone-900 text-xs">₹199</span>
                        </label>
                      </div>
                    </div>

                    {/* Discrete Packaging Checkbox */}
                    <label className="flex items-center gap-2 pt-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.discretePackaging}
                        onChange={(e) => setFormData({ ...formData, discretePackaging: e.target.checked })}
                        className="rounded text-[#7A152E] focus:ring-[#7A152E]"
                      />
                      <span className="text-[11px] text-stone-600">
                        Deliver in unbranded, tamper-proof outer packaging for discreet gifting surprises.
                      </span>
                    </label>

                    {/* Continue Button */}
                    <div className="pt-4">
                      <button
                        type="submit"
                        className="w-full py-3.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs sm:text-sm font-semibold uppercase tracking-wider rounded-xl shadow-lg transition-all cursor-pointer flex items-center justify-center gap-2"
                      >
                        <span>Continue to Payment Method</span>
                        <ArrowLeft className="w-4 h-4 rotate-180" />
                      </button>
                    </div>

                  </form>
                ) : (
                  <div className="mt-4 p-4 rounded-xl bg-stone-50 border border-stone-200 text-xs space-y-1">
                    <div className="font-bold text-stone-900">
                      {formData.firstName} {formData.lastName} (+91 {formData.phone})
                    </div>
                    <div className="text-stone-600">
                      {formData.address}, {formData.locality}, {formData.city}, {formData.state} - {formData.pincode}
                    </div>
                    <div className="text-emerald-700 font-medium pt-1 flex items-center gap-1">
                      <Truck className="w-3.5 h-3.5" />
                      <span>BlueDart Insured Air Express (Complimentary)</span>
                    </div>
                  </div>
                )}

              </div>

              {/* STEP 2: PAYMENT GATEWAY (INTERACTIVE FULL MOCK) */}
              <div className={`bg-white rounded-3xl border border-[#EAE4DC] p-6 sm:p-8 shadow-md transition-all ${currentStep === 2 ? 'ring-2 ring-[#7A152E]/10' : 'opacity-70 pointer-events-none'}`}>
                
                <div className="flex items-center justify-between pb-6 border-b border-[#EAE4DC]">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-[#7A152E] text-white text-xs font-bold flex items-center justify-center">
                      2
                    </div>
                    <div>
                      <h2 className="font-serif text-lg sm:text-xl font-normal text-stone-900">
                        Payment Gateway
                      </h2>
                      <p className="text-xs text-stone-500 mt-0.5">
                        Encrypted RBI-compliant transaction with instantaneous hallmark confirmation.
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-serif font-bold text-[#7A152E]">
                    Payable: ₹{cartTotal.toLocaleString('en-IN')}
                  </span>
                </div>

                {currentStep === 2 && (
                  <div className="mt-6 space-y-6">
                    
                    {/* Payment Mode Selector Tabs */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      {[
                        { id: 'upi', label: 'UPI Instant', icon: QrCode, sub: 'Zero Fee • Fast' },
                        { id: 'card', label: 'Cards', icon: CreditCard, sub: 'Visa, RuPay, MC' },
                        { id: 'netbanking', label: 'Net Banking', icon: Building2, sub: '50+ Banks' },
                        { id: 'cod', label: 'Cash / COD', icon: Banknote, sub: 'Doorstep UPI/Cash' }
                      ].map((mode) => {
                        const Icon = mode.icon;
                        const isSelected = paymentMethod === mode.id;
                        return (
                          <button
                            key={mode.id}
                            type="button"
                            onClick={() => setPaymentMethod(mode.id)}
                            className={`p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                              isSelected
                                ? 'border-[#7A152E] bg-[#FAF8F5] ring-2 ring-[#7A152E]/15 shadow-sm'
                                : 'border-stone-200 bg-white hover:border-stone-300'
                            }`}
                          >
                            <div className="flex items-center justify-between">
                              <Icon className={`w-5 h-5 ${isSelected ? 'text-[#7A152E]' : 'text-stone-400'}`} />
                              {isSelected && <span className="w-2 h-2 rounded-full bg-[#7A152E]" />}
                            </div>
                            <div className="mt-3">
                              <div className={`font-bold text-xs ${isSelected ? 'text-[#7A152E]' : 'text-stone-900'}`}>
                                {mode.label}
                              </div>
                              <div className="text-[10px] text-stone-500 mt-0.5">{mode.sub}</div>
                            </div>
                          </button>
                        );
                      })}
                    </div>

                    {/* TAB A: UPI PAYMENT (MOST POPULAR) */}
                    {paymentMethod === 'upi' && (
                      <div className="p-6 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-6 animate-fadeIn">
                        
                        {/* Quick UPI App Selector */}
                        <div>
                          <label className="block text-xs font-bold text-stone-800 mb-2">
                            Select UPI App
                          </label>
                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                            {[
                              { id: 'gpay', name: 'Google Pay', color: '#4285F4' },
                              { id: 'phonepe', name: 'PhonePe', color: '#5F259F' },
                              { id: 'paytm', name: 'Paytm UPI', color: '#00BAF2' },
                              { id: 'bhim', name: 'BHIM / CRED', color: '#00796B' }
                            ].map(app => (
                              <button
                                key={app.id}
                                type="button"
                                onClick={() => setUpiApp(app.id)}
                                className={`py-2.5 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer ${
                                  upiApp === app.id
                                    ? 'bg-white border-[#7A152E] text-[#7A152E] shadow-sm ring-1 ring-[#7A152E]'
                                    : 'bg-white/60 border-stone-200 text-stone-700 hover:bg-white'
                                }`}
                              >
                                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: app.color }} />
                                <span>{app.name}</span>
                              </button>
                            ))}
                          </div>
                        </div>

                        {/* Interactive Dynamic QR Code */}
                        <div className="flex flex-col sm:flex-row items-center gap-6 p-5 rounded-2xl bg-white border border-stone-200 shadow-xs">
                          {/* Generated QR Graphic with Logo Overlay */}
                          <div className="relative p-3 bg-white rounded-2xl border-2 border-[#7A152E]/30 shadow-md shrink-0">
                            <svg width="130" height="130" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <rect width="100" height="100" fill="white" />
                              {/* Corner targets */}
                              <rect x="5" y="5" width="26" height="26" stroke="#231F20" strokeWidth="4" fill="none" rx="4" />
                              <rect x="11" y="11" width="14" height="14" fill="#7A152E" rx="2" />
                              <rect x="69" y="5" width="26" height="26" stroke="#231F20" strokeWidth="4" fill="none" rx="4" />
                              <rect x="75" y="11" width="14" height="14" fill="#7A152E" rx="2" />
                              <rect x="5" y="69" width="26" height="26" stroke="#231F20" strokeWidth="4" fill="none" rx="4" />
                              <rect x="11" y="75" width="14" height="14" fill="#7A152E" rx="2" />
                              {/* QR Code Dots Mock */}
                              <rect x="36" y="10" width="8" height="8" fill="#231F20" />
                              <rect x="48" y="15" width="12" height="6" fill="#231F20" />
                              <rect x="36" y="24" width="6" height="12" fill="#231F20" />
                              <rect x="10" y="36" width="16" height="6" fill="#231F20" />
                              <rect x="10" y="48" width="8" height="10" fill="#231F20" />
                              <rect x="42" y="42" width="16" height="16" fill="#C5A059" rx="3" />
                              <rect x="68" y="38" width="10" height="8" fill="#231F20" />
                              <rect x="82" y="48" width="8" height="12" fill="#231F20" />
                              <rect x="38" y="68" width="12" height="8" fill="#231F20" />
                              <rect x="48" y="80" width="18" height="10" fill="#231F20" />
                              <rect x="72" y="72" width="18" height="18" fill="#231F20" />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                              <span className="w-6 h-6 rounded-full bg-white border border-[#C5A059] flex items-center justify-center text-[8px] font-bold text-[#7A152E]">
                                925
                              </span>
                            </div>
                          </div>

                          <div className="text-left space-y-1.5 flex-1">
                            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10.5px] font-bold">
                              <span>Zero Convenience Fee</span>
                            </div>
                            <h4 className="font-serif text-base font-bold text-stone-900">
                              Scan with any UPI App
                            </h4>
                            <p className="text-xs text-stone-500 leading-relaxed font-light">
                              Open Google Pay, PhonePe, Paytm, or your banking app and scan this secure QR code to pay <strong className="text-stone-900">₹{cartTotal.toLocaleString('en-IN')}</strong>.
                            </p>
                            <div className="text-[11px] text-[#7A152E] font-mono font-semibold flex items-center gap-1.5 pt-1">
                              <Clock className="w-3.5 h-3.5" />
                              <span>QR Code expires in {formattedUpiTime}</span>
                            </div>
                          </div>
                        </div>

                        {/* Or Enter UPI ID */}
                        <div className="space-y-2">
                          <label className="block text-xs font-bold text-stone-800">
                            Or Enter Virtual Payment Address (VPA) / UPI ID
                          </label>
                          <div className="flex gap-2">
                            <input
                              type="text"
                              value={upiId}
                              onChange={(e) => setUpiId(e.target.value)}
                              placeholder="e.g. yourname@okhdfcbank"
                              className="flex-1 px-3.5 py-2.5 rounded-xl border border-stone-200 bg-white text-xs focus:border-[#7A152E] focus:outline-none font-mono"
                            />
                            <button
                              type="button"
                              onClick={() => {
                                if (upiId) showToast(`UPI ID ${upiId} verified!`);
                                else showToast('Please enter your UPI ID', 'info');
                              }}
                              className="px-4 py-2.5 rounded-xl border border-stone-300 bg-white hover:bg-stone-50 text-stone-800 text-xs font-semibold cursor-pointer"
                            >
                              Verify
                            </button>
                          </div>
                        </div>

                      </div>
                    )}

                    {/* TAB B: CREDIT / DEBIT CARDS WITH INTERACTIVE 3D CARD VISUALIZER */}
                    {paymentMethod === 'card' && (
                      <div className="p-6 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-6 animate-fadeIn">
                        
                        {/* Interactive Metallic Luxury Card Preview */}
                        <div className="relative w-full max-w-sm mx-auto aspect-[1.586/1] rounded-2xl p-6 text-white bg-gradient-to-tr from-[#1E1E24] via-[#2A1520] to-[#7A152E] shadow-2xl border border-white/20 flex flex-col justify-between overflow-hidden">
                          {/* Hologram shine & Chip */}
                          <div className="flex items-center justify-between">
                            <div className="w-11 h-8 rounded-md bg-gradient-to-r from-[#D5B980] via-[#F3E5C8] to-[#C5A059] border border-[#C5A059]/60 flex items-center justify-center shadow-xs">
                              <div className="w-8 h-5 border border-[#9E7B35]/40 rounded-xs" />
                            </div>
                            <span className="font-serif tracking-widest text-sm font-semibold text-white/90">
                              SOLYSTRA ATELIER
                            </span>
                          </div>

                          {/* Card Number display */}
                          <div className="font-mono text-base sm:text-lg tracking-widest drop-shadow-md text-stone-100 py-1">
                            {cardData.number || '•••• •••• •••• 9250'}
                          </div>

                          {/* Footer of Card */}
                          <div className="flex items-end justify-between text-xs">
                            <div>
                              <span className="text-[8px] uppercase tracking-wider text-stone-300 block">CARDHOLDER</span>
                              <span className="font-medium tracking-wider text-stone-100 uppercase">{cardData.name || 'VRUND SHAH'}</span>
                            </div>
                            <div>
                              <span className="text-[8px] uppercase tracking-wider text-stone-300 block">EXPIRES</span>
                              <span className="font-mono text-stone-100">{cardData.expiry || 'MM/YY'}</span>
                            </div>
                            <div className="font-bold font-mono text-sm tracking-wider text-white">
                              {cardBrand}
                            </div>
                          </div>
                        </div>

                        {/* Quick Prefill for Testing */}
                        <div className="flex justify-end">
                          <button
                            type="button"
                            onClick={handlePrefillDemoCard}
                            className="text-xs font-semibold text-[#7A152E] hover:underline flex items-center gap-1 cursor-pointer"
                          >
                            <CreditCard className="w-3.5 h-3.5" />
                            <span>Prefill Test Visa Card</span>
                          </button>
                        </div>

                        {/* Card Form Inputs */}
                        <div className="space-y-4 text-xs">
                          <div>
                            <label className="block text-stone-700 font-semibold mb-1">
                              Card Number
                            </label>
                            <div className="relative">
                              <input
                                type="text"
                                maxLength={19}
                                value={cardData.number}
                                onChange={handleCardNumberChange}
                                placeholder="4532 •••• •••• ••••"
                                className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-white font-mono text-xs focus:border-[#7A152E] focus:outline-none"
                              />
                              <CreditCard className="w-4 h-4 text-stone-400 absolute right-3 top-3" />
                            </div>
                          </div>

                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div className="sm:col-span-2">
                              <label className="block text-stone-700 font-semibold mb-1">
                                Cardholder Name
                              </label>
                              <input
                                type="text"
                                value={cardData.name}
                                onChange={(e) => setCardData({ ...cardData, name: e.target.value.toUpperCase() })}
                                placeholder="NAME AS ON CARD"
                                className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-white uppercase text-xs focus:border-[#7A152E] focus:outline-none"
                              />
                            </div>

                            <div>
                              <label className="block text-stone-700 font-semibold mb-1">
                                Expiry (MM/YY)
                              </label>
                              <input
                                type="text"
                                maxLength={5}
                                value={cardData.expiry}
                                onChange={handleExpiryChange}
                                placeholder="MM/YY"
                                className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-white font-mono text-xs focus:border-[#7A152E] focus:outline-none"
                              />
                            </div>
                          </div>

                          <div className="w-32">
                            <label className="block text-stone-700 font-semibold mb-1">
                              CVV / CVC
                            </label>
                            <input
                              type="password"
                              maxLength={4}
                              value={cardData.cvv}
                              onChange={(e) => setCardData({ ...cardData, cvv: e.target.value.replace(/\D/g, '') })}
                              placeholder="•••"
                              className="w-full px-3.5 py-2.5 rounded-xl border border-stone-200 bg-white font-mono text-xs focus:border-[#7A152E] focus:outline-none"
                            />
                          </div>

                          <label className="flex items-center gap-2 pt-1 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={cardData.saveCard}
                              onChange={(e) => setCardData({ ...cardData, saveCard: e.target.checked })}
                              className="rounded text-[#7A152E] focus:ring-[#7A152E]"
                            />
                            <span className="text-[11px] text-stone-600">
                              Securely save this card as per RBI tokenization directives.
                            </span>
                          </label>
                        </div>

                      </div>
                    )}

                    {/* TAB C: NET BANKING */}
                    {paymentMethod === 'netbanking' && (
                      <div className="p-6 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-4 animate-fadeIn">
                        <label className="block text-xs font-bold text-stone-800">
                          Popular Indian Banks
                        </label>
                        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                          {['HDFC', 'ICICI', 'State Bank of India', 'Axis Bank', 'Kotak Mahindra', 'Punjab National'].map(bank => (
                            <button
                              key={bank}
                              type="button"
                              onClick={() => setSelectedBank(bank)}
                              className={`p-3 rounded-xl border text-xs font-semibold text-center transition-all cursor-pointer ${
                                selectedBank === bank
                                  ? 'border-[#7A152E] bg-white text-[#7A152E] shadow-sm ring-1 ring-[#7A152E]'
                                  : 'border-stone-200 bg-white/60 text-stone-700 hover:bg-white'
                              }`}
                            >
                              {bank}
                            </button>
                          ))}
                        </div>

                        <div className="pt-2">
                          <label className="block text-xs font-bold text-stone-800 mb-1.5">
                            Or Select Other Major Banks
                          </label>
                          <div className="flex flex-wrap gap-2">
                            {['Bank of Baroda', 'IndusInd Bank', 'Yes Bank', 'IDFC First Bank', 'Canara Bank', 'Union Bank'].map(bank => (
                              <button
                                key={bank}
                                type="button"
                                onClick={() => setSelectedBank(bank)}
                                className={`px-3 py-1.5 rounded-xl border text-xs font-medium transition-all cursor-pointer ${
                                  selectedBank === bank
                                    ? 'border-[#7A152E] bg-white text-[#7A152E] font-bold shadow-2xs ring-1 ring-[#7A152E]'
                                    : 'border-stone-200 bg-white text-stone-600 hover:border-[#7A152E]/40 hover:text-stone-900'
                                }`}
                              >
                                {bank}
                              </button>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}

                    {/* TAB D: CASH ON DELIVERY (COD) */}
                    {paymentMethod === 'cod' && (
                      <div className="p-6 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-4 animate-fadeIn text-xs">
                        <div className="flex items-start gap-3 p-4 rounded-xl bg-stone-50 border border-stone-200 text-stone-800">
                          <AlertCircle className="w-5 h-5 text-[#7A152E] shrink-0 mt-0.5" />
                          <div className="leading-relaxed">
                            <strong>Doorstep Cash / UPI Verification:</strong> BlueDart courier will present your BIS Hallmarked Keepsake Vault. You can pay via Cash or any UPI QR code directly to the delivery personnel upon inspection.
                          </div>
                        </div>

                        <div className="space-y-2 pt-1">
                          <label className="block text-stone-800 font-bold">
                            Mobile Verification for COD Orders
                          </label>
                          {!codOtpSent ? (
                            <button
                              type="button"
                              onClick={() => {
                                setCodOtpSent(true);
                                showToast('Mock OTP 9250 sent to +91 ' + formData.phone);
                              }}
                              className="px-5 py-2.5 bg-stone-900 hover:bg-black text-white rounded-xl font-semibold cursor-pointer"
                            >
                              Send Verification OTP (+91 {formData.phone})
                            </button>
                          ) : !codVerified ? (
                            <div className="flex gap-2 items-center">
                              <input
                                type="text"
                                maxLength={4}
                                value={codOtp}
                                onChange={(e) => setCodOtp(e.target.value)}
                                placeholder="Enter OTP (Use: 9250)"
                                className="w-48 px-3.5 py-2 rounded-xl border border-stone-200 bg-white font-mono text-center tracking-widest text-sm focus:border-[#7A152E] focus:outline-none"
                              />
                              <button
                                type="button"
                                onClick={() => {
                                  if (codOtp === '9250' || codOtp.length === 4) {
                                    setCodVerified(true);
                                    showToast('Mobile number verified for COD delivery!');
                                  } else {
                                    showToast('Invalid OTP. Use demo OTP 9250', 'info');
                                  }
                                }}
                                className="px-4 py-2 bg-emerald-700 text-white rounded-xl font-semibold cursor-pointer"
                              >
                                Verify OTP
                              </button>
                            </div>
                          ) : (
                            <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 font-semibold">
                              <CheckCircle2 className="w-4 h-4" />
                              <span>Phone Number Verified for COD</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Final CTA Action */}
                    <div className="pt-4">
                      <button
                        type="button"
                        onClick={handleCompleteOrder}
                        className="w-full py-4 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs sm:text-sm font-semibold uppercase tracking-wider rounded-xl shadow-xl transition-all cursor-pointer flex items-center justify-center gap-2"
                      >
                        <Lock className="w-4 h-4 text-white/90" />
                        <span>Place Order & Pay ₹{cartTotal.toLocaleString('en-IN')}</span>
                      </button>
                      <div className="flex items-center justify-center gap-2 text-[10.5px] text-stone-500 mt-2">
                        <ShieldCheck className="w-3.5 h-3.5 text-[#C5A059]" />
                        <span>Instant Refund Guarantee &bull; 15-Day Exchange Policy</span>
                      </div>
                    </div>

                  </div>
                )}

              </div>

            </div>

            {/* RIGHT COLUMN: STICKY ORDER SUMMARY SIDEBAR (5 COLS) */}
            <div className="hidden lg:block lg:col-span-5 lg:sticky lg:top-28 space-y-6">
              
              <div className="bg-white rounded-3xl border border-[#EAE4DC] p-6 sm:p-7 shadow-lg space-y-6">
                
                <div className="flex items-center justify-between pb-4 border-b border-[#EAE4DC]">
                  <h3 className="font-serif text-lg font-bold text-stone-900">
                    Order Summary ({cart.reduce((t, i) => t + i.quantity, 0)} Pieces)
                  </h3>
                  <span className="text-xs text-stone-500 font-mono">
                    BIS 925 Guaranteed
                  </span>
                </div>

                {/* Items Mini List */}
                <div className="divide-y divide-stone-100 max-h-64 overflow-y-auto pr-1">
                  {cart.map((item) => (
                    <div key={item.variantKey} className="py-3 flex items-center gap-3.5">
                      <div className="relative w-14 h-14 rounded-xl overflow-hidden border border-stone-200 shrink-0 bg-stone-50">
                        <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                        <span className="absolute top-0 right-0 w-4 h-4 rounded-bl-lg bg-[#7A152E] text-white text-[9px] flex items-center justify-center font-mono">
                          {item.quantity}
                        </span>
                      </div>

                      <div className="flex-1 min-w-0 text-xs">
                        <h4 className="font-serif font-medium text-stone-900 truncate">
                          {item.shortName || item.name}
                        </h4>
                        <div className="text-[11px] text-stone-500 mt-0.5">
                          {item.metal} {item.size && `• Size ${item.size}`}
                        </div>
                      </div>

                      <div className="text-right shrink-0 text-xs">
                        <div className="font-bold text-stone-900">
                          ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                        </div>
                        {item.mrp && item.mrp > item.price && (
                          <div className="text-[10px] text-stone-400 line-through">
                            ₹{(item.mrp * item.quantity).toLocaleString('en-IN')}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Complimentary Velvet Keepsake Vault Toggle */}
                <div className="p-3.5 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <Package className="w-5 h-5 text-[#7A152E] shrink-0" />
                    <div>
                      <div className="text-xs font-bold text-stone-900">Velvet Keepsake Vault</div>
                      <div className="text-[10.5px] text-stone-500">Hallmark card + Royal velvet box</div>
                    </div>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={isGiftPackagingAdded}
                      onChange={(e) => setIsGiftPackagingAdded(e.target.checked)}
                      className="sr-only peer"
                    />
                    <div className="w-9 h-5 bg-stone-300 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-stone-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[#7A152E]"></div>
                  </label>
                </div>

                {/* Promo Code Input */}
                {appliedCoupon ? (
                  <div className="flex items-center justify-between p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs">
                    <div className="flex items-center gap-2 text-emerald-800 font-bold">
                      <Tag className="w-4 h-4 text-emerald-700" />
                      <span>{appliedCoupon.code} applied ({appliedCoupon.label})</span>
                    </div>
                    <button
                      onClick={removeCoupon}
                      className="text-xs text-red-600 hover:underline font-bold cursor-pointer"
                    >
                      Remove
                    </button>
                  </div>
                ) : (
                  <form onSubmit={handleApplyCoupon} className="flex gap-2">
                    <input
                      type="text"
                      value={couponCodeInput}
                      onChange={(e) => setCouponCodeInput(e.target.value)}
                      placeholder="Promo Code (e.g. ROYAL10)"
                      className="flex-1 text-xs px-3.5 py-2.5 rounded-xl border border-stone-200 bg-stone-50/50 uppercase tracking-wider focus:outline-none focus:border-[#7A152E]"
                    />
                    <button
                      type="submit"
                      className="px-4 py-2.5 bg-stone-900 hover:bg-black text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer"
                    >
                      Apply
                    </button>
                  </form>
                )}

                {/* Pricing Summary Breakdown */}
                <div className="space-y-2 pt-2 border-t border-[#EAE4DC] text-xs text-stone-600">
                  <div className="flex justify-between">
                    <span>Bag Subtotal (MRP)</span>
                    <span className="font-semibold text-stone-900">₹{cartMrpTotal.toLocaleString('en-IN')}</span>
                  </div>

                  {totalSavings > 0 && (
                    <div className="flex justify-between text-emerald-700 font-medium">
                      <span>Atelier Direct Savings</span>
                      <span>-₹{totalSavings.toLocaleString('en-IN')}</span>
                    </div>
                  )}

                  {discountAmount > 0 && (
                    <div className="flex justify-between text-[#7A152E] font-bold">
                      <span>Coupon Discount ({appliedCoupon?.code})</span>
                      <span>-₹{discountAmount.toLocaleString('en-IN')}</span>
                    </div>
                  )}

                  <div className="flex justify-between">
                    <span>BlueDart Insured Air Express</span>
                    <span className="font-bold text-emerald-700">FREE</span>
                  </div>

                  <div className="flex justify-between">
                    <span>Velvet Keepsake Packaging</span>
                    <span className="font-bold text-emerald-700">COMPLIMENTARY</span>
                  </div>

                  <div className="pt-3 border-t border-[#EAE4DC] flex justify-between items-baseline">
                    <span className="font-serif text-base font-bold text-stone-900">Grand Total</span>
                    <span className="font-serif text-2xl font-bold text-[#7A152E]">
                      ₹{cartTotal.toLocaleString('en-IN')}
                    </span>
                  </div>
                  <div className="text-[10.5px] text-stone-400 text-right">
                    Includes all central & state GST taxes
                  </div>
                </div>

                {/* Trust Guarantee Bullets */}
                <div className="p-4 rounded-2xl bg-stone-50 border border-stone-200 space-y-2 text-[11px] text-stone-600">
                  <div className="flex items-center gap-2">
                    <ShieldCheck className="w-4 h-4 text-[#C5A059]" />
                    <span>Government BIS 925 Hallmark Certified</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Award className="w-4 h-4 text-[#7A152E]" />
                    <span>2.0µm Rhodium Anti-Tarnish Platinum Clad</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Truck className="w-4 h-4 text-emerald-700" />
                    <span>Insured Transit & Free 15-Day Exchange</span>
                  </div>
                </div>

              </div>

            </div>

          </div>
        )}

      </main>

      {/* ========================================================
          PROCESSING MODAL OVERLAY SIMULATION
          ======================================================== */}
      {isProcessing && (
        <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-stone-950 rounded-3xl p-8 sm:p-10 max-w-sm w-full border border-stone-700 shadow-2xl text-center space-y-5">
            <div className="w-16 h-16 rounded-full border-3 border-stone-700 border-t-[#C5A059] animate-spin mx-auto" />
            <h3 className="font-serif text-xl text-white font-normal">
              Processing Transaction
            </h3>
            <p className="text-xs text-stone-400 font-mono animate-pulse">
              {processingStepText}
            </p>
            <div className="pt-2 text-[10px] text-stone-500">
              Please do not refresh or press back.
            </div>
          </div>
        </div>
      )}

      {/* ========================================================
          BLUEDART TRACKING MODAL
          ======================================================== */}
      {showBlueDartTracking && (
        <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-lg w-full border border-stone-200 shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-stone-200">
              <div className="flex items-center gap-2">
                <Truck className="w-5 h-5 text-[#7A152E]" />
                <h3 className="font-serif text-lg font-bold text-stone-900">
                  BlueDart Air Tracking Status
                </h3>
              </div>
              <button
                onClick={() => setShowBlueDartTracking(false)}
                className="text-stone-400 hover:text-stone-800 text-xs font-bold"
              >
                ✕ Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between p-3 rounded-xl bg-stone-50 font-mono">
                <span>Waybill: {lastOrder?.waybillNumber || 'BD-AIR-894210'}</span>
                <span className="text-emerald-700 font-bold">In Transit (Air)</span>
              </div>

              <div className="border-l-2 border-[#7A152E] pl-4 space-y-4 pt-2">
                <div>
                  <div className="font-bold text-stone-900">Consignment Manifested & Picked Up</div>
                  <div className="text-[11px] text-stone-500">Mumbai Central Aviation Facility &bull; Today, 9:45 PM</div>
                </div>
                <div>
                  <div className="font-bold text-stone-900">Security X-Ray & Vault Transit Seal Verified</div>
                  <div className="text-[11px] text-stone-500">BOM Hub &bull; Today, 10:15 PM</div>
                </div>
                <div className="opacity-60">
                  <div className="font-bold text-stone-700">Out for Priority Delivery Handover</div>
                  <div className="text-[11px] text-stone-400">Destination Delivery Facility &bull; Expected {lastOrder?.estimatedDelivery}</div>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowBlueDartTracking(false)}
              className="w-full py-3 bg-[#7A152E] text-white text-xs font-semibold rounded-xl"
            >
              Done
            </button>
          </div>
        </div>
      )}

    </div>
  );
};
