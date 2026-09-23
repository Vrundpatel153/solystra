import React, { useState } from 'react';
import { useShop } from '../context/ShopContext';
import {
  X,
  Trash2,
  Plus,
  Minus,
  ShoppingBag,
  ShieldCheck,
  ArrowRight,
  Tag,
  Package,
  Lock,
  Truck,
  Award
} from 'lucide-react';

export const CartDrawer = () => {
  const {
    cart,
    isCartOpen,
    setIsCartOpen,
    cartItemCount,
    cartSubtotal,
    cartMrpTotal,
    totalSavings,
    discountAmount,
    appliedCoupon,
    shippingFee,
    cartTotal,
    freeShippingThreshold,
    isFreeShipping,
    removeFromCart,
    updateQuantity,
    applyCoupon,
    removeCoupon,
    startCheckout,
    isGiftPackagingAdded,
    setIsGiftPackagingAdded
  } = useShop();

  const [couponInput, setCouponInput] = useState('');

  if (!isCartOpen) return null;

  const handleApplyCoupon = (e) => {
    e.preventDefault();
    if (couponInput) {
      applyCoupon(couponInput);
      setCouponInput('');
    }
  };

  const amountNeededForFreeShipping = Math.max(0, freeShippingThreshold - cartSubtotal);
  const shippingProgress = Math.min(100, Math.round((cartSubtotal / freeShippingThreshold) * 100));

  return (
    <div className="fixed inset-0 z-50 overflow-hidden font-sans">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-xs transition-opacity"
        onClick={() => setIsCartOpen(false)}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-6 sm:pl-10">
        <div data-lenis-prevent="true" className="w-screen max-w-md bg-white shadow-2xl flex flex-col border-l border-[#EAE4DC] animate-slideLeft">
          
          {/* Header */}
          <div className="p-5 border-b border-[#EAE4DC] flex items-center justify-between bg-[#FAF8F5]">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-[#7A152E]/10 flex items-center justify-center text-[#7A152E]">
                <ShoppingBag className="w-4 h-4" />
              </div>
              <div>
                <h2 className="font-serif text-base sm:text-lg font-bold text-stone-900 tracking-wide">
                  Shopping Bag
                </h2>
                <span className="text-[11px] text-stone-500">
                  {cartItemCount} {cartItemCount === 1 ? 'Design' : 'Designs'} Selected
                </span>
              </div>
            </div>

            <button
              onClick={() => setIsCartOpen(false)}
              className="p-2 rounded-full hover:bg-stone-200/60 text-stone-500 hover:text-stone-900 transition-colors cursor-pointer"
              aria-label="Close bag"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Free Shipping Progress Meter */}
          {cart.length > 0 && (
            <div className="bg-[#FAF8F5] px-5 py-3.5 border-b border-[#EAE4DC]">
              <div className="flex items-center justify-between text-xs mb-1.5">
                <span className="text-stone-800">
                  {isFreeShipping ? (
                    <span className="text-emerald-800 font-bold flex items-center gap-1.5 text-xs">
                      <Truck className="w-3.5 h-3.5 text-emerald-700" />
                      <span>Complimentary Insured Air Express Unlocked!</span>
                    </span>
                  ) : (
                    <span>
                      Add <strong className="text-[#7A152E]">₹{amountNeededForFreeShipping.toLocaleString('en-IN')}</strong> more for Free Delivery
                    </span>
                  )}
                </span>
                <span className="font-mono font-bold text-[#C5A059] text-[11px]">
                  {shippingProgress}%
                </span>
              </div>
              <div className="w-full bg-[#EAE4DC] rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-[#7A152E] to-[#C5A059] h-full rounded-full transition-all duration-500"
                  style={{ width: `${shippingProgress}%` }}
                />
              </div>
            </div>
          )}

          {/* Cart Items List */}
          <div className="flex-1 overflow-y-auto p-5 divide-y divide-stone-100 hide-scrollbar">
            {cart.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-6 text-stone-500 space-y-4">
                <div className="w-20 h-20 rounded-3xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E] shadow-xs">
                  <ShoppingBag className="w-9 h-9 stroke-[1.5]" />
                </div>
                <div>
                  <h3 className="font-serif text-xl font-normal text-stone-900">Your Bag is Empty</h3>
                  <p className="text-xs text-stone-500 mt-1 max-w-xs leading-relaxed">
                    Discover our certified 925 sterling silver and 18K gold vermeil handcrafted collections.
                  </p>
                </div>
                <button
                  onClick={() => setIsCartOpen(false)}
                  className="px-6 py-3 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs uppercase tracking-wider font-semibold rounded-xl shadow-md transition-all cursor-pointer"
                >
                  Explore Collections
                </button>
              </div>
            ) : (
              <>
                {cart.map((item) => (
                  <div key={item.variantKey} className="py-4 flex gap-3.5 items-start">
                    
                    {/* Item Image */}
                    <div
                      className="w-20 h-20 rounded-xl overflow-hidden bg-stone-50 border border-stone-200 shrink-0 cursor-pointer"
                      onClick={() => {
                        setIsCartOpen(false);
                        window.location.hash = `#/product/${item.id}`;
                      }}
                    >
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>

                    {/* Item Details */}
                    <div className="flex-1 min-w-0 text-xs">
                      <h4
                        className="font-serif text-sm font-normal text-stone-900 truncate hover:text-[#7A152E] transition-colors cursor-pointer"
                        onClick={() => {
                          setIsCartOpen(false);
                          window.location.hash = `#/product/${item.id}`;
                        }}
                      >
                        {item.shortName || item.name}
                      </h4>

                      <div className="flex flex-wrap items-center gap-1.5 mt-1 text-[10.5px]">
                        <span className="px-2 py-0.5 rounded bg-[#FAF8F5] border border-[#EAE4DC] text-stone-800 font-medium">
                          {item.metal}
                        </span>
                        {item.size && (
                          <span className="px-1.5 py-0.5 rounded bg-[#FAF8F5] border border-[#EAE4DC] text-stone-600">
                            Size {item.size}
                          </span>
                        )}
                        {item.engraving && (
                          <span className="text-[#7A152E] italic">
                            "{item.engraving}"
                          </span>
                        )}
                      </div>

                      {/* Stepper and Price */}
                      <div className="flex items-center justify-between mt-3 pt-1">
                        <div className="flex items-center border border-stone-200 rounded-lg overflow-hidden bg-white shadow-2xs">
                          <button
                            onClick={() => updateQuantity(item.variantKey, -1)}
                            className="p-1 px-2.5 hover:bg-stone-100 text-stone-700 cursor-pointer"
                            aria-label="Decrease quantity"
                          >
                            <Minus className="w-3 h-3" />
                          </button>
                          <span className="px-2 text-xs font-semibold text-stone-900 font-mono">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => updateQuantity(item.variantKey, 1)}
                            className="p-1 px-2.5 hover:bg-stone-100 text-stone-700 cursor-pointer"
                            aria-label="Increase quantity"
                          >
                            <Plus className="w-3 h-3" />
                          </button>
                        </div>

                        <div className="text-right">
                          <span className="font-serif text-sm font-bold text-[#7A152E]">
                            ₹{(item.price * item.quantity).toLocaleString('en-IN')}
                          </span>
                          {item.mrp && item.mrp > item.price && (
                            <div className="text-[10px] text-stone-400 line-through">
                              ₹{(item.mrp * item.quantity).toLocaleString('en-IN')}
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Delete action */}
                    <button
                      onClick={() => removeFromCart(item.variantKey)}
                      className="text-stone-400 hover:text-red-600 p-1 transition-colors cursor-pointer"
                      aria-label="Remove item"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}

                {/* Velvet Keepsake Vault Free Addon */}
                <div className="mt-4 p-3.5 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5">
                    <Package className="w-5 h-5 text-[#7A152E] shrink-0" />
                    <div>
                      <div className="text-xs font-bold text-stone-900">Complimentary Velvet Vault</div>
                      <div className="text-[10px] text-stone-500">Hallmark certificate & royal keepsake box</div>
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
              </>
            )}
          </div>

          {/* Footer Order Summary & Checkout Trigger */}
          {cart.length > 0 && (
            <div className="p-5 border-t border-[#EAE4DC] bg-[#FAF8F5] space-y-3 shadow-lg">
              
              {/* Promo Code Input & Quick Tags */}
              {appliedCoupon ? (
                <div className="flex items-center justify-between p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs">
                  <div className="flex items-center gap-1.5 text-emerald-800 font-bold">
                    <Tag className="w-3.5 h-3.5 text-emerald-700" />
                    <span>{appliedCoupon.code} applied ({appliedCoupon.label})</span>
                  </div>
                  <button
                    onClick={removeCoupon}
                    className="text-[11px] text-red-600 hover:underline font-bold cursor-pointer"
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <div className="space-y-1.5">
                  <form onSubmit={handleApplyCoupon} className="flex gap-2">
                    <input
                      type="text"
                      value={couponInput}
                      onChange={(e) => setCouponInput(e.target.value)}
                      placeholder="Promo Code (e.g. ROYAL10)"
                      className="flex-1 text-xs px-3 py-2 bg-white border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E] uppercase font-mono tracking-wider"
                    />
                    <button
                      type="submit"
                      className="px-4 py-2 bg-stone-900 hover:bg-black text-white text-xs font-semibold rounded-xl transition-colors cursor-pointer"
                    >
                      Apply
                    </button>
                  </form>
                  <div className="flex items-center gap-2 text-[10.5px] text-stone-500">
                    <span>Try:</span>
                    <button
                      type="button"
                      onClick={() => applyCoupon('ROYAL10')}
                      className="text-[#7A152E] font-mono font-bold hover:underline cursor-pointer"
                    >
                      ROYAL10
                    </button>
                    <span>&bull;</span>
                    <button
                      type="button"
                      onClick={() => applyCoupon('VAULT500')}
                      className="text-[#7A152E] font-mono font-bold hover:underline cursor-pointer"
                    >
                      VAULT500
                    </button>
                  </div>
                </div>
              )}

              {/* Price Breakdown */}
              <div className="space-y-1 text-xs text-stone-600 pt-1">
                <div className="flex justify-between">
                  <span>Bag Subtotal</span>
                  <span className="font-semibold text-stone-900">₹{cartSubtotal.toLocaleString('en-IN')}</span>
                </div>

                {totalSavings > 0 && (
                  <div className="flex justify-between text-emerald-700">
                    <span>Atelier Savings</span>
                    <span>-₹{totalSavings.toLocaleString('en-IN')}</span>
                  </div>
                )}

                {discountAmount > 0 && (
                  <div className="flex justify-between text-[#7A152E] font-bold">
                    <span>Coupon Discount</span>
                    <span>-₹{discountAmount.toLocaleString('en-IN')}</span>
                  </div>
                )}

                <div className="flex justify-between">
                  <span>BlueDart Insured Air Express</span>
                  <span className="font-bold text-emerald-700">FREE</span>
                </div>

                <div className="border-t border-[#EAE4DC] pt-2 flex justify-between items-baseline font-serif">
                  <span className="text-sm font-bold text-stone-900">Total Payable</span>
                  <span className="text-lg font-bold text-[#7A152E]">
                    ₹{cartTotal.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>

              {/* Proceed to Checkout CTA */}
              <button
                onClick={startCheckout}
                className="w-full py-4 bg-[#7A152E] hover:bg-[#590D1E] text-white rounded-xl font-serif text-xs uppercase tracking-widest font-bold transition-all flex items-center justify-center gap-2 shadow-xl hover:shadow-2xl cursor-pointer"
              >
                <Lock className="w-4 h-4 text-white/90" />
                <span>Proceed to Checkout &bull; ₹{cartTotal.toLocaleString('en-IN')}</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              {/* Purity Guarantee Footer */}
              <div className="flex items-center justify-center gap-3 text-[10px] text-stone-500 pt-1">
                <span className="flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5 text-[#C5A059]" /> 256-Bit Encrypted
                </span>
                <span>&bull;</span>
                <span className="text-[#7A152E] font-bold">BIS 925 Guaranteed</span>
                <span>&bull;</span>
                <span>15-Day Exchange</span>
              </div>

            </div>
          )}

        </div>
      </div>
    </div>
  );
};
