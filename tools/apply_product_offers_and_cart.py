#!/usr/bin/env python3
"""
apply_product_offers_and_cart.py
Updates product page offers and aligns cart/checkout discount logic:
1. Flat 100rs off on prepaid (code PREPAID100 & auto-applied on prepaid checkout)
2. 5% off on order above 5000 (code SOL5)
3. 10% off on order above 10k (code SOL10)
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.abspath('.')

# ==============================================================================
# 1. NEW OFFERS HTML BLOCK FOR product.html
# ==============================================================================
NEW_OFFERS_HTML = """<div class="space-y-2 pt-1"><div class="text-xs font-semibold text-stone-900 tracking-wide flex items-center justify-between"><span>Available offers</span><span class="text-[10.5px] text-[#61532E] font-medium">Auto-applied at checkout</span></div><div class="flex gap-2.5 overflow-x-auto hide-scrollbar pb-1"><button class="min-w-[155px] sm:min-w-[170px] p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] text-left hover:border-[#61532E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 active:scale-95 shadow-2xs" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('PREPAID100')"><div class="flex items-center justify-between"><p class="text-xs font-bold text-stone-900 leading-tight">Flat ₹100 off</p><span class="text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1.5 py-0.5 rounded">PREPAID</span></div><p class="text-[10.5px] text-stone-600 mt-1">On all prepaid orders</p><div class="mt-2.5 text-[10.5px] font-mono tracking-wide flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700">use <strong class="text-[#61532E] font-bold">PREPAID100</strong></span><span class="text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button><button class="min-w-[155px] sm:min-w-[170px] p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] text-left hover:border-[#61532E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 active:scale-95 shadow-2xs" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('SOL5')"><div class="flex items-center justify-between"><p class="text-xs font-bold text-stone-900 leading-tight">Get 5% off</p><span class="text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1.5 py-0.5 rounded">&gt; ₹5,000</span></div><p class="text-[10.5px] text-stone-600 mt-1">On orders above ₹5,000</p><div class="mt-2.5 text-[10.5px] font-mono tracking-wide flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700">use <strong class="text-[#61532E] font-bold">SOL5</strong></span><span class="text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button><button class="min-w-[155px] sm:min-w-[170px] p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] text-left hover:border-[#61532E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 active:scale-95 shadow-2xs" type="button" onclick="window.usePromoCode &amp;&amp; window.usePromoCode('SOL10')"><div class="flex items-center justify-between"><p class="text-xs font-bold text-stone-900 leading-tight">Get 10% off</p><span class="text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1.5 py-0.5 rounded">&gt; ₹10,000</span></div><p class="text-[10.5px] text-stone-600 mt-1">On orders above ₹10,000</p><div class="mt-2.5 text-[10.5px] font-mono tracking-wide flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5"><span class="text-stone-700">use <strong class="text-[#61532E] font-bold">SOL10</strong></span><span class="text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span></div></button></div></div>"""

OLD_OFFERS_PAT = r'<div class="space-y-2 pt-1"><div class="text-xs font-semibold text-stone-900 tracking-wide(?: flex items-center justify-between)?[^>]*><span>Available offers</span>.*?</div><div class="flex gap-2\.5 overflow-x-auto hide-scrollbar pb-1">.*?</div></div>|<div class="space-y-2 pt-1"><div class="text-xs font-semibold text-stone-900 tracking-wide">Available offers</div><div class="flex gap-2\.5 overflow-x-auto hide-scrollbar pb-1">.*?</div></div>'

# ==============================================================================
# 2. CART DRAWER PROMO TRY CHIPS
# ==============================================================================
NEW_CART_TRY_CHIPS = """<div class="flex flex-wrap items-center gap-1.5 text-[10.5px] text-stone-500">
<span>Offers:</span>
<button class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors" onclick="window.usePromoCode('PREPAID100')" type="button" title="Flat ₹100 OFF on prepaid">PREPAID100</button>
<button class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors" onclick="window.usePromoCode('SOL5')" type="button" title="5% OFF above ₹5,000">SOL5 (5% OFF)</button>
<button class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors" onclick="window.usePromoCode('SOL10')" type="button" title="10% OFF above ₹10,000">SOL10 (10% OFF)</button>
</div>"""

OLD_CART_TRY_CHIPS_PAT = r'<div class="flex items-center gap-2 text-\[10\.5px\] text-stone-500">\s*<span>Try:</span>\s*<button class="text-\[#61532E\] font-mono font-bold hover:underline cursor-pointer" onclick="window\.usePromoCode\(\'ROYAL10\'\)"[^>]*>ROYAL10</button>\s*<span>•</span>\s*<button class="text-\[#61532E\] font-mono font-bold hover:underline cursor-pointer" onclick="window\.usePromoCode\(\'VAULT500\'\)"[^>]*>VAULT500</button>\s*</div>'

# ==============================================================================
# 3. CHECKOUT COUPON TRY CHIPS
# ==============================================================================
NEW_CHECKOUT_TRY_CHIPS = """<div class="flex flex-wrap items-center gap-1.5 text-[10.5px] text-stone-500 -mt-2">
<span>Offers:</span>
<button type="button" onclick="window.useCheckoutPromo('PREPAID100')" class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors">PREPAID100</button>
<button type="button" onclick="window.useCheckoutPromo('SOL5')" class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors">SOL5 (5% OFF)</button>
<button type="button" onclick="window.useCheckoutPromo('SOL10')" class="text-[#61532E] font-mono font-bold bg-[#61532E]/10 hover:bg-[#61532E]/20 px-1.5 py-0.5 rounded cursor-pointer transition-colors">SOL10 (10% OFF)</button>
</div>"""

OLD_CHECKOUT_TRY_CHIPS_PAT = r'<div class="flex items-center gap-2 text-\[10\.5px\] text-stone-500 -mt-3">\s*<span>Try:</span>\s*<button type="button" onclick="window\.useCheckoutPromo\(\'ROYAL10\'\)"[^>]*>ROYAL10</button>\s*<span>•</span>\s*<button type="button" onclick="window\.useCheckoutPromo\(\'VAULT500\'\)"[^>]*>VAULT500</button>\s*</div>'

def patch_html_file(file_path):
    if not os.path.isfile(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content

    # 1. Patch product.html offers
    if os.path.basename(file_path) == 'product.html':
        if re.search(OLD_OFFERS_PAT, content, re.DOTALL):
            content = re.sub(OLD_OFFERS_PAT, NEW_OFFERS_HTML, content, count=1, flags=re.DOTALL)
            print(f"  [{os.path.basename(file_path)}] Updated Available Offers (Flat 100, 5% > 5k, 10% > 10k)")

    # 2. Patch cart drawer try chips
    if re.search(OLD_CART_TRY_CHIPS_PAT, content, re.DOTALL):
        content = re.sub(OLD_CART_TRY_CHIPS_PAT, NEW_CART_TRY_CHIPS, content, count=1, flags=re.DOTALL)
        print(f"  [{os.path.basename(file_path)}] Updated Cart Drawer Offer Chips")

    # 3. Patch checkout try chips
    if os.path.basename(file_path) == 'checkout.html':
        if re.search(OLD_CHECKOUT_TRY_CHIPS_PAT, content, re.DOTALL):
            content = re.sub(OLD_CHECKOUT_TRY_CHIPS_PAT, NEW_CHECKOUT_TRY_CHIPS, content, count=1, flags=re.DOTALL)
            print(f"  [{os.path.basename(file_path)}] Updated Checkout Offer Chips")

    if content != orig:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved {file_path}")

def patch_app_js(js_path):
    if not os.path.isfile(js_path):
        return
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
    orig = js

    # 1. Update applyPromoCode
    old_apply_promo = """  window.applyPromoCode = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    const input = document.getElementById('cart-promo-input');
    if (!input) return;
    const val = input.value.trim().toUpperCase();

    if (val === 'ROYAL10') {
      setAppliedPromo('ROYAL10');
      window.showToast('Promo Code Applied!', '10% privilege discount unlocked.');
    } else if (val === 'VAULT500') {
      setAppliedPromo('VAULT500');
      window.showToast('Promo Code Applied!', 'Flat ₹500 discount unlocked.');
    } else if (val === 'SOULY10') {
      setAppliedPromo('SOULY10');
      window.showToast('Welcome Offer Applied!', '10% privilege discount unlocked.');
    } else {
      window.showToast('Invalid Code', 'Try ROYAL10 or VAULT500', 'info');
      return;
    }
    renderCartDrawer();
  };"""

    new_apply_promo = """  window.applyPromoCode = function (e) {
    if (e && e.preventDefault) e.preventDefault();
    const input = document.getElementById('cart-promo-input');
    if (!input) return;
    const val = input.value.trim().toUpperCase();
    const cart = getCart();
    const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);

    if (val === 'PREPAID100') {
      setAppliedPromo('PREPAID100');
      window.showToast('Prepaid Offer Applied!', 'Flat ₹100 discount on prepaid orders unlocked.');
    } else if (val === 'SOL5') {
      setAppliedPromo('SOL5');
      if (subtotal >= 5000) {
        window.showToast('5% Privilege Applied!', '5% discount on order above ₹5,000 unlocked.');
      } else {
        const diff = 5000 - subtotal;
        window.showToast('Offer Code Saved!', 'Add ₹' + diff.toLocaleString('en-IN') + ' more to unlock 5% OFF.', 'info');
      }
    } else if (val === 'SOL10') {
      setAppliedPromo('SOL10');
      if (subtotal >= 10000) {
        window.showToast('10% Privilege Applied!', '10% discount on order above ₹10,000 unlocked.');
      } else {
        const diff = 10000 - subtotal;
        window.showToast('Offer Code Saved!', 'Add ₹' + diff.toLocaleString('en-IN') + ' more to unlock 10% OFF.', 'info');
      }
    } else if (val === 'ROYAL10' || val === 'SOULY10') {
      setAppliedPromo(val);
      window.showToast('Welcome Offer Applied!', '10% privilege discount unlocked.');
    } else if (val === 'VAULT500') {
      setAppliedPromo('VAULT500');
      window.showToast('Promo Code Applied!', 'Flat ₹500 discount unlocked.');
    } else {
      window.showToast('Invalid Code', 'Try PREPAID100, SOL5, or SOL10', 'info');
      return;
    }
    renderCartDrawer();
  };"""

    if old_apply_promo in js:
        js = js.replace(old_apply_promo, new_apply_promo)
        print(f"  [{os.path.basename(js_path)}] Updated window.applyPromoCode")

    # 2. Update usePromoCode
    old_use_promo = """  window.usePromoCode = function (code) {
    const input = document.getElementById('cart-promo-input');
    if (input) input.value = code;
    setAppliedPromo(code);
    window.showToast('Promo Code Applied!', `${code} unlocked successfully.`);
    renderCartDrawer();
  };"""

    new_use_promo = """  window.usePromoCode = function (code) {
    const input = document.getElementById('cart-promo-input');
    if (input) input.value = code;
    setAppliedPromo(code);
    const cart = getCart();
    const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    if (code === 'PREPAID100') {
      window.showToast('Prepaid Offer Applied!', 'Flat ₹100 off on prepaid orders unlocked.');
    } else if (code === 'SOL5') {
      if (subtotal >= 5000) {
        window.showToast('5% Privilege Applied!', '5% discount unlocked on orders above ₹5,000.');
      } else {
        window.showToast('Code Applied!', 'Add ₹' + (5000 - subtotal).toLocaleString('en-IN') + ' more to unlock 5% OFF.', 'info');
      }
    } else if (code === 'SOL10') {
      if (subtotal >= 10000) {
        window.showToast('10% Privilege Applied!', '10% discount unlocked on orders above ₹10,000.');
      } else {
        window.showToast('Code Applied!', 'Add ₹' + (10000 - subtotal).toLocaleString('en-IN') + ' more to unlock 10% OFF.', 'info');
      }
    } else {
      window.showToast('Promo Code Applied!', `${code} unlocked successfully.`);
    }
    renderCartDrawer();
  };"""

    if old_use_promo in js:
        js = js.replace(old_use_promo, new_use_promo)
        print(f"  [{os.path.basename(js_path)}] Updated window.usePromoCode")

    # 3. Update Cart Drawer discount calculation in renderCartDrawer
    old_cart_calc = """    // Promo calculation
    const promo = getAppliedPromo();
    let discount = 0;
    if (promo === 'ROYAL10' || promo === 'SOULY10') {
      discount = Math.round(subtotal * 0.10);
    } else if (promo === 'VAULT500') {
      discount = Math.min(500, subtotal);
    }

    const totalPayable = Math.max(0, subtotal - discount);"""

    new_cart_calc = """    // Promo calculation with 3 client-specified offers:
    // 1. Flat 100 off on prepaid (PREPAID100)
    // 2. 5% off on order above 5000 (SOL5)
    // 3. 10% off on order above 10k (SOL10)
    const promo = getAppliedPromo();
    let discount = 0;
    let promoBadge = '';

    if (promo === 'PREPAID100') {
      discount = Math.min(100, subtotal);
      promoBadge = 'PREPAID100 (Flat ₹100 Off)';
    } else if (promo === 'SOL5') {
      if (subtotal >= 5000) {
        discount = Math.round(subtotal * 0.05);
        promoBadge = 'SOL5 (5% Off above ₹5,000)';
      }
    } else if (promo === 'SOL10') {
      if (subtotal >= 10000) {
        discount = Math.round(subtotal * 0.10);
        promoBadge = 'SOL10 (10% Off above ₹10,000)';
      }
    } else if (promo === 'ROYAL10' || promo === 'SOULY10') {
      discount = Math.round(subtotal * 0.10);
      promoBadge = promo + ' (10% Off)';
    } else if (promo === 'VAULT500') {
      discount = Math.min(500, subtotal);
      promoBadge = 'VAULT500 (Flat ₹500 Off)';
    }

    const totalPayable = Math.max(0, subtotal - discount);"""

    if old_cart_calc in js:
        js = js.replace(old_cart_calc, new_cart_calc)
        print(f"  [{os.path.basename(js_path)}] Updated cart drawer discount calculation")

    # 4. Update checkout coupon & computeTotals in initCheckoutPage
    old_checkout_coupon = """      if (code.toUpperCase() === 'ROYAL10' || code.toUpperCase() === 'SOULY10') {
        setAppliedPromo(code.toUpperCase());
        window.showToast('Privilege Code Applied', '10% privilege reduction unlocked.');
      } else if (code.toUpperCase() === 'VAULT500') {
        setAppliedPromo(code.toUpperCase());
        window.showToast('Privilege Code Applied', 'Flat ₹500 vault credit applied.');
      } else {
        window.showToast('Invalid Code', 'Try ROYAL10 or VAULT500.', 'info');
      }"""

    new_checkout_coupon = """      const cUpper = code.toUpperCase();
      const sub = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
      if (cUpper === 'PREPAID100') {
        setAppliedPromo('PREPAID100');
        window.showToast('Prepaid Offer Applied', 'Flat ₹100 discount on prepaid orders.');
      } else if (cUpper === 'SOL5') {
        setAppliedPromo('SOL5');
        if (sub >= 5000) {
          window.showToast('5% Privilege Applied', '5% discount on order above ₹5,000.');
        } else {
          window.showToast('Code Saved', 'Add ₹' + (5000 - sub).toLocaleString('en-IN') + ' more for 5% OFF.', 'info');
        }
      } else if (cUpper === 'SOL10') {
        setAppliedPromo('SOL10');
        if (sub >= 10000) {
          window.showToast('10% Privilege Applied', '10% discount on order above ₹10,000.');
        } else {
          window.showToast('Code Saved', 'Add ₹' + (10000 - sub).toLocaleString('en-IN') + ' more for 10% OFF.', 'info');
        }
      } else if (cUpper === 'ROYAL10' || cUpper === 'SOULY10') {
        setAppliedPromo(cUpper);
        window.showToast('Privilege Code Applied', '10% privilege reduction unlocked.');
      } else if (cUpper === 'VAULT500') {
        setAppliedPromo('VAULT500');
        window.showToast('Privilege Code Applied', 'Flat ₹500 vault credit applied.');
      } else {
        window.showToast('Invalid Code', 'Try PREPAID100, SOL5, or SOL10.', 'info');
      }"""

    if old_checkout_coupon in js:
        js = js.replace(old_checkout_coupon, new_checkout_coupon)
        print(f"  [{os.path.basename(js_path)}] Updated checkout applyCheckoutCoupon")

    # 5. Update computeTotals in initCheckoutPage to give Flat 100 on Prepaid & calculate tiered 5%/10%
    old_compute_totals = """    // Calculate totals
    function computeTotals() {
      const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
      const mrpTotal = cart.reduce((acc, item) => acc + ((item.mrp || item.price) * item.quantity), 0);
      const savings = Math.max(0, mrpTotal - subtotal);

      const promo = getAppliedPromo();
      let discount = 0;
      if (promo === 'ROYAL10' || promo === 'SOULY10') {
        discount = Math.round(subtotal * 0.10);
      } else if (promo === 'VAULT500') {
        discount = Math.min(500, subtotal);
      }

      const grandTotal = Math.max(0, subtotal - discount + deliverySpeedCost);

      return { subtotal, mrpTotal, savings, discount, grandTotal, promo };
    }"""

    new_compute_totals = """    // Calculate totals with 3 client-specified offers:
    // 1. Flat 100 off on prepaid (UPI, Card, NetBanking or PREPAID100)
    // 2. 5% off on order above 5000 (SOL5)
    // 3. 10% off on order above 10k (SOL10)
    function computeTotals() {
      const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
      const mrpTotal = cart.reduce((acc, item) => acc + ((item.mrp || item.price) * item.quantity), 0);
      const savings = Math.max(0, mrpTotal - subtotal);

      const promo = getAppliedPromo();
      let couponDiscount = 0;
      let couponLabel = '';

      if (promo === 'PREPAID100') {
        couponDiscount = Math.min(100, subtotal);
        couponLabel = 'PREPAID100';
      } else if (promo === 'SOL5') {
        if (subtotal >= 5000) {
          couponDiscount = Math.round(subtotal * 0.05);
          couponLabel = 'SOL5 (5% OFF)';
        }
      } else if (promo === 'SOL10') {
        if (subtotal >= 10000) {
          couponDiscount = Math.round(subtotal * 0.10);
          couponLabel = 'SOL10 (10% OFF)';
        }
      } else if (promo === 'ROYAL10' || promo === 'SOULY10') {
        couponDiscount = Math.round(subtotal * 0.10);
        couponLabel = promo;
      } else if (promo === 'VAULT500') {
        couponDiscount = Math.min(500, subtotal);
        couponLabel = 'VAULT500';
      }

      // Flat 100 off on prepaid payment methods
      const isPrepaid = (selectedPaymentMode !== 'cod');
      let prepaidDiscount = 0;
      if (isPrepaid) {
        // If PREPAID100 was already applied as coupon, don't duplicate
        if (promo !== 'PREPAID100') {
          prepaidDiscount = 100;
        }
      }

      const totalDiscount = couponDiscount + prepaidDiscount;
      const grandTotal = Math.max(0, subtotal - totalDiscount + deliverySpeedCost);

      return { subtotal, mrpTotal, savings, discount: totalDiscount, couponDiscount, prepaidDiscount, couponLabel, grandTotal, promo };
    }"""

    if old_compute_totals in js:
        js = js.replace(old_compute_totals, new_compute_totals)
        print(f"  [{os.path.basename(js_path)}] Updated checkout computeTotals with prepaid & tier discounts")

    # 6. Re-render order summary when payment mode changes
    old_select_tab = """    window.selectPaymentTab = function (modeId) {
      selectedPaymentMode = modeId;
      const modes = ['upi', 'card', 'netbanking', 'cod'];

      modes.forEach(m => {
        const btn = document.getElementById('tab-btn-' + m);
        const panel = document.getElementById('payment-panel-' + m);

        if (m === modeId) {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-[#61532E] bg-[#FAF8F5] ring-2 ring-[#61532E]/15 shadow-sm';
            const dot = btn.querySelector('span.w-2.h-2');
            if (dot) dot.className = 'w-2 h-2 rounded-full bg-[#61532E]';
          }
          if (panel) panel.classList.remove('hidden');
        } else {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-stone-200 bg-white hover:border-stone-300';
            const dot = btn.querySelector('span.w-2.h-2');
            if (dot) dot.className = 'w-2 h-2 rounded-full border border-stone-300';
          }
          if (panel) panel.classList.add('hidden');
        }
      });
    };"""

    new_select_tab = """    window.selectPaymentTab = function (modeId) {
      selectedPaymentMode = modeId;
      const modes = ['upi', 'card', 'netbanking', 'cod'];

      modes.forEach(m => {
        const btn = document.getElementById('tab-btn-' + m);
        const panel = document.getElementById('payment-panel-' + m);

        if (m === modeId) {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-[#61532E] bg-[#FAF8F5] ring-2 ring-[#61532E]/15 shadow-sm';
            const dot = btn.querySelector('span.w-2.h-2');
            if (dot) dot.className = 'w-2 h-2 rounded-full bg-[#61532E]';
          }
          if (panel) panel.classList.remove('hidden');
        } else {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-stone-200 bg-white hover:border-stone-300';
            const dot = btn.querySelector('span.w-2.h-2');
            if (dot) dot.className = 'w-2 h-2 rounded-full border border-stone-300';
          }
          if (panel) panel.classList.add('hidden');
        }
      });
      renderOrderSummary();
    };"""

    if old_select_tab in js:
        js = js.replace(old_select_tab, new_select_tab)
        print(f"  [{os.path.basename(js_path)}] Updated selectPaymentTab to recompute totals on payment mode change")

    # 7. Update renderOrderSummary label in checkout
    old_summary_discount = """      const discountRow = document.getElementById('summary-discount-row');
      const discountTotal = document.getElementById('summary-discount-total');
      if (totals.discount > 0) {
        if (discountRow) discountRow.classList.remove('hidden');
        if (discountTotal) discountTotal.textContent = '-' + formatINR(totals.discount);
      } else {
        if (discountRow) discountRow.classList.add('hidden');
      }"""

    new_summary_discount = """      const discountRow = document.getElementById('summary-discount-row');
      const discountTotal = document.getElementById('summary-discount-total');
      const discountLabel = document.getElementById('summary-discount-label');
      if (totals.discount > 0) {
        if (discountRow) discountRow.classList.remove('hidden');
        if (discountTotal) discountTotal.textContent = '-' + formatINR(totals.discount);
        if (discountLabel) {
          let parts = [];
          if (totals.couponDiscount > 0) parts.push(totals.couponLabel || 'Coupon');
          if (totals.prepaidDiscount > 0) parts.push('Prepaid Flat ₹100 Off');
          discountLabel.textContent = parts.length > 0 ? parts.join(' + ') : 'Special Privilege Discount';
        }
      } else {
        if (discountRow) discountRow.classList.add('hidden');
      }"""

    if old_summary_discount in js:
        js = js.replace(old_summary_discount, new_summary_discount)
        print(f"  [{os.path.basename(js_path)}] Updated renderOrderSummary discount breakdown label")

    if js != orig:
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Saved {js_path}")

def main():
    folders = ['jewellery-design-html', 'jewellery-design-html-dist']
    for folder in folders:
        dir_path = os.path.join(ROOT, folder)
        if not os.path.exists(dir_path):
            continue
        print(f"\n--- Processing {folder} ---")
        for fname in os.listdir(dir_path):
            if fname.endswith('.html'):
                patch_html_file(os.path.join(dir_path, fname))
        patch_app_js(os.path.join(dir_path, 'js', 'app.js'))

if __name__ == '__main__':
    main()
