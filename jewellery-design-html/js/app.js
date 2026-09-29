/**
 * Solystra Jewels - Pure HTML/CSS/JS Atelier Experience
 * Full interactive ecommerce flow matching React 1:1
 */

(function () {
  'use strict';

  // State keys
  const CART_KEY = 'solystra_cart';
  const WISHLIST_KEY = 'solystra_wishlist';
  const PROMO_KEY = 'solystra_promo';
  const VELVET_KEY = 'solystra_velvet_vault';

  // Helpers for storage
  function getCart() {
    try {
      const data = localStorage.getItem(CART_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }

  function saveCart(cart) {
    try {
      localStorage.setItem(CART_KEY, JSON.stringify(cart));
      updateBadges();
      renderCartDrawer();
    } catch (e) {}
  }

  function getWishlist() {
    try {
      const data = localStorage.getItem(WISHLIST_KEY);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      return [];
    }
  }

  function saveWishlist(wishlist) {
    try {
      localStorage.setItem(WISHLIST_KEY, JSON.stringify(wishlist));
      updateBadges();
      renderWishlistDrawer();
    } catch (e) {}
  }

  function getAppliedPromo() {
    return localStorage.getItem(PROMO_KEY) || '';
  }

  function setAppliedPromo(code) {
    if (code) {
      localStorage.setItem(PROMO_KEY, code.toUpperCase());
    } else {
      localStorage.removeItem(PROMO_KEY);
    }
  }

  function isVelvetVaultEnabled() {
    const val = localStorage.getItem(VELVET_KEY);
    return val === null ? true : val === 'true';
  }

  function setVelvetVaultEnabled(val) {
    localStorage.setItem(VELVET_KEY, val ? 'true' : 'false');
  }

  // Format currency
  function formatINR(num) {
    return '₹' + Number(num || 0).toLocaleString('en-IN');
  }

  // Find product by ID
  function findProduct(id) {
    if (!window.PRODUCTS || !window.PRODUCTS.length) return null;
    return window.PRODUCTS.find(p => p.id === id) || null;
  }

  // Toast Notification
  window.showToast = function (title, message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast-item pointer-events-auto bg-white border border-[#EAE4DC] shadow-2xl rounded-2xl p-4 flex items-center justify-between gap-3 text-stone-900 border-l-4 ' +
      (type === 'success' ? 'border-l-[#7A152E]' : 'border-l-[#C5A059]');

    toast.innerHTML = `
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-xl bg-[#7A152E]/10 flex items-center justify-center text-[#7A152E] shrink-0">
          <svg class="lucide lucide-sparkles w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"></path></svg>
        </div>
        <div>
          <div class="font-serif text-xs sm:text-sm font-bold text-stone-900">${title}</div>
          <div class="text-[11px] text-stone-500">${message}</div>
        </div>
      </div>
      <button onclick="this.parentElement.remove()" class="p-1 rounded-full text-stone-400 hover:text-stone-800 transition-colors cursor-pointer">
        <svg class="lucide lucide-x w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
      </button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      if (toast.parentElement) toast.remove();
    }, 3500);
  };

  // Badges update
  function updateBadges() {
    const cart = getCart();
    const wishlist = getWishlist();
    const count = cart.reduce((acc, item) => acc + (item.quantity || 1), 0);

    // Cart badge mobile
    const mobBadge = document.getElementById('nav-cart-badge-mobile');
    if (mobBadge) {
      mobBadge.textContent = count;
      if (count > 0) mobBadge.classList.remove('hidden');
      else mobBadge.classList.add('hidden');
    }

    // Cart text desktop
    const deskText = document.getElementById('nav-cart-text-desktop');
    if (deskText) {
      deskText.textContent = `Bag (${count})`;
    }

    // Wishlist badge
    const wishBadge = document.getElementById('nav-wishlist-badge');
    if (wishBadge) {
      wishBadge.textContent = wishlist.length;
      if (wishlist.length > 0) wishBadge.classList.remove('hidden');
      else wishBadge.classList.add('hidden');
    }

    // Header count in cart drawer
    const cartHeaderCount = document.getElementById('cart-header-count');
    if (cartHeaderCount) {
      cartHeaderCount.textContent = `${count} ${count === 1 ? 'Design' : 'Designs'} Selected`;
    }

    // Header count in wishlist drawer
    const wishHeaderTitle = document.getElementById('wishlist-header-title');
    if (wishHeaderTitle) {
      wishHeaderTitle.textContent = `Your Wishlist (${wishlist.length})`;
    }
  }

  // Cart operations
  window.addToCart = function (product, metal, size, engraving = '', quantity = 1) {
    if (!product) return;
    const cart = getCart();

    const selectedMetal = metal || (product.metals && product.metals[0]) || 'Pure 925 Silver';
    const selectedSize = size || (product.category === 'rings' ? '12' : null);

    const existingIndex = cart.findIndex(item =>
      item.id === product.id &&
      item.metal === selectedMetal &&
      item.size === selectedSize &&
      item.engraving === engraving
    );

    if (existingIndex > -1) {
      cart[existingIndex].quantity += quantity;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        mrp: product.mrp || product.price,
        image: (product.images && product.images[0]) || 'solystra_assets/categories/zavya_style/necklaces.png',
        category: product.category,
        metal: selectedMetal,
        size: selectedSize,
        engraving: engraving,
        quantity: quantity
      });
    }

    saveCart(cart);
    window.showToast('Added to Shopping Bag', `${product.name} has been added.`);
    window.openCartDrawer();
  };

  window.quickAddToCart = function (productId) {
    const product = findProduct(productId);
    if (!product) return;
    window.addToCart(product);
  };

  window.updateCartQuantity = function (index, delta) {
    const cart = getCart();
    if (!cart[index]) return;

    cart[index].quantity += delta;
    if (cart[index].quantity <= 0) {
      cart.splice(index, 1);
    }
    saveCart(cart);
  };

  window.removeCartItem = function (index) {
    const cart = getCart();
    if (!cart[index]) return;
    cart.splice(index, 1);
    saveCart(cart);
  };

  window.toggleVelvetVault = function (checked) {
    setVelvetVaultEnabled(checked);
    renderCartDrawer();
  };

  window.applyPromoCode = function (e) {
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
  };

  window.usePromoCode = function (code) {
    const input = document.getElementById('cart-promo-input');
    if (input) input.value = code;
    setAppliedPromo(code);
    window.showToast('Promo Code Applied!', `${code} unlocked successfully.`);
    renderCartDrawer();
  };

  // Render Cart Drawer
  function renderCartDrawer() {
    const itemsContainer = document.getElementById('cart-drawer-items');
    if (!itemsContainer) return;

    const cart = getCart();
    if (cart.length === 0) {
      itemsContainer.innerHTML = `
        <div class="h-64 flex flex-col items-center justify-center text-center p-6 text-stone-400 space-y-4">
          <div class="w-16 h-16 rounded-full bg-[#FAF8F5] border border-[#EAE4DC] flex items-center justify-center text-[#7A152E]">
            <svg class="lucide lucide-shopping-bag w-8 h-8 opacity-70" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
          </div>
          <div class="font-serif text-base sm:text-lg font-bold text-stone-900">Your Bag is Empty</div>
          <p class="text-xs text-stone-500 max-w-xs">
            Discover our handcrafted BIS hallmarked 925 sterling silver &amp; 18K gold collections.
          </p>
          <a href="products.html" onclick="window.closeCartDrawer()" class="px-6 py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-widest font-semibold rounded-xl hover:bg-[#590D1E] transition-all shadow-sm">
            Explore Collection
          </a>
        </div>
      `;

      // Update totals to 0
      const subtotalEl = document.getElementById('cart-subtotal-text');
      const totalEl = document.getElementById('cart-total-text');
      const btnText = document.getElementById('cart-checkout-btn-text');
      if (subtotalEl) subtotalEl.textContent = formatINR(0);
      if (totalEl) totalEl.textContent = formatINR(0);
      if (btnText) btnText.textContent = `Proceed to Checkout • ${formatINR(0)}`;
      return;
    }

    let subtotal = 0;
    let savings = 0;

    itemsContainer.innerHTML = cart.map((item, idx) => {
      const itemTotal = item.price * item.quantity;
      const mrpTotal = (item.mrp || item.price) * item.quantity;
      subtotal += itemTotal;
      if (mrpTotal > itemTotal) savings += (mrpTotal - itemTotal);

      return `
        <div class="py-4 flex gap-3.5 items-start">
          <div class="w-20 h-20 rounded-xl overflow-hidden bg-stone-50 border border-stone-200 shrink-0 cursor-pointer" onclick="window.location.href='product.html?id=${item.id}'">
            <img src="${item.image}" alt="${item.name}" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300">
          </div>
          <div class="flex-1 min-w-0 text-xs">
            <h4 onclick="window.location.href='product.html?id=${item.id}'" class="font-serif text-sm font-normal text-stone-900 truncate hover:text-[#7A152E] transition-colors cursor-pointer">
              ${item.name}
            </h4>
            <div class="flex flex-wrap items-center gap-1.5 mt-1 text-[10.5px]">
              <span class="px-2 py-0.5 rounded bg-[#FAF8F5] border border-[#EAE4DC] text-stone-800 font-medium">${item.metal}</span>
              ${item.size ? `<span class="px-1.5 py-0.5 rounded bg-stone-100 text-stone-600 font-mono">Size ${item.size}</span>` : ''}
              ${item.engraving ? `<span class="px-1.5 py-0.5 rounded bg-stone-100 text-stone-600 font-mono text-[9px]">"${item.engraving}"</span>` : ''}
            </div>
            <div class="flex items-center justify-between mt-3 pt-1">
              <div class="flex items-center border border-stone-200 rounded-lg overflow-hidden bg-white shadow-2xs">
                <button onclick="window.updateCartQuantity(${idx}, -1)" aria-label="Decrease quantity" class="p-1 px-2.5 hover:bg-stone-100 text-stone-700 cursor-pointer">
                  <svg class="lucide lucide-minus w-3 h-3" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M5 12h14"></path></svg>
                </button>
                <span class="px-2 text-xs font-semibold text-stone-900 font-mono">${item.quantity}</span>
                <button onclick="window.updateCartQuantity(${idx}, 1)" aria-label="Increase quantity" class="p-1 px-2.5 hover:bg-stone-100 text-stone-700 cursor-pointer">
                  <svg class="lucide lucide-plus w-3 h-3" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M5 12h14"></path><path d="M12 5v14"></path></svg>
                </button>
              </div>
              <div class="text-right">
                <span class="font-serif text-sm font-bold text-[#7A152E]">${formatINR(itemTotal)}</span>
                ${item.mrp && item.mrp > item.price ? `<div class="text-[10px] text-stone-400 line-through">${formatINR(mrpTotal)}</div>` : ''}
              </div>
            </div>
          </div>
          <button onclick="window.removeCartItem(${idx})" aria-label="Remove item" class="text-stone-400 hover:text-red-600 p-1 transition-colors cursor-pointer">
            <svg class="lucide lucide-trash2 w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" x2="10" y1="11" y2="17"></line><line x1="14" x2="14" y1="11" y2="17"></line></svg>
          </button>
        </div>
      `;
    }).join('');

    // Promo calculation
    const promo = getAppliedPromo();
    let discount = 0;
    if (promo === 'ROYAL10' || promo === 'SOULY10') {
      discount = Math.round(subtotal * 0.10);
    } else if (promo === 'VAULT500') {
      discount = Math.min(500, subtotal);
    }

    const totalPayable = Math.max(0, subtotal - discount);

    const subtotalEl = document.getElementById('cart-subtotal-text');
    if (subtotalEl) subtotalEl.textContent = formatINR(subtotal);

    const savingsEl = document.getElementById('cart-savings-text');
    if (savingsEl) savingsEl.textContent = '-' + formatINR(savings + discount);

    const totalEl = document.getElementById('cart-total-text');
    if (totalEl) totalEl.textContent = formatINR(totalPayable);

    const btnText = document.getElementById('cart-checkout-btn-text');
    if (btnText) btnText.textContent = `Proceed to Checkout • ${formatINR(totalPayable)}`;

    // Velvet vault checkbox state
    const vaultCb = document.getElementById('cart-velvet-vault-checkbox');
    if (vaultCb) vaultCb.checked = isVelvetVaultEnabled();
  }

  // Wishlist operations
  window.toggleWishlist = function (productId) {
    if (!productId) return;
    const wishlist = getWishlist();
    const idx = wishlist.indexOf(productId);
    const prod = findProduct(productId);
    const name = prod ? prod.name : 'Piece';

    if (idx > -1) {
      wishlist.splice(idx, 1);
      window.showToast('Removed from Wishlist', `${name} removed from your saved pieces.`, 'info');
    } else {
      wishlist.push(productId);
      window.showToast('Saved to Wishlist', `${name} saved to your wishlist.`);
    }

    saveWishlist(wishlist);
  };

  window.isInWishlist = function (productId) {
    return getWishlist().includes(productId);
  };

  function renderWishlistDrawer() {
    const container = document.getElementById('wishlist-drawer-items');
    if (!container) return;

    const wishlist = getWishlist();
    if (wishlist.length === 0) {
      container.innerHTML = `
        <div class="h-full flex flex-col items-center justify-center text-center p-6 text-[#717171] space-y-4">
          <div class="w-16 h-16 rounded-full bg-[#FAF8F5] flex items-center justify-center text-[#7A152E] border border-[#E8E5DF]">
            <svg class="lucide lucide-heart w-8 h-8 opacity-70" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
          </div>
          <div class="font-serif text-lg font-semibold text-[#111111]">No Favorites Saved Yet</div>
          <p class="text-xs text-[#717171] max-w-xs">
            Tap the heart icon on any jewelry piece to save it to your wishlist.
          </p>
          <a href="products.html" onclick="window.closeWishlistDrawer()" class="px-6 py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-widest font-semibold rounded-lg hover:bg-[#590D1E] transition-all shadow-sm">
            Discover Pieces
          </a>
        </div>
      `;
      return;
    }

    container.innerHTML = wishlist.map(id => {
      const p = findProduct(id);
      if (!p) return '';
      return `
        <div class="py-4 flex gap-4 items-center">
          <div class="w-20 h-20 rounded-lg overflow-hidden bg-[#FAF8F5] border border-[#E8E5DF] shrink-0 cursor-pointer" onclick="window.location.href='product.html?id=${p.id}'">
            <img src="${p.images[0]}" alt="${p.name}" class="w-full h-full object-cover hover:scale-105 transition-transform">
          </div>
          <div class="flex-1 min-w-0">
            <div onclick="window.location.href='product.html?id=${p.id}'" class="font-serif text-sm font-semibold text-[#111111] truncate cursor-pointer hover:text-[#7A152E] transition-colors">
              ${p.shortName || p.name}
            </div>
            <div class="font-serif text-sm font-bold text-[#7A152E] mt-1">
              ${formatINR(p.price)}
            </div>
            <div class="flex items-center gap-2 mt-2">
              <button onclick="window.addToCart(window.PRODUCTS.find(x => x.id === '${p.id}')); window.toggleWishlist('${p.id}')" class="px-3 py-1 bg-[#7A152E] text-white text-[11px] uppercase tracking-wider font-semibold rounded hover:bg-[#590D1E] transition-colors flex items-center gap-1 shadow-sm cursor-pointer">
                <svg class="lucide lucide-shopping-bag w-3 h-3" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
                Move to Bag
              </button>
              <button onclick="window.toggleWishlist('${p.id}')" class="p-1 text-[#717171] hover:text-[#7A152E] transition-colors cursor-pointer" aria-label="Remove from wishlist">
                <svg class="lucide lucide-trash2 w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M3 6h18"></path><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path><line x1="10" x2="10" y1="11" y2="17"></line><line x1="14" x2="14" y1="11" y2="17"></line></svg>
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  // Quick View Modal
  window.openQuickView = function (productId) {
    const p = findProduct(productId);
    if (!p) return;

    const modal = document.getElementById('quickview-modal-root');
    const content = document.getElementById('quickview-content');
    if (!modal || !content) return;

    const defaultMetal = p.metalType === 'gold' ? '18K Yellow Gold' : (p.metalType === 'rose' ? 'Rose Gold Plated' : 'Pure 925 Silver');
    const isRing = p.category === 'rings';

    content.innerHTML = `
      <!-- Gallery -->
      <div class="p-6 bg-[#FAF8F5] flex flex-col items-center justify-center border-b md:border-b-0 md:border-r border-[#E8E5DF]">
        <div class="w-full aspect-square rounded-xl overflow-hidden bg-white border border-[#E8E5DF] shadow-sm relative group mb-4">
          <img id="qv-main-img" src="${p.images[0]}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
        </div>
        ${p.images.length > 1 ? `
          <div class="flex gap-2 overflow-x-auto max-w-full pb-1 no-scrollbar">
            ${p.images.map((img, i) => `
              <button onclick="document.getElementById('qv-main-img').src='${img}'" class="w-14 h-14 rounded-lg overflow-hidden border-2 border-[#E8E5DF] opacity-70 hover:opacity-100 hover:border-[#7A152E] transition-all cursor-pointer">
                <img src="${img}" alt="Angle" class="w-full h-full object-cover">
              </button>
            `).join('')}
          </div>
        ` : ''}
      </div>

      <!-- Details -->
      <div class="p-6 sm:p-8 flex flex-col justify-between space-y-5">
        <div>
          <div class="flex items-center gap-2 text-xs uppercase tracking-widest text-[#7A152E] font-bold">
            <span>${p.categoryName || p.category}</span>
            <span>•</span>
            <span class="text-[#717171]">SKU: ${p.sku}</span>
          </div>

          <h2 class="font-serif text-2xl font-bold text-[#111111] mt-1">${p.name}</h2>

          <div class="flex items-center gap-2 mt-2 text-xs font-sans text-[#717171]">
            <span class="font-bold text-[#7A152E]">Rated ${p.rating}</span>
            <span>•</span>
            <span>${p.reviewsCount} verified reviews</span>
          </div>

          <div class="flex items-baseline gap-3 mt-4">
            <span class="font-serif text-3xl font-bold text-[#7A152E]">${formatINR(p.price)}</span>
            ${p.mrp && p.mrp > p.price ? `
              <span class="text-sm text-[#717171] line-through">${formatINR(p.mrp)}</span>
              <span class="px-2 py-0.5 bg-[#7A152E] text-white text-xs font-bold rounded">${p.discount}</span>
            ` : ''}
          </div>

          <div class="mt-5">
            <label class="block text-xs uppercase tracking-wider font-semibold text-[#111111] mb-2">
              Metal Finish: <span class="text-[#7A152E] font-bold">${defaultMetal}</span>
            </label>
            <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl border border-[#7A152E]/30 bg-[#FDF2F4] text-[#7A152E] text-xs font-semibold">
              <span class="w-2 h-2 rounded-full bg-[#7A152E]"></span>
              <span>${defaultMetal}</span>
            </div>
          </div>

          ${isRing ? `
            <div class="mt-4">
              <div class="flex items-center justify-between mb-2">
                <label class="block text-xs uppercase tracking-wider font-semibold text-[#111111]">Select Ring Size:</label>
                <span class="text-xs font-bold text-[#7A152E]">Size 12</span>
              </div>
              <div class="flex flex-wrap gap-2">
                ${['10', '12', '14', '16', '18'].map(s => `
                  <button class="w-9 h-9 rounded-xl border text-xs font-bold transition-all cursor-pointer flex items-center justify-center border-[#E8E5DF] hover:border-[#7A152E] text-[#111111]">
                    ${s}
                  </button>
                `).join('')}
              </div>
            </div>
          ` : ''}
        </div>

        <div class="space-y-3 pt-4 border-t border-[#E8E5DF]">
          <div class="flex gap-3">
            <button onclick="window.addToCart(window.PRODUCTS.find(x => x.id === '${p.id}')); window.closeQuickViewModal();" class="flex-1 py-3.5 bg-[#7A152E] text-white font-serif text-xs uppercase tracking-widest font-bold rounded-xl hover:bg-[#590D1E] transition-all shadow-md flex items-center justify-center gap-2 cursor-pointer">
              <svg class="lucide lucide-shopping-bag w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"></path><path d="M3 6h18"></path><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
              <span>Add to Bag</span>
            </button>
            <button onclick="window.toggleWishlist('${p.id}')" class="p-3.5 rounded-xl border border-[#E8E5DF] hover:border-[#7A152E] text-[#111111] transition-all cursor-pointer">
              <svg class="lucide lucide-heart w-5 h-5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path></svg>
            </button>
          </div>
          <a href="product.html?id=${p.id}" class="w-full text-center text-xs uppercase tracking-widest font-semibold text-[#111111] hover:text-[#7A152E] transition-colors flex items-center justify-center gap-1.5 pt-1">
            <span>View Full Product Details &amp; Specs</span>
            <svg class="lucide lucide-arrow-right w-3.5 h-3.5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
          </a>
        </div>
      </div>
    `;

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  };

  window.closeQuickViewModal = function () {
    const modal = document.getElementById('quickview-modal-root');
    if (modal) modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  // Modals show/hide
  window.openCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer-root');
    if (drawer) {
      renderCartDrawer();
      drawer.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer-root');
    if (drawer) drawer.classList.add('hidden');
    document.body.style.overflow = '';
  };

  window.openWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer-root');
    if (drawer) {
      renderWishlistDrawer();
      drawer.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer-root');
    if (drawer) drawer.classList.add('hidden');
    document.body.style.overflow = '';
  };

  window.openBoutiqueModal = function () {
    const modal = document.getElementById('boutique-modal-root');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeBoutiqueModal = function () {
    const modal = document.getElementById('boutique-modal-root');
    if (modal) modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  window.openSearchModal = function () {
    const modal = document.getElementById('search-modal-root');
    if (modal) {
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      const input = document.getElementById('search-input');
      if (input) {
        input.focus();
        window.handleSearchInput(input.value || '');
      }
    }
  };

  window.closeSearchModal = function () {
    const modal = document.getElementById('search-modal-root');
    if (modal) modal.classList.add('hidden');
    document.body.style.overflow = '';
  };

  // Search logic
  let currentSearchCategory = 'all';

  window.setSearchFilterCategory = function (cat, btnEl) {
    currentSearchCategory = cat;
    document.querySelectorAll('.search-cat-pill').forEach(b => {
      b.className = 'search-cat-pill px-3 py-1 rounded-lg capitalize shrink-0 transition-all bg-[#FAF8F5] text-[#111111] border border-[#E8E5DF] hover:bg-[#7A152E]/10 cursor-pointer';
    });
    if (btnEl) {
      btnEl.className = 'search-cat-pill px-3 py-1 rounded-lg capitalize shrink-0 transition-all bg-[#7A152E] text-white font-bold shadow-sm cursor-pointer';
    }
    const input = document.getElementById('search-input');
    window.handleSearchInput(input ? input.value : '');
  };

  window.clearSearchInput = function () {
    const input = document.getElementById('search-input');
    if (input) {
      input.value = '';
      window.handleSearchInput('');
    }
  };

  window.handleSearchInput = function (query) {
    const resultsContainer = document.getElementById('search-modal-results');
    if (!resultsContainer || !window.PRODUCTS) return;

    const term = (query || '').toLowerCase().trim();
    let matches = window.PRODUCTS.filter(p => {
      const matchCat = currentSearchCategory === 'all' || p.category === currentSearchCategory;
      if (!matchCat) return false;
      if (!term) return true;
      return (
        p.name.toLowerCase().includes(term) ||
        (p.desc && p.desc.toLowerCase().includes(term)) ||
        (p.categoryName && p.categoryName.toLowerCase().includes(term)) ||
        (p.sku && p.sku.toLowerCase().includes(term))
      );
    });

    if (!term && currentSearchCategory === 'all') {
      matches = matches.slice(0, 6);
    }

    if (matches.length === 0) {
      resultsContainer.innerHTML = `
        <div class="py-12 text-center text-[#717171] space-y-2">
          <p class="font-serif text-lg text-[#111111]">No jewelry matches found</p>
          <p class="text-xs">Try searching for "Solitaire", "Bloom", "Tennis", or "Rings"</p>
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = matches.map(p => `
      <div onclick="window.location.href='product.html?id=${p.id}'; window.closeSearchModal();" class="py-3.5 flex items-center justify-between group cursor-pointer hover:bg-[#FAF8F5] -mx-3 px-3 rounded-xl transition-all">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-lg overflow-hidden bg-[#FAF8F5] border border-[#E8E5DF] shrink-0">
            <img src="${p.images[0]}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-110 transition-transform">
          </div>
          <div>
            <div class="font-serif text-sm font-semibold text-[#111111] group-hover:text-[#7A152E] transition-colors">${p.name}</div>
            <div class="flex items-center gap-2 mt-0.5 text-xs text-[#717171]">
              <span class="capitalize">${p.categoryName || p.category}</span>
              <span>•</span>
              <span class="text-[#7A152E] font-bold">Rated ${p.rating}</span>
              <span>•</span>
              <span class="text-[#111111] font-semibold">925 Silver</span>
            </div>
          </div>
        </div>
        <div class="text-right flex items-center gap-4">
          <div>
            <div class="font-serif text-sm font-bold text-[#7A152E]">${formatINR(p.price)}</div>
            ${p.mrp && p.mrp > p.price ? `<div class="text-[11px] text-[#717171] line-through">${formatINR(p.mrp)}</div>` : ''}
          </div>
          <div class="w-8 h-8 rounded-full bg-[#FAF8F5] border border-[#E8E5DF] flex items-center justify-center text-[#111111] group-hover:bg-[#7A152E] group-hover:text-white transition-all">
            <svg class="lucide lucide-arrow-up-right w-4 h-4" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M7 7h10v10"></path><path d="M7 17 17 7"></path></svg>
          </div>
        </div>
      </div>
    `).join('');
  };

  // Collections Dropdown Menu
  let isCollectionsMenuOpen = false;
  window.toggleCollectionsMenu = function () {
    isCollectionsMenuOpen = !isCollectionsMenuOpen;
    const overlay = document.getElementById('collections-dropdown-overlay');
    const panel = document.getElementById('collections-dropdown-panel');
    const chevron = document.getElementById('collections-chevron');

    if (isCollectionsMenuOpen) {
      if (overlay) {
        overlay.classList.remove('opacity-0', 'pointer-events-none', 'bg-stone-900/0', 'backdrop-blur-none');
        overlay.classList.add('opacity-100', 'pointer-events-auto', 'bg-stone-900/40', 'backdrop-blur-md');
      }
      if (panel) {
        panel.classList.remove('opacity-0', '-translate-y-6', 'scale-[0.99]', 'pointer-events-none', 'invisible', 'shadow-none');
        panel.classList.add('opacity-100', 'translate-y-0', 'scale-100', 'pointer-events-auto', 'visible', 'shadow-[0_30px_70px_-15px_rgba(0,0,0,0.25)]');
        const inner = panel.firstElementChild;
        if (inner) {
          inner.classList.remove('opacity-0', '-translate-y-3');
          inner.classList.add('opacity-100', 'translate-y-0');
        }
      }
      if (chevron) chevron.classList.add('rotate-180', 'text-[#7A152E]');
      document.body.style.overflow = 'hidden';
    } else {
      window.closeCollectionsMenu();
    }
  };

  window.closeCollectionsMenu = function () {
    isCollectionsMenuOpen = false;
    const overlay = document.getElementById('collections-dropdown-overlay');
    const panel = document.getElementById('collections-dropdown-panel');
    const chevron = document.getElementById('collections-chevron');

    if (overlay) {
      overlay.classList.add('opacity-0', 'pointer-events-none', 'bg-stone-900/0', 'backdrop-blur-none');
      overlay.classList.remove('opacity-100', 'pointer-events-auto', 'bg-stone-900/40', 'backdrop-blur-md');
    }
    if (panel) {
      panel.classList.add('opacity-0', '-translate-y-6', 'scale-[0.99]', 'pointer-events-none', 'invisible', 'shadow-none');
      panel.classList.remove('opacity-100', 'translate-y-0', 'scale-100', 'pointer-events-auto', 'visible', 'shadow-[0_30px_70px_-15px_rgba(0,0,0,0.25)]');
      const inner = panel.firstElementChild;
      if (inner) {
        inner.classList.add('opacity-0', '-translate-y-3');
        inner.classList.remove('opacity-100', 'translate-y-0');
      }
    }
    if (chevron) chevron.classList.remove('rotate-180', 'text-[#7A152E]');
    document.body.style.overflow = '';
  };

  // Close modals on Escape key
  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      window.closeCartDrawer();
      window.closeWishlistDrawer();
      window.closeSearchModal();
      window.closeBoutiqueModal();
      window.closeQuickViewModal();
      window.closeCollectionsMenu();
    }
  });

  // Revolving announcement ticker
  const TICKER_MESSAGES = [
    '100% Certified BIS 925 Hallmarked Pure Silver Jewelry',
    'Free Insured Express Delivery Across India • 10% Off with Code: SOULY10',
    'Complimentary Luxury Velvet Keepsake Box with Authenticity Certificate',
    '15-Day Hassle-Free Returns & Lifetime Replating Guarantee'
  ];
  let tickerIdx = 0;
  setInterval(() => {
    const el = document.getElementById('announcement-ticker');
    if (!el) return;
    el.style.opacity = '0';
    setTimeout(() => {
      tickerIdx = (tickerIdx + 1) % TICKER_MESSAGES.length;
      el.textContent = TICKER_MESSAGES[tickerIdx];
      el.style.opacity = '1';
    }, 300);
  }, 3800);

  // Initial setup on DOM ready
  document.addEventListener('DOMContentLoaded', function () {
    updateBadges();

    // Check if on Checkout Page
    if (window.location.pathname.includes('checkout.html')) {
      initCheckoutPage();
    }

    // Check if on Product Detail Page
    if (window.location.pathname.includes('product.html')) {
      initProductDetailPage();
    }
  });

  // Product Detail Page initialization
  function initProductDetailPage() {
    const params = new URLSearchParams(window.location.search);
    const prodId = params.get('id') || 'accent-circle-925-silver-necklace';
    const product = findProduct(prodId);
    if (!product) return;

    // Update document title
    document.title = `${product.name} | Solystra Jewels Atelier`;

    // Swap main images when clicking thumbnails
    const thumbnails = document.querySelectorAll('button img[alt="Angle"], button img[alt="Product Angle"]');
    const mainImg = document.querySelector('img[alt="' + product.name + '"]') || document.querySelector('main img');

    thumbnails.forEach(thumb => {
      thumb.parentElement.addEventListener('click', function () {
        if (mainImg) mainImg.src = thumb.src;
        thumbnails.forEach(t => t.parentElement.classList.remove('border-[#7A152E]', 'shadow-sm'));
        thumb.parentElement.classList.add('border-[#7A152E]', 'shadow-sm');
      });
    });

    // Pincode checker
    const pinBtn = document.querySelector('button:has(svg.lucide-truck)');
    const pinInput = document.querySelector('input[placeholder*="pincode"], input[placeholder*="Pincode"]');
    if (pinBtn && pinInput) {
      pinBtn.addEventListener('click', function (e) {
        e.preventDefault();
        const pin = pinInput.value.trim();
        if (pin.length === 6 && /^\d+$/.test(pin)) {
          window.showToast('Delivery Available', `BlueDart Express reaches ${pin} in 2-3 business days.`);
        } else {
          window.showToast('Invalid Pincode', 'Please enter a valid 6-digit Indian PIN code.', 'info');
        }
      });
    }

    // Add to Bag CTA
    const addBtns = document.querySelectorAll('button');
    addBtns.forEach(b => {
      const txt = b.get_text ? b.get_text() : b.textContent;
      if (txt.includes('Add to Bag')) {
        b.onclick = function () {
          window.addToCart(product);
        };
      } else if (txt.includes('Buy Now')) {
        b.onclick = function () {
          window.addToCart(product);
          window.location.href = 'checkout.html';
        };
      }
    });
  }

  // Checkout Page initialization
  function initCheckoutPage() {
    const cart = getCart();
    const subtotal = cart.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    const promo = getAppliedPromo();
    let discount = 0;
    if (promo === 'ROYAL10' || promo === 'SOULY10') {
      discount = Math.round(subtotal * 0.10);
    } else if (promo === 'VAULT500') {
      discount = Math.min(500, subtotal);
    }
    const total = Math.max(0, subtotal - discount);

    // Wire place order button
    const placeBtn = document.querySelector('button:has(svg.lucide-lock)');
    if (placeBtn) {
      placeBtn.onclick = function (e) {
        e.preventDefault();
        const orderId = 'SLY-' + Math.floor(100000 + Math.random() * 900000);
        localStorage.removeItem(CART_KEY);
        updateBadges();

        alert(`✨ Luxury Order Confirmed!\n\nOrder ID: ${orderId}\nTotal: ${formatINR(total)}\n\nThank you for choosing Solystra Jewels Atelier.\nA confirmation SMS & Email have been dispatched along with your insured BlueDart tracking number.`);
        window.location.href = 'index.html';
      };
    }
  }


  // Hero Carousel Slider Controller
  let currentHeroSlide = 2; // Default: Modern Classics
  window.setHeroSlide = function (idx) {
    currentHeroSlide = idx;
    for (let i = 0; i < 4; i++) {
      const slide = document.getElementById(`hero-slide-${i}`);
      const dot = document.getElementById(`hero-dot-${i}`);
      if (slide) {
        if (i === idx) {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-100 z-10';
        } else {
          slide.className = 'absolute inset-0 transition-opacity duration-700 ease-in-out opacity-0 z-0 pointer-events-none';
        }
      }
      if (dot) {
        if (i === idx) {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-7 bg-[#C5A059] shadow-xs';
        } else {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-2 bg-white/40 hover:bg-white/70';
        }
      }
    }
  };

  setInterval(() => {
    const next = (currentHeroSlide + 1) % 4;
    window.setHeroSlide(next);
  }, 5500);


  /* ==========================================================================
     Top Collections Coverflow Slider Engine (Exact 1:1 React Behavior)
     - Center card enlarged (scale-105, opacity-100, gold ring, deep ruby shadow)
     - Side cards tapered down (scale-80, opacity-55, contrast-95)
     - Initial load centered on set 2 (card index 7)
     - Dynamic 60fps center tracking on scroll
     - Seamless infinite circular boundary wrap
     - Click card to center
     - Silky smooth mouse drag-to-scroll with kinetic momentum
     ========================================================================== */
  function initTopCollectionsCoverflow() {
    const el = document.getElementById('top-collections-scroll');
    if (!el) return;

    const cards = el.querySelectorAll('[data-collection-card]');
    if (!cards.length) return;

    let activeIndex = 7;
    let isTicking = false;
    let isDragging = false;
    let startX = 0;
    let scrollLeftStart = 0;
    let hasMoved = false;

    // Center classes
    const centerClasses = ['scale-100', 'sm:scale-105', 'opacity-100', 'z-20', 'shadow-[0_16px_40px_rgba(122,21,46,0.32)]', 'ring-1', 'ring-[#D4AF37]/40'];
    const sideClasses = ['scale-[0.76]', 'sm:scale-[0.80]', 'opacity-55', 'hover:opacity-75', 'z-0', 'shadow-sm', 'filter', 'contrast-95'];

    function applyCardClasses(targetIdx) {
      cards.forEach((card, i) => {
        if (i === targetIdx) {
          sideClasses.forEach(c => card.classList.remove(c));
          centerClasses.forEach(c => card.classList.add(c));
        } else {
          centerClasses.forEach(c => card.classList.remove(c));
          sideClasses.forEach(c => card.classList.add(c));
        }
      });
    }

    function centerCardByIndex(idx, smooth = false) {
      const card = cards[idx];
      if (!card) return;
      const targetScroll = card.offsetLeft - (el.clientWidth - card.clientWidth) / 2;
      el.scrollTo({ left: targetScroll, behavior: smooth ? 'smooth' : 'auto' });
      applyCardClasses(idx);
    }

    // Set initial position centered at card 7
    function initPosition() {
      centerCardByIndex(7, false);
    }

    initPosition();
    setTimeout(initPosition, 100);
    setTimeout(initPosition, 400);
    window.addEventListener('resize', initPosition);

    // Scroll listener with RAF throttle
    el.addEventListener('scroll', function () {
      if (isTicking) return;
      isTicking = true;

      requestAnimationFrame(function () {
        const containerCenter = el.scrollLeft + el.clientWidth / 2;
        let closestIdx = activeIndex;
        let minDiff = Infinity;

        cards.forEach((card, i) => {
          const cardCenter = card.offsetLeft + card.clientWidth / 2;
          const diff = Math.abs(containerCenter - cardCenter);
          if (diff < minDiff) {
            minDiff = diff;
            closestIdx = i;
          }
        });

        if (closestIdx !== activeIndex) {
          activeIndex = closestIdx;
          applyCardClasses(activeIndex);
        }

        // Seamless boundary wrap
        const singleSet = el.scrollWidth / 3;
        if (singleSet > 50) {
          if (el.scrollLeft < 30) {
            el.scrollLeft += singleSet;
          } else if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          }
        }

        isTicking = false;
      });
    }, { passive: true });

    // Click handler: if side card, scroll it to center; if center card, navigate
    cards.forEach((card, idx) => {
      card.addEventListener('click', function (e) {
        if (hasMoved) return; // Ignore drag clicks
        if (idx !== activeIndex) {
          e.preventDefault();
          centerCardByIndex(idx, true);
        } else {
          window.location.href = 'products.html';
        }
      });
    });

    // Silky Mouse Drag-to-Scroll
    el.addEventListener('mousedown', function (e) {
      if (e.button !== 0) return;
      isDragging = true;
      hasMoved = false;
      startX = e.pageX - el.offsetLeft;
      scrollLeftStart = el.scrollLeft;
      el.style.scrollBehavior = 'auto';
      el.style.cursor = 'grabbing';
      el.style.userSelect = 'none';
    });

    window.addEventListener('mousemove', function (e) {
      if (!isDragging) return;
      const x = e.pageX - el.offsetLeft;
      const walk = (x - startX);
      if (Math.abs(walk) > 4) {
        hasMoved = true;
      }
      el.scrollLeft = scrollLeftStart - walk;
    });

    window.addEventListener('mouseup', function () {
      if (!isDragging) return;
      isDragging = false;
      el.style.cursor = 'grab';
      el.style.userSelect = '';
      setTimeout(() => { hasMoved = false; }, 50);
    });
  }

  /* ==========================================================================
     Motion Reels Video Engine (Pure Radiance Captured)
     - Autoplay all videos (muted, playsinline, loop)
     - Continuous infinite marquee glide ticker (requestAnimationFrame)
     - Boundary wrapping without interruption
     - Pause on hover, pause on drag/touch
     - Mouse drag-to-scroll with kinetic momentum
     - Add to cart integration on reels
     ========================================================================== */
  function initMotionReelsVideos() {
    const el = document.getElementById('video-reels-scroll');
    if (!el) return;

    // Ensure all videos play continuously
    const videos = el.querySelectorAll('video');
    videos.forEach(v => {
      v.muted = true;
      v.playsInline = true;
      v.loop = true;
      v.setAttribute('muted', '');
      v.setAttribute('playsinline', '');
      v.setAttribute('autoplay', '');
      v.setAttribute('loop', '');
      
      const playPromise = v.play();
      if (playPromise !== undefined) {
        playPromise.catch(() => {
          // Retry on first user interaction
          const retryPlay = () => {
            v.play().catch(() => {});
            document.removeEventListener('click', retryPlay);
            document.removeEventListener('touchstart', retryPlay);
          };
          document.addEventListener('click', retryPlay, { once: true });
          document.addEventListener('touchstart', retryPlay, { once: true });
        });
      }
    });

    // Center video reel container initially to set 2 (middle set)
    function initVideoPos() {
      const singleSet = el.scrollWidth / 3;
      if (singleSet > 50 && (el.scrollLeft < 50 || el.scrollLeft >= singleSet * 2.2)) {
        el.scrollLeft = singleSet;
      }
    }
    initVideoPos();
    setTimeout(initVideoPos, 200);
    setTimeout(initVideoPos, 600);

    // Continuous Infinite Marquee Glide
    let animId = null;
    let isHoverPaused = false;
    let isInteracting = false;
    const scrollSpeed = 0.75; // ~45px per second luxury glide

    function step() {
      if (!isHoverPaused && !isInteracting) {
        el.scrollLeft += scrollSpeed;
        const singleSet = el.scrollWidth / 3;
        if (singleSet > 50) {
          if (el.scrollLeft >= singleSet * 2) {
            el.scrollLeft -= singleSet;
          } else if (el.scrollLeft <= 10) {
            el.scrollLeft += singleSet;
          }
        }
      }
      animId = requestAnimationFrame(step);
    }
    animId = requestAnimationFrame(step);

    // Pause glide on hover
    el.addEventListener('mouseenter', () => { isHoverPaused = true; });
    el.addEventListener('mouseleave', () => { isHoverPaused = false; });

    // Touch interaction
    el.addEventListener('touchstart', () => { isInteracting = true; }, { passive: true });
    el.addEventListener('touchend', () => {
      setTimeout(() => { isInteracting = false; }, 400);
    }, { passive: true });

    // Mouse drag-to-scroll on video container
    let isDragging = false;
    let startX = 0;
    let scrollStart = 0;

    el.addEventListener('mousedown', function (e) {
      if (e.button !== 0) return;
      isDragging = true;
      isInteracting = true;
      startX = e.pageX - el.offsetLeft;
      scrollStart = el.scrollLeft;
      el.style.scrollBehavior = 'auto';
      el.style.cursor = 'grabbing';
      el.style.userSelect = 'none';
    });

    window.addEventListener('mousemove', function (e) {
      if (!isDragging) return;
      const x = e.pageX - el.offsetLeft;
      const walk = (x - startX);
      el.scrollLeft = scrollStart - walk;

      const singleSet = el.scrollWidth / 3;
      if (singleSet > 50) {
        if (el.scrollLeft >= singleSet * 2) el.scrollLeft -= singleSet;
        else if (el.scrollLeft <= 10) el.scrollLeft += singleSet;
      }
    });

    window.addEventListener('mouseup', function () {
      if (!isDragging) return;
      isDragging = false;
      el.style.cursor = 'grab';
      el.style.userSelect = '';
      setTimeout(() => { isInteracting = false; }, 300);
    });

    // Wire up Add to Cart buttons inside Video Reel cards
    const reelButtons = el.querySelectorAll('button');
    reelButtons.forEach((btn, i) => {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        e.preventDefault();
        // Add popular product
        if (window.PRODUCTS && window.PRODUCTS.length > 0) {
          const product = window.PRODUCTS[i % window.PRODUCTS.length];
          window.addToCart(product);
        } else {
          window.showToast('Added to Shopping Bag', 'Artisan piece reserved in your private bag.');
          window.openCartDrawer();
        }
      });
    });
  }

  /* ==========================================================================
     Shop the Complete Look: Multi-Combo Auto-Slider & Interactive Hotspots
     ========================================================================== */
  const COMBOS_DATA = [
    {
      id: 'combo-1',
      name: 'Amethyst Floral Blossom Set',
      tag: 'ROSE GOLD VERMEIL',
      comboText: 'Combo 01 / 03',
      img: 'solystra_assets/banners/banner_blush_tones_pc.jpg',
      title: 'Amethyst Bloom Floral Set',
      desc: 'Handcrafted floral blossom necklace paired with matching petal drop earrings.',
      item1: { name: 'Amethyst Bloom Floral Necklace', metal: 'Rose Gold Vermeil • Handcrafted Setting', price: '₹9,585', mrp: '₹11,981' },
      item2: { name: 'Blossom Petal Drop Earrings', metal: 'Rose Gold Vermeil • Double-Micron Rhodium', price: '₹2,499', mrp: '₹3,499' },
      bundlePrice: '₹12,084',
      originalPrice: '₹15,480',
      savings: '₹3,396'
    },
    {
      id: 'combo-2',
      name: 'Classic Solitaire Set',
      tag: 'PURE 925 STERLING SILVER',
      comboText: 'Combo 02 / 03',
      img: 'solystra_assets/banners/banner_pc_1.jpg',
      title: 'Classic Solitaire Atelier Set',
      desc: 'Austrian round-brilliant solitaire pendant paired with sparkling pavé huggie earrings.',
      item1: { name: 'Radiant Austrian Solitaire Pendant', metal: 'Pure 925 Silver • 57-Facet Austrian Crystal', price: '₹3,299', mrp: '₹4,499' },
      item2: { name: 'Solitaire Pavé Huggies', metal: 'Pure 925 Silver • Precision Prong Setting', price: '₹2,199', mrp: '₹2,999' },
      bundlePrice: '₹5,498',
      originalPrice: '₹7,498',
      savings: '₹2,000'
    },
    {
      id: 'combo-3',
      name: 'Imperial Chandelier Bridal Set',
      tag: '18K GOLD VERMEIL',
      comboText: 'Combo 03 / 03',
      img: 'solystra_assets/banners/banner_pc_2.jpg',
      title: 'Imperial Tennis & Chandelier Suite',
      desc: 'Graduated tennis choker necklace harmonized with multi-tiered chandelier earrings.',
      item1: { name: 'Graduated Tennis Choker', metal: '18K Gold Vermeil • Articulated Settings', price: '₹5,499', mrp: '₹7,999' },
      item2: { name: 'Imperial Chandelier Drops', metal: 'Pure 925 Silver • Multi-Tier Drops', price: '₹3,499', mrp: '₹4,999' },
      bundlePrice: '₹8,998',
      originalPrice: '₹12,998',
      savings: '₹4,000'
    }
  ];

  let currentComboIdx = 1;
  function initStylingCombos() {
    const comboSection = document.querySelector('section:has(h2:contains("Shop the Complete Look"))') ||
      Array.from(document.querySelectorAll('section')).find(s => s.textContent.includes('Shop the Complete Look'));
    if (!comboSection) return;

    const countText = comboSection.querySelector('.font-mono');
    const dots = comboSection.querySelectorAll('.flex.items-center.gap-1\.5 button');
    const mainImg = comboSection.querySelector('img[alt*="Set"]');

    function renderCombo(idx) {
      currentComboIdx = idx;
      const data = COMBOS_DATA[idx];
      if (!data) return;

      if (countText) countText.textContent = data.comboText;

      dots.forEach((dot, dIdx) => {
        if (dIdx === idx) {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-5 bg-[#7A152E]';
        } else {
          dot.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-1.5 bg-stone-300 hover:bg-stone-400';
        }
      });

      if (mainImg) {
        mainImg.src = data.img;
        mainImg.alt = data.name;
      }
    }

    dots.forEach((dot, idx) => {
      dot.addEventListener('click', () => renderCombo(idx));
    });

    setInterval(() => {
      const next = (currentComboIdx + 1) % COMBOS_DATA.length;
      renderCombo(next);
    }, 5500);
  }

  /* ==========================================================================
     Newly Launched & Product Carousels Loop & Drag Engine
     ========================================================================== */
  function initProductCarousels() {
    const carousels = document.querySelectorAll('.overflow-x-auto');
    carousels.forEach(el => {
      if (el.id === 'top-collections-scroll' || el.id === 'video-reels-scroll') return;

      // Add mouse drag scrolling to horizontal carousels
      let isDown = false;
      let startX = 0;
      let scrollLeft = 0;

      el.addEventListener('mousedown', (e) => {
        if (e.button !== 0) return;
        isDown = true;
        startX = e.pageX - el.offsetLeft;
        scrollLeft = el.scrollLeft;
        el.style.scrollBehavior = 'auto';
      });

      window.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        const x = e.pageX - el.offsetLeft;
        const walk = (x - startX);
        el.scrollLeft = scrollLeft - walk;
      });

      window.addEventListener('mouseup', () => {
        if (!isDown) return;
        isDown = false;
      });
    });
  }

  // Hook into DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(initTopCollectionsCoverflow, 50);
    setTimeout(initMotionReelsVideos, 100);
    setTimeout(initStylingCombos, 150);
    setTimeout(initProductCarousels, 200);
  });

})();
