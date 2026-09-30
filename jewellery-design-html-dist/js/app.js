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
        image: (product.images && product.images[0]) || 'solystra_assets/categories/zavya_style/necklaces.webp',
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

  window.removeCartItem = function (index, btn) {
    const cart = getCart();
    if (!cart[index]) return;
    const row = btn ? btn.closest('.py-4') : null;
    if (row) {
      row.style.transition = 'all 240ms cubic-bezier(0.16, 1, 0.3, 1)';
      row.style.opacity = '0';
      row.style.transform = 'translateX(24px)';
      setTimeout(() => {
        cart.splice(index, 1);
        saveCart(cart);
      }, 200);
      return;
    }
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
          <button onclick="window.removeCartItem(${idx}, this)" aria-label="Remove item" class="text-stone-400 hover:text-red-600 p-1 transition-colors cursor-pointer">
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
    void modal.offsetWidth;
    requestAnimationFrame(() => {
      modal.classList.add('is-open');
    });
    document.body.style.overflow = 'hidden';
  };

  // Modals & Drawers Smooth In-Out Animations Controller
  let cartCloseTimer = null;
  let wishlistCloseTimer = null;
  let quickviewCloseTimer = null;

  window.openCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer-root');
    if (drawer) {
      if (cartCloseTimer) {
        clearTimeout(cartCloseTimer);
        cartCloseTimer = null;
      }
      // If wishlist drawer was open, close it
      const wishDrawer = document.getElementById('wishlist-drawer-root');
      if (wishDrawer && wishDrawer.classList.contains('is-open')) {
        window.closeWishlistDrawer();
      }

      renderCartDrawer();
      drawer.classList.remove('hidden');
      void drawer.offsetWidth; // Force reflow to establish initial translateX(100%) and opacity 0
      requestAnimationFrame(() => {
        drawer.classList.add('is-open');
      });
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer-root');
    if (drawer) {
      if (cartCloseTimer) {
        clearTimeout(cartCloseTimer);
        cartCloseTimer = null;
      }
      drawer.classList.remove('is-open');
      cartCloseTimer = setTimeout(() => {
        drawer.classList.add('hidden');
        cartCloseTimer = null;
        if (!document.querySelector('.drawer-root.is-open, .quickview-root.is-open, #boutique-modal-root:not(.hidden), #search-modal-root:not(.hidden)')) {
          document.body.style.overflow = '';
        }
      }, 380);
    }
  };

  window.openWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer-root');
    if (drawer) {
      if (wishlistCloseTimer) {
        clearTimeout(wishlistCloseTimer);
        wishlistCloseTimer = null;
      }
      // If cart drawer was open, close it
      const cartDrawer = document.getElementById('cart-drawer-root');
      if (cartDrawer && cartDrawer.classList.contains('is-open')) {
        window.closeCartDrawer();
      }

      renderWishlistDrawer();
      drawer.classList.remove('hidden');
      void drawer.offsetWidth;
      requestAnimationFrame(() => {
        drawer.classList.add('is-open');
      });
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer-root');
    if (drawer) {
      if (wishlistCloseTimer) {
        clearTimeout(wishlistCloseTimer);
        wishlistCloseTimer = null;
      }
      drawer.classList.remove('is-open');
      wishlistCloseTimer = setTimeout(() => {
        drawer.classList.add('hidden');
        wishlistCloseTimer = null;
        if (!document.querySelector('.drawer-root.is-open, .quickview-root.is-open, #boutique-modal-root:not(.hidden), #search-modal-root:not(.hidden)')) {
          document.body.style.overflow = '';
        }
      }, 380);
    }
  };

  window.closeQuickViewModal = function () {
    const modal = document.getElementById('quickview-modal-root');
    if (modal) {
      modal.classList.remove('is-open');
      quickviewCloseTimer = setTimeout(() => {
        modal.classList.add('hidden');
        quickviewCloseTimer = null;
        if (!document.querySelector('.drawer-root.is-open, .quickview-root.is-open, #boutique-modal-root:not(.hidden), #search-modal-root:not(.hidden)')) {
          document.body.style.overflow = '';
        }
      }, 280);
    }
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
    if (!document.querySelector('.drawer-root.is-open, .quickview-root.is-open, #search-modal-root:not(.hidden)')) {
      document.body.style.overflow = '';
    }
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
    if (!document.querySelector('.drawer-root.is-open, .quickview-root.is-open, #boutique-modal-root:not(.hidden)')) {
      document.body.style.overflow = '';
    }
  };

  // Global Escape key listener for smooth closing
  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.keyCode === 27) {
      const cartDrawer = document.getElementById('cart-drawer-root');
      if (cartDrawer && cartDrawer.classList.contains('is-open')) {
        window.closeCartDrawer();
        return;
      }
      const wishlistDrawer = document.getElementById('wishlist-drawer-root');
      if (wishlistDrawer && wishlistDrawer.classList.contains('is-open')) {
        window.closeWishlistDrawer();
        return;
      }
      const quickviewModal = document.getElementById('quickview-modal-root');
      if (quickviewModal && quickviewModal.classList.contains('is-open')) {
        window.closeQuickViewModal();
        return;
      }
      const boutiqueModal = document.getElementById('boutique-modal-root');
      if (boutiqueModal && !boutiqueModal.classList.contains('hidden')) {
        window.closeBoutiqueModal();
        return;
      }
      const searchModal = document.getElementById('search-modal-root');
      if (searchModal && !searchModal.classList.contains('hidden')) {
        window.closeSearchModal();
        return;
      }
    }
  });

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

  // Initial setup on DOM ready or immediate if already loaded
  function runPageInitializers() {
    updateBadges();

    // Check if on Checkout Page
    if (window.location.pathname.includes('checkout.html')) {
      initCheckoutPage();
    }

    // Check if on Catalog Page
    if (window.location.pathname.includes('products.html')) {
      initProductsPage();
    }

    // Check if on Product Detail Page
    if (window.location.pathname.includes('product.html')) {
      initProductDetailPage();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runPageInitializers);
  } else {
    runPageInitializers();
  }

  // Product Detail Page initialization
    // Product Detail Page initialization
  window.initProductDetailPage = initProductDetailPage;
  function initProductDetailPage() {
    const params = new URLSearchParams(window.location.search);
    const prodId = params.get('id');
    let product = null;

    if (prodId && window.PRODUCTS && window.PRODUCTS.length > 0) {
      product = window.PRODUCTS.find(p => p.id === prodId || p.id === prodId.toLowerCase().trim());
      if (!product) {
        product = window.PRODUCTS.find(p => p.name.toLowerCase().includes(prodId.toLowerCase()) || prodId.toLowerCase().includes(p.name.toLowerCase()));
      }
    }
    if (!product && window.PRODUCTS && window.PRODUCTS.length > 0) {
      product = window.PRODUCTS[0];
    }
    if (!product) return;

    let selectedMetal = (product.metals && product.metals[0])
      ? product.metals[0]
      : (product.metalType === 'gold' ? '18K Gold Vermeil' : product.metalType === 'rose' ? '18K Rose Gold Finish' : 'Pure 925 Silver');

    // 1. Update Document Title
    document.title = `${product.name} | Solystra Jewels Atelier`;

    // 2. Breadcrumb
    const crumbCat = document.getElementById('pdp-crumb-cat') || document.querySelector('nav[class*="border-b"] a.capitalize');
    if (crumbCat) {
      crumbCat.textContent = product.categoryName || 'Fine Jewelry';
      crumbCat.href = `products.html?category=${product.category || 'all'}`;
    }
    const crumbTitle = document.getElementById('pdp-crumb-title') || document.querySelector('nav[class*="border-b"] span.truncate');
    if (crumbTitle) crumbTitle.textContent = product.name;

    // 3. Main Product Image & Badge
    const mainImg = document.getElementById('pdp-main-img') || document.querySelector('.lg\\:col-span-7 img[draggable="false"]') || document.querySelector('.lg\\:col-span-7 img');
    let currentImageIndex = 0;
    const productImages = (product.images && product.images.length > 0) ? product.images : [mainImg ? mainImg.src : ''];

    if (mainImg) {
      mainImg.src = productImages[0];
      mainImg.alt = product.name;
      mainImg.onerror = function () {
        if (!this.dataset.fallbackTried) {
          this.dataset.fallbackTried = '1';
          if (this.src.endsWith('.webp')) {
            this.src = this.src.slice(0, -5) + '.png';
          } else if (this.src.endsWith('.png')) {
            this.src = this.src.slice(0, -4) + '.jpg';
          } else if (this.src.endsWith('.jpg')) {
            this.src = this.src.slice(0, -4) + '.webp';
          } else if (!this.src.startsWith('/') && !this.src.startsWith('http')) {
            this.src = '/' + this.src;
          }
        }
      };
      mainImg.classList.add('cursor-zoom-in');
      mainImg.onclick = function () {
        window.openImageLightbox(mainImg.src, product);
      };
    }
    const badgeEl = document.getElementById('pdp-badge') || document.querySelector('.lg\\:col-span-7 span.bg-\\[\\#7A152E\\]');
    if (badgeEl) {
      badgeEl.textContent = product.badge || (product.isNew ? 'New Arrival' : 'Bestseller');
    }

    // 4. Thumbnails Gallery
    const thumbsContainer = document.getElementById('pdp-thumbnails') || document.querySelector('.lg\\:col-span-7 .flex.sm\\:flex-col');
    const bottomDots = document.querySelectorAll('.aspect-square.w-full .absolute.bottom-3 span');

    function setActiveImage(idx) {
      if (idx < 0) idx = productImages.length - 1;
      if (idx >= productImages.length) idx = 0;
      currentImageIndex = idx;

      if (mainImg) {
        mainImg.style.opacity = '0.5';
        setTimeout(() => {
          mainImg.dataset.fallbackTried = '';
          mainImg.src = productImages[currentImageIndex];
          mainImg.style.opacity = '1';
        }, 120);
      }

      if (thumbsContainer) {
        thumbsContainer.querySelectorAll('button').forEach((b, i) => {
          if (i === currentImageIndex) {
            b.className = 'relative w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden bg-white border transition-all shrink-0 cursor-pointer border-[#7A152E] ring-2 ring-[#7A152E]/20 shadow-xs';
          } else {
            b.className = 'relative w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden bg-white border transition-all shrink-0 cursor-pointer border-stone-200 opacity-75 hover:opacity-100 hover:border-stone-400';
          }
        });
      }

      if (bottomDots && bottomDots.length > 0) {
        bottomDots.forEach((dot, i) => {
          if (i === currentImageIndex) {
            dot.className = 'h-1.5 rounded-full transition-all duration-300 w-5 bg-[#7A152E]';
          } else {
            dot.className = 'h-1.5 rounded-full transition-all duration-300 w-1.5 bg-black/25';
          }
        });
      }
    }

    if (thumbsContainer && productImages.length > 0) {
      thumbsContainer.innerHTML = '';
      productImages.forEach((imgSrc, idx) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.setAttribute('aria-label', `View angle ${idx + 1}`);
        btn.className = `relative w-16 h-16 sm:w-20 sm:h-20 rounded-xl overflow-hidden bg-white border transition-all shrink-0 cursor-pointer ${idx === 0 ? 'border-[#7A152E] ring-2 ring-[#7A152E]/20 shadow-xs' : 'border-stone-200 opacity-75 hover:opacity-100 hover:border-stone-400'}`;
        btn.innerHTML = `<img src="${imgSrc}" alt="${product.name} angle ${idx + 1}" onerror="if(!this.dataset.fallbackTried){this.dataset.fallbackTried='1';if(this.src.endsWith('.webp')){this.src=this.src.slice(0,-5)+'.png';}else if(this.src.endsWith('.png')){this.src=this.src.slice(0,-4)+'.jpg';}}" class="w-full h-full object-cover block" />`;
        btn.onclick = function () {
          setActiveImage(idx);
        };
        thumbsContainer.appendChild(btn);
      });
    }

    // Touch Swipe & Mouse Drag on Main Image
    const mainImgWrapper = document.querySelector('.aspect-square.w-full') || (mainImg ? mainImg.parentElement : null);
    if (mainImgWrapper) {
      let touchStartX = 0;
      let touchStartY = 0;
      let isDragging = false;
      let mouseStartX = 0;

      mainImgWrapper.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }, { passive: true });

      mainImgWrapper.addEventListener('touchend', (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        const diffX = touchEndX - touchStartX;
        const diffY = touchEndY - touchStartY;

        // Horizontal swipe detected
        if (Math.abs(diffX) > 40 && Math.abs(diffX) > Math.abs(diffY)) {
          if (diffX < 0) {
            setActiveImage(currentImageIndex + 1); // Next
          } else {
            setActiveImage(currentImageIndex - 1); // Prev
          }
        }
      }, { passive: true });

      mainImgWrapper.addEventListener('mousedown', (e) => {
        isDragging = true;
        mouseStartX = e.clientX;
      });

      window.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        const diffX = e.clientX - mouseStartX;
        if (Math.abs(diffX) > 50) {
          if (diffX < 0) {
            setActiveImage(currentImageIndex + 1);
          } else {
            setActiveImage(currentImageIndex - 1);
          }
        }
      });
    }

    // Enlarge Magnifier Button
    const enlargeBtn = document.querySelector('button[aria-label="Enlarge Image"]');
    if (enlargeBtn) {
      enlargeBtn.onclick = function (e) {
        e.stopPropagation();
        window.openImageLightbox(mainImg ? mainImg.src : productImages[0], product);
      };
    }

    // 5. Title, Subtitle, Price, MRP, Discount
    const titleEl = document.getElementById('pdp-title') || document.querySelector('h1');
    if (titleEl) titleEl.textContent = product.name;

    const subtitleEl = document.getElementById('pdp-subtitle') || (titleEl ? titleEl.nextElementSibling : null);
    if (subtitleEl && subtitleEl.tagName === 'P') {
      subtitleEl.textContent = `Made with ${selectedMetal}`;
    }

    const priceEl = document.getElementById('pdp-price') || document.querySelector('.lg\\:col-span-5 .text-3xl');
    if (priceEl) priceEl.textContent = `₹${product.price.toLocaleString('en-IN')}`;

    const discountEl = document.getElementById('pdp-discount') || document.querySelector('.lg\\:col-span-5 span[class*="text-[#D11A46]"]');
    if (discountEl) discountEl.textContent = product.discount || '20% OFF';

    const mrpEl = document.getElementById('pdp-mrp') || document.querySelector('.lg\\:col-span-5 .line-through');
    if (mrpEl) {
      mrpEl.textContent = product.mrp ? `MRP ₹${product.mrp.toLocaleString('en-IN')}` : '';
    }

    // 6. Metal Variants Selector
    let metalsBox = document.getElementById('pdp-metals-selector');
    if (!metalsBox && titleEl && titleEl.parentElement) {
      metalsBox = document.createElement('div');
      metalsBox.id = 'pdp-metals-selector';
      metalsBox.className = 'pt-2 pb-1 space-y-2';
      const availableMetals = (product.metals && product.metals.length > 0)
        ? product.metals
        : ['Pure 925 Silver', '18K Gold Vermeil', '18K Rose Gold Finish'];
      
      metalsBox.innerHTML = `
        <div class="flex items-center justify-between text-xs">
          <span class="text-stone-600 font-medium">Selected Finish: <strong id="pdp-selected-metal-name" class="text-stone-900 font-semibold">${selectedMetal}</strong></span>
          <span class="text-[11px] text-[#7A152E] font-medium">BIS 925 Hallmark</span>
        </div>
        <div id="pdp-metal-pills" class="flex flex-wrap gap-2"></div>
      `;
      titleEl.parentElement.insertAdjacentElement('afterend', metalsBox);

      const pillsContainer = metalsBox.querySelector('#pdp-metal-pills');
      availableMetals.forEach(m => {
        const pillBtn = document.createElement('button');
        pillBtn.type = 'button';
        const isSel = m.toLowerCase().includes(selectedMetal.toLowerCase()) || selectedMetal.toLowerCase().includes(m.toLowerCase());
        pillBtn.className = `px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all cursor-pointer ${isSel ? 'bg-[#7A152E] text-white border-[#7A152E] shadow-xs' : 'bg-white text-stone-700 border-[#EAE4DC] hover:border-[#7A152E]/40'}`;
        pillBtn.textContent = m;
        pillBtn.onclick = function () {
          selectedMetal = m;
          const metalName = document.getElementById('pdp-selected-metal-name');
          if (metalName) metalName.textContent = m;
          if (subtitleEl) subtitleEl.textContent = `Made with ${m}`;
          pillsContainer.querySelectorAll('button').forEach(b => {
            b.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all cursor-pointer bg-white text-stone-700 border-[#EAE4DC] hover:border-[#7A152E]/40';
          });
          pillBtn.className = 'px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all cursor-pointer bg-[#7A152E] text-white border-[#7A152E] shadow-xs';
          window.showToast('Finish Selected', `Atelier finish updated to ${m}`);
        };
        pillsContainer.appendChild(pillBtn);
      });
    }

    // 7. Add to Bag & Buy Now Buttons
    const addBtn = document.getElementById('pdp-add-btn') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('ADD TO CART') || b.textContent.includes('Add to Bag'));
    if (addBtn) {
      addBtn.onclick = function () {
        window.addToCart(product, selectedMetal);
      };
    }
    const buyBtn = document.getElementById('pdp-buy-btn') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('BUY NOW'));
    if (buyBtn) {
      buyBtn.onclick = function () {
        window.addToCart(product, selectedMetal);
        window.location.href = 'checkout.html';
      };
    }

    // 8. Wishlist Toggle Buttons on PDP
    const wishlistButtons = document.querySelectorAll('button[aria-label="Wishlist"]');
    function updateWishlistButtonState() {
      const isWish = window.isInWishlist(product.id);
      wishlistButtons.forEach(btn => {
        const svg = btn.querySelector('svg');
        if (isWish) {
          btn.className = 'p-2.5 rounded-full bg-white text-[#7A152E] border border-[#7A152E]/40 shadow-xs cursor-pointer';
          if (svg) svg.classList.add('fill-[#7A152E]', 'text-[#7A152E]');
        } else {
          btn.className = 'p-2.5 rounded-full bg-white/90 text-stone-700 hover:text-[#7A152E] border border-stone-200 shadow-xs cursor-pointer';
          if (svg) svg.classList.remove('fill-[#7A152E]', 'text-[#7A152E]');
        }
      });
    }
    updateWishlistButtonState();

    wishlistButtons.forEach(btn => {
      btn.onclick = function (e) {
        e.stopPropagation();
        window.toggleWishlist(product);
        updateWishlistButtonState();
      };
    });

    // Share Button
    const shareBtn = document.querySelector('button[aria-label="Share"]');
    if (shareBtn) {
      shareBtn.onclick = function () {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(window.location.href).then(() => {
            window.showToast('Piece Link Copied!', 'Atelier product link copied to your clipboard.');
          }).catch(() => {
            window.showToast('Solystra Atelier', window.location.href);
          });
        } else {
          window.showToast('Solystra Atelier', window.location.href);
        }
      };
    }

    // Laser Engraving Checkbox
    const engraveCheckbox = document.querySelector('input[type="checkbox"][class*="accent-black"]');
    if (engraveCheckbox) {
      engraveCheckbox.onchange = function () {
        let engraveInput = document.getElementById('pdp-engrave-text-box');
        if (this.checked) {
          if (!engraveInput) {
            engraveInput = document.createElement('div');
            engraveInput.id = 'pdp-engrave-text-box';
            engraveInput.className = 'mt-2 pt-2 border-t border-stone-100 flex items-center gap-2 animate-fade-in';
            engraveInput.innerHTML = `
              <input type="text" maxlength="8" placeholder="Enter initials (max 8 chars)" class="flex-1 px-3 py-1.5 border border-stone-200 rounded-lg text-xs uppercase font-mono tracking-wider focus:outline-none focus:border-[#7A152E]" />
              <span class="text-[10px] text-stone-400 font-mono">Complimentary</span>
            `;
            engraveCheckbox.closest('.border-y').appendChild(engraveInput);
          }
          engraveInput.style.display = 'flex';
          window.showToast('Laser Engraving Added', 'Complimentary custom engraving enabled.');
        } else if (engraveInput) {
          engraveInput.style.display = 'none';
        }
      };
    }

    // 9. Mobile Accordion Stack with See More / See Less Toggle
    const mobileAccordionCards = document.querySelectorAll('.md\\:hidden.divide-y.divide-stone-200 > div');
    mobileAccordionCards.forEach(card => {
      const header = card.querySelector('.cursor-pointer');
      const btn = card.querySelector('button');
      const content = card.querySelector('.transition-all.duration-300');
      const span = btn ? btn.querySelector('span') : null;
      const svg = btn ? btn.querySelector('svg') : null;

      function toggleAccordion() {
        if (!content) return;
        const isExpanded = content.classList.contains('opacity-100');
        if (isExpanded) {
          content.classList.remove('max-h-[1200px]', 'opacity-100', 'pb-4', 'px-4');
          content.classList.add('max-h-0', 'opacity-0');
          if (span) span.textContent = 'See More';
          if (svg) svg.classList.replace('rotate-180', 'rotate-0');
        } else {
          content.classList.remove('max-h-0', 'opacity-0');
          content.classList.add('max-h-[1200px]', 'opacity-100', 'pb-4', 'px-4');
          if (span) span.textContent = 'See Less';
          if (svg) svg.classList.replace('rotate-0', 'rotate-180');
        }
      }

      if (header) {
        header.onclick = function (e) {
          e.preventDefault();
          toggleAccordion();
        };
      }
      if (btn && btn !== header) {
        btn.onclick = function (e) {
          e.preventDefault();
          e.stopPropagation();
          toggleAccordion();
        };
      }
    });

    // 10. Desktop Specifications Tabs
    const desktopTabs = document.querySelectorAll('.hidden.md\\:grid.grid-cols-5 button');
    const desktopTabContentContainer = document.querySelector('.hidden.md\\:block.p-6.sm\\:p-10');

    if (desktopTabs.length > 0 && desktopTabContentContainer) {
      const tabPanelsData = [
        // Tab 0: Specifications & Purity
        `
        <div class="space-y-4 animate-fade-in">
          <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
            <h3 class="font-serif text-2xl text-stone-900 font-normal">Certified Craftsmanship Specifications</h3>
            <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">BIS 925 Hallmark Verified</span>
          </div>
          <p class="text-xs text-stone-500 font-light mb-4">Every Solystra creation is individually hallmarked and micro-set in pure 925 sterling silver.</p>
          <div id="pdp-specs-grid" class="grid grid-cols-1 md:grid-cols-2 gap-3.5 sm:gap-4 text-xs">
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Metal Purity</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Metal Purity']) || 'BIS Certified 925 Sterling Silver'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Plating Finish</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Plating Finish']) || 'Anti-Tarnish Rhodium & Micron E-Coat'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Stone Setting</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Stone Setting']) || 'AAA+ Austrian Solitaire Crystals'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Hallmark Verification</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Hallmark Verification']) || 'Certified 925 Stamp on Clasp/Band'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Warranty Coverage</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Warranty Coverage']) || '6 Months Free Replating Assurance'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
              <span class="text-stone-500 font-medium text-xs">Packaging</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Packaging']) || 'Luxury Suede Box with Authenticity Card'}</span>
            </div>
            <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors col-span-1 md:col-span-2">
              <span class="text-stone-500 font-medium text-xs">Shipping</span>
              <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${(product.specs && product.specs['Shipping']) || 'Free Insured Express Delivery Across India'}</span>
            </div>
          </div>
        </div>`,
        // Tab 1: Shipping & Details
        `
        <div class="space-y-5 animate-fade-in text-xs text-stone-700">
          <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
            <h3 class="font-serif text-2xl text-stone-900 font-normal">Express Insured Courier & Seamless Returns</h3>
            <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">BlueDart Express Air</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">24-48 Hr Dispatch</h5>
              <p class="text-stone-600 leading-relaxed font-light">Every creation undergoes a 7-point microscopic quality inspection and hallmarking verification before immediate dispatch.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">Transit Insurance</h5>
              <p class="text-stone-600 leading-relaxed font-light">100% door-to-door transit coverage. In the rare event of transit damage or delay, replacement or full refund is expedited.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">15-Day Easy Returns</h5>
              <p class="text-stone-600 leading-relaxed font-light">Complimentary doorstep pickup across 19,000+ PIN codes with full refund to original payment source within 48 hours.</p>
            </div>
          </div>
        </div>`,
        // Tab 2: Jewelry Care Guide
        `
        <div class="space-y-5 animate-fade-in text-xs text-stone-700">
          <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
            <h3 class="font-serif text-2xl text-stone-900 font-normal">Preserving Your Atelier Radiance</h3>
            <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Lifelong Silver Preservation</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">The "Last On, First Off" Rule</h5>
              <p class="text-stone-600 leading-relaxed font-light">Always wear your jewelry after applying makeup, perfumes, and lotions. Remove before swimming, showers, or intensive workouts to preserve the dual-micron rhodium shield.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">Signature Microfiber Buffing</h5>
              <p class="text-stone-600 leading-relaxed font-light">Gently polish stones and bands using the enclosed Solystra suede polishing cloth. Avoid abrasive chemical dips or ultrasonic bath solutions.</p>
            </div>
          </div>
        </div>`,
        // Tab 3: Packaging & Gifting
        `
        <div class="space-y-5 animate-fade-in text-xs text-stone-700">
          <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
            <h3 class="font-serif text-2xl text-stone-900 font-normal">The Royal Solystra Unboxing Experience</h3>
            <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Complimentary Keepsake Vault</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">Burgundy Suede Vault</h5>
              <p class="text-stone-600 leading-relaxed font-light">Custom fitted plush velvet interior with anti-tarnish micro-cushioning and embossed gold foil branding.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">Embossed Purity Certificate</h5>
              <p class="text-stone-600 leading-relaxed font-light">Individual serial certificate confirming BIS hallmarked 925 sterling silver purity and Austrian crystal grade.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">Gift Ready Presentation</h5>
              <p class="text-stone-600 leading-relaxed font-light">Delivered in a rigid satin-ribbon gift carrier bag with a personalized handwritten greeting card upon request.</p>
            </div>
          </div>
        </div>`,
        // Tab 4: Warranty & Authenticity
        `
        <div class="space-y-5 animate-fade-in text-xs text-stone-700">
          <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
            <h3 class="font-serif text-2xl text-stone-900 font-normal">Authenticity & 6-Month Plating Warranty</h3>
            <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Hallmark Certified</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">BIS 925 Hallmark Guarantee</h5>
              <p class="text-stone-600 leading-relaxed font-light">Bureau of Indian Standards certified pure silver content (92.5%). Every item carries the official triangular BIS stamp and Solystra atelier hallmark punch.</p>
            </div>
            <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
              <h5 class="font-semibold text-stone-900 text-sm">6 Months Free Replating</h5>
              <p class="text-stone-600 leading-relaxed font-light">Should your creation encounter unexpected tarnish or surface discoloration within 6 months, we replating and service your piece with complimentary reverse courier pickup.</p>
            </div>
          </div>
        </div>`
      ];

      desktopTabs.forEach((tabBtn, tabIdx) => {
        tabBtn.onclick = function () {
          desktopTabs.forEach((b, i) => {
            if (i === tabIdx) {
              b.className = 'py-4 px-2 lg:px-3 text-[11px] lg:text-xs uppercase tracking-wider transition-all text-center cursor-pointer border-r border-stone-200 last:border-r-0 border-b-2 border-b-[#7A152E] text-[#7A152E] bg-white font-bold shadow-2xs';
            } else {
              b.className = 'py-4 px-2 lg:px-3 text-[11px] lg:text-xs uppercase tracking-wider transition-all text-center cursor-pointer border-r border-stone-200 last:border-r-0 text-stone-500 hover:text-stone-900 hover:bg-stone-100/60 font-medium';
            }
          });
          desktopTabContentContainer.innerHTML = tabPanelsData[tabIdx] || tabPanelsData[0];
        };
      });
    }

    // 11. Design Story & Description
    const storyDesc = document.getElementById('pdp-story-desc');
    if (storyDesc) {
      storyDesc.textContent = product.desc || 'Handcrafted in certified 925 sterling silver with dual-micron rhodium for enduring brilliance and hypoallergenic comfort.';
    }

    // 12. Reviews Section Wiring & 5-Star Triggers
    const writeReviewBtns = document.querySelectorAll('button:has(svg.lucide-message-square), button:contains("Write a Review"), button:contains("Write Customer Review")');
    document.querySelectorAll('button').forEach(btn => {
      const txt = btn.textContent.trim();
      if (txt.includes('Write a Review') || txt.includes('Review this creation') || txt.includes('Write Customer Review')) {
        btn.onclick = function (e) {
          e.preventDefault();
          window.openReviewModal(product, 5);
        };
      } else if (txt.includes('Ask a Question') || txt.includes('Ask Concierge Desk')) {
        btn.onclick = function (e) {
          e.preventDefault();
          window.openAskQuestionModal(product);
        };
      }
    });

    // Wire individual star buttons in review summary prompt card
    const promptStarButtons = document.querySelectorAll('button[title*="Rate"]');
    promptStarButtons.forEach(btn => {
      const title = btn.getAttribute('title') || '';
      const match = title.match(/Rate (\d+)/);
      const starRating = match ? parseInt(match[1], 10) : 5;
      btn.onclick = function (e) {
        e.preventDefault();
        e.stopPropagation();
        window.openReviewModal(product, starRating);
      };
    });

    // Load custom reviews stored in localStorage
    try {
      const storedReviews = JSON.parse(localStorage.getItem('solystra_reviews_' + product.id) || '[]');
      const reviewsList = document.querySelector('.divide-y.divide-\\[\\#EAE4DC\\].pt-2');
      if (storedReviews.length > 0 && reviewsList) {
        storedReviews.forEach(rev => {
          const revArticle = document.createElement('article');
          revArticle.className = 'py-6 sm:py-7 space-y-3';
          revArticle.innerHTML = `
            <div class="flex items-start justify-between gap-2">
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-10 h-10 rounded-full bg-[#FAF0F2] text-[#7A152E] font-serif font-bold text-xs flex items-center justify-center shrink-0 border border-[#EAD5DA]">
                  ${rev.initials || 'VP'}
                </div>
                <div class="min-w-0">
                  <div class="flex flex-wrap items-center gap-1.5">
                    <span class="font-medium text-stone-900 text-sm">${rev.author}</span>
                    <span class="inline-flex items-center gap-1 text-[10px] font-semibold text-[#8B6B38] bg-[#FAF6EE] px-2 py-0.5 rounded-full border border-[#E8DCC4] shrink-0">
                      <svg class="lucide lucide-shield-check w-2.5 h-2.5 text-[#C5A059]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path></svg>
                      <span>Verified Patron</span>
                    </span>
                  </div>
                  <div class="text-[11px] text-stone-400 mt-0.5 flex items-center gap-2">
                    <span>${rev.city}</span>
                    <span>•</span>
                    <span class="text-[#7A152E] font-medium">${rev.date}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <div class="flex items-center gap-0.5">
                ${[...Array(5)].map((_, i) => `
                  <svg class="w-3.5 h-3.5 ${i < rev.rating ? 'text-[#C5A059] fill-[#C5A059]' : 'text-stone-300 fill-none'}" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
                  </svg>
                `).join('')}
              </div>
              <h5 class="font-semibold text-stone-900 text-xs sm:text-sm">${rev.title}</h5>
            </div>
            <p class="text-xs sm:text-[13px] text-stone-600 leading-relaxed font-light">${rev.comment}</p>
          `;
          reviewsList.insertBefore(revArticle, reviewsList.firstChild);
        });
      }
    } catch (e) {
      console.warn(e);
    }

    // 13. FAQ Accordion Interaction
    document.querySelectorAll('#qna-section .border, section:has(#qna-section) .border').forEach(card => {
      const qBtn = card.querySelector('button') || card.querySelector('h4');
      if (qBtn) {
        qBtn.style.cursor = 'pointer';
        qBtn.onclick = function () {
          const ans = card.querySelector('p');
          if (ans) {
            ans.classList.toggle('line-clamp-2');
            ans.classList.toggle('line-clamp-none');
          }
        };
      }
    });

    // 14. Pincode checker
    const pinBtn = document.querySelector('button:has(svg.lucide-truck)');
    const pinInput = document.querySelector('input[placeholder*="pincode"], input[placeholder*="Pincode"]');
    if (pinBtn && pinInput) {
      pinBtn.onclick = function (e) {
        e.preventDefault();
        const pin = pinInput.value.trim();
        if (pin.length === 6 && /^\d+$/.test(pin)) {
          window.showToast('Delivery Available', `BlueDart Express reaches ${pin} in 2-3 business days.`);
        } else {
          window.showToast('Invalid Pincode', 'Please enter a valid 6-digit Indian PIN code.', 'info');
        }
      };
    }
  }

  // Products Catalog Page Filtering & Sorting Engine
  window.initProductsPage = initProductsPage;
  function initProductsPage() {
    const grid = document.getElementById('products-catalog-grid') ||
                 document.querySelector('main .grid.grid-cols-2') ||
                 document.querySelector('.grid.xl\\:grid-cols-4') ||
                 document.querySelector('main .grid');
    if (!grid) return;
    grid.id = 'products-catalog-grid';

    const cards = Array.from(grid.children).filter(el => el.classList.contains('group'));
    if (cards.length === 0) return;

    // Build product lookup map by ID
    const productMap = {};
    if (window.PRODUCTS && Array.isArray(window.PRODUCTS)) {
      window.PRODUCTS.forEach(p => {
        productMap[p.id] = p;
      });
    }

    // Tag each card with metadata
    cards.forEach((card, idx) => {
      card.setAttribute('data-original-index', idx);
      const onclickAttr = card.getAttribute('onclick') || '';
      const match = onclickAttr.match(/id=([a-zA-Z0-9_-]+)/);
      const prodId = match ? match[1] : '';
      const prod = productMap[prodId] || {};

      card.setAttribute('data-id', prodId);
      card.setAttribute('data-name', (prod.name || card.querySelector('h3, h4, p')?.textContent || '').toLowerCase());
      card.setAttribute('data-category', (prod.category || 'all').toLowerCase());
      card.setAttribute('data-metal', (prod.metalType || 'silver').toLowerCase());
      card.setAttribute('data-price', prod.price || parseInt(card.querySelector('[class*="font-bold"]')?.textContent.replace(/[^0-9]/g, '') || '2999', 10));
      card.setAttribute('data-mrp', prod.mrp || 0);
      card.setAttribute('data-rating', prod.rating || 4.8);
      card.setAttribute('data-bestseller', (prod.isBestseller || prod.badge === 'Bestseller') ? 'true' : 'false');
      card.setAttribute('data-new', (prod.isNew || prod.badge === 'New Arrival') ? 'true' : 'false');

      // Wire quick-view / add-to-bag button on card
      const addBagBtn = card.querySelector('button');
      if (addBagBtn) {
        addBagBtn.onclick = function (e) {
          e.stopPropagation();
          if (window.addToCart && prod.id) {
            window.addToCart(prod);
          } else {
            window.location.href = `product.html?id=${prodId}`;
          }
        };
      }
    });

    // Filter states
    const params = new URLSearchParams(window.location.search);
    let activeCategory = (params.get('category') || 'all').toLowerCase();
    let activeMetal = (params.get('metal') || 'all').toLowerCase();
    let activeFilter = (params.get('filter') || 'all').toLowerCase();
    let maxPrice = parseInt(params.get('maxPrice') || '80000', 10);
    let activePriceRange = params.get('priceRange') || 'all';
    let searchQuery = (params.get('search') || '').trim().toLowerCase();
    let currentSort = params.get('sort') || 'featured';

    const searchInput = document.getElementById('catalog-search-input');
    if (searchInput && searchQuery) {
      searchInput.value = searchQuery;
    }

    const priceSlider = document.getElementById('catalog-price-slider');
    const priceDisplay = document.querySelector('input#catalog-price-slider')?.parentElement?.querySelector('.text-\\[\\#7A152E\\]');
    if (priceSlider) {
      priceSlider.value = maxPrice;
      if (priceDisplay) priceDisplay.textContent = `₹${maxPrice.toLocaleString('en-IN')}`;
    }

    // Function to apply filters
    function applyFilters() {
      let visibleCount = 0;

      cards.forEach(card => {
        const cat = card.getAttribute('data-category') || '';
        const metal = card.getAttribute('data-metal') || '';
        const price = parseInt(card.getAttribute('data-price') || '0', 10);
        const name = card.getAttribute('data-name') || '';
        const isBestseller = card.getAttribute('data-bestseller') === 'true';
        const isNew = card.getAttribute('data-new') === 'true';

        // Category match
        let catMatch = false;
        if (activeCategory === 'all') {
          catMatch = true;
        } else if (activeCategory === 'bestseller' || activeCategory === 'bestsellers') {
          catMatch = isBestseller;
        } else if (activeCategory === 'new') {
          catMatch = isNew;
        } else if (activeCategory === 'complete_sets' || activeCategory === 'gift sets & suites' || activeCategory === 'sets') {
          catMatch = cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite');
        } else if (activeCategory === 'layering chains' || activeCategory === 'chains') {
          catMatch = cat === 'necklaces' && (name.includes('chain') || name.includes('lariat'));
        } else if (activeCategory === 'silver anklets' || activeCategory === 'anklets') {
          catMatch = cat === 'anklets' || name.includes('anklet');
        } else if (activeCategory === 'bracelets & kadas' || activeCategory === 'bracelets') {
          catMatch = cat === 'bracelets' || name.includes('bracelet') || name.includes('bangle') || name.includes('cuff') || name.includes('kada');
        } else if (activeCategory === 'necklaces & pendants' || activeCategory === 'necklaces') {
          catMatch = cat === 'necklaces' || name.includes('necklace') || name.includes('pendant');
        } else if (activeCategory === 'rings & bands' || activeCategory === 'rings') {
          catMatch = cat === 'rings' || name.includes('ring') || name.includes('band') || name.includes('solitaire');
        } else if (activeCategory === 'earrings & studs' || activeCategory === 'earrings') {
          catMatch = cat === 'earrings' || name.includes('earring') || name.includes('stud') || name.includes('hoop') || name.includes('drop');
        } else {
          catMatch = cat.includes(activeCategory) || activeCategory.includes(cat);
        }

        // Metal match
        let metalMatch = false;
        if (activeMetal === 'all') {
          metalMatch = true;
        } else if (activeMetal === 'silver' || activeMetal === '925 silver') {
          metalMatch = metal === 'silver';
        } else if (activeMetal === 'gold' || activeMetal === '18k gold') {
          metalMatch = metal === 'gold';
        } else if (activeMetal === 'rose' || activeMetal === 'rose gold') {
          metalMatch = metal === 'rose';
        }

        // Filter badge match (bestseller / new)
        let filterMatch = true;
        if (activeFilter === 'bestseller') {
          filterMatch = isBestseller;
        } else if (activeFilter === 'new') {
          filterMatch = isNew;
        }

        // Price slider match
        let priceMatch = price <= maxPrice;

        // Quick price pill match
        if (activePriceRange !== 'all') {
          if (activePriceRange === 'under-3000') priceMatch = priceMatch && price < 3000;
          else if (activePriceRange === '3000-7000') priceMatch = priceMatch && price >= 3000 && price <= 7000;
          else if (activePriceRange === '7000-15000') priceMatch = priceMatch && price >= 7000 && price <= 15000;
          else if (activePriceRange === '15000-30000') priceMatch = priceMatch && price >= 15000 && price <= 30000;
          else if (activePriceRange === 'above-30000') priceMatch = priceMatch && price > 30000;
        }

        // Search match
        let searchMatch = true;
        if (searchQuery) {
          searchMatch = name.includes(searchQuery) || cat.includes(searchQuery) || metal.includes(searchQuery);
        }

        if (catMatch && metalMatch && filterMatch && priceMatch && searchMatch) {
          card.style.display = '';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      // Update counters
      const countEl = document.querySelector('.text-stone-400.font-light');
      if (countEl) {
        countEl.textContent = `(${visibleCount} creations)`;
      }

      // Show/Hide Empty State
      let emptyState = document.getElementById('catalog-empty-state');
      if (visibleCount === 0) {
        if (!emptyState) {
          emptyState = document.createElement('div');
          emptyState.id = 'catalog-empty-state';
          emptyState.className = 'col-span-full py-16 text-center space-y-4 bg-white rounded-2xl border border-[#EAE4DC] p-8 shadow-xs';
          emptyState.innerHTML = `
            <div class="w-14 h-14 rounded-full bg-[#FAF0F2] text-[#7A152E] flex items-center justify-center mx-auto border border-[#EAD5DA]">
              <svg class="w-6 h-6 stroke-[1.8]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>
            </div>
            <h4 class="font-serif text-xl text-stone-900 font-normal">No creations match your filter criteria</h4>
            <p class="text-xs text-stone-500 max-w-md mx-auto leading-relaxed">Try adjusting your budget, selecting all precious finishes, or resetting your filter preferences to explore the complete Solystra atelier collection.</p>
            <button onclick="window.resetCatalogFilters()" class="px-5 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-semibold uppercase tracking-wider rounded-xl shadow-xs transition-colors cursor-pointer">Reset All Filters</button>
          `;
          grid.appendChild(emptyState);
        }
        emptyState.style.display = 'block';
      } else if (emptyState) {
        emptyState.style.display = 'none';
      }
    }

    // Sorting function
    function applySort(sortKey) {
      currentSort = sortKey;
      const visibleCards = cards.slice();

      visibleCards.sort((a, b) => {
        if (sortKey === 'price-low') {
          return parseInt(a.getAttribute('data-price') || '0', 10) - parseInt(b.getAttribute('data-price') || '0', 10);
        } else if (sortKey === 'price-high') {
          return parseInt(b.getAttribute('data-price') || '0', 10) - parseInt(a.getAttribute('data-price') || '0', 10);
        } else if (sortKey === 'rating') {
          return parseFloat(b.getAttribute('data-rating') || '0') - parseFloat(a.getAttribute('data-rating') || '0');
        } else if (sortKey === 'newest') {
          const aNew = a.getAttribute('data-new') === 'true' ? 1 : 0;
          const bNew = b.getAttribute('data-new') === 'true' ? 1 : 0;
          return bNew - aNew;
        } else {
          return parseInt(a.getAttribute('data-original-index') || '0', 10) - parseInt(b.getAttribute('data-original-index') || '0', 10);
        }
      });

      visibleCards.forEach(c => grid.appendChild(c));
    }

    // Attach global filterCatalog for oninput/onchange
    window.filterCatalog = function () {
      if (searchInput) searchQuery = searchInput.value.trim().toLowerCase();
      applyFilters();
    };

    window.setCatalogMaxPrice = function (val) {
      maxPrice = parseInt(val, 10);
      if (priceDisplay) priceDisplay.textContent = `₹${maxPrice.toLocaleString('en-IN')}`;
      applyFilters();
    };

    window.resetCatalogFilters = function () {
      activeCategory = 'all';
      activeMetal = 'all';
      activeFilter = 'all';
      maxPrice = 80000;
      activePriceRange = 'all';
      searchQuery = '';
      if (searchInput) searchInput.value = '';
      if (priceSlider) priceSlider.value = 80000;
      if (priceDisplay) priceDisplay.textContent = '₹80,000';
      highlightCategoryPills();
      highlightMetalButtons();
      highlightPricePills();
      applyFilters();
      applySort('featured');
    };

    // Category button click handlers
    function highlightCategoryPills() {
      const topPills = document.querySelectorAll('section.bg-white.border-b button');
      topPills.forEach(btn => {
        const text = btn.textContent.trim().toLowerCase();
        let isMatch = false;
        if (activeCategory === 'all' && text.includes('all')) isMatch = true;
        else if (activeCategory === 'bracelets' && text.includes('bracelet')) isMatch = true;
        else if (activeCategory === 'necklaces' && text.includes('necklace')) isMatch = true;
        else if (activeCategory === 'rings' && text.includes('ring')) isMatch = true;
        else if (activeCategory === 'earrings' && text.includes('earring')) isMatch = true;
        else if (activeCategory === 'complete_sets' && (text.includes('suite') || text.includes('set'))) isMatch = true;
        else if (activeCategory === 'anklets' && text.includes('anklet')) isMatch = true;
        else if (activeCategory === 'bestseller' && text.includes('bestseller')) isMatch = true;
        else if (text.includes(activeCategory)) isMatch = true;

        if (isMatch) {
          btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all cursor-pointer active:scale-95 bg-[#7A152E] text-white shadow-xs';
        } else {
          btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all cursor-pointer active:scale-95 bg-stone-100 hover:bg-stone-200/80 text-stone-700';
        }
      });

      const sideCatButtons = document.querySelectorAll('aside button');
      sideCatButtons.forEach(btn => {
        const text = btn.textContent.trim().toLowerCase();
        if (text.includes('all metals') || text.includes('silver') || text.includes('gold') || text.includes('rose')) return;
        let isMatch = false;
        if (activeCategory === 'all' && text.includes('all designs')) isMatch = true;
        else if (activeCategory === 'bracelets' && text.includes('bracelet')) isMatch = true;
        else if (activeCategory === 'necklaces' && text.includes('necklace')) isMatch = true;
        else if (activeCategory === 'rings' && text.includes('ring')) isMatch = true;
        else if (activeCategory === 'earrings' && text.includes('earring')) isMatch = true;
        else if (activeCategory === 'complete_sets' && (text.includes('suite') || text.includes('set'))) isMatch = true;
        else if (activeCategory === 'anklets' && text.includes('anklet')) isMatch = true;

        if (isMatch) {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer bg-[#7A152E]/10 text-[#7A152E] font-semibold';
        } else {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50';
        }
      });
    }

    const topPills = document.querySelectorAll('section.bg-white.border-b button');
    topPills.forEach(btn => {
      btn.onclick = function () {
        const text = btn.textContent.trim().toLowerCase();
        if (text.includes('all')) activeCategory = 'all';
        else if (text.includes('bracelet')) activeCategory = 'bracelets';
        else if (text.includes('necklace')) activeCategory = 'necklaces';
        else if (text.includes('ring')) activeCategory = 'rings';
        else if (text.includes('earring')) activeCategory = 'earrings';
        else if (text.includes('suite') || text.includes('set')) activeCategory = 'complete_sets';
        else if (text.includes('chain')) activeCategory = 'necklaces';
        else if (text.includes('anklet')) activeCategory = 'anklets';
        else if (text.includes('bestseller')) activeCategory = 'bestseller';
        else activeCategory = text;

        highlightCategoryPills();
        applyFilters();
      };
    });

    const sideCatButtons = document.querySelectorAll('aside button');
    sideCatButtons.forEach(btn => {
      const text = btn.textContent.trim().toLowerCase();
      if (text.includes('all metals') || text.includes('silver') || text.includes('gold') || text.includes('rose')) return;
      btn.onclick = function () {
        if (text.includes('all designs')) activeCategory = 'all';
        else if (text.includes('bracelet')) activeCategory = 'bracelets';
        else if (text.includes('necklace')) activeCategory = 'necklaces';
        else if (text.includes('ring')) activeCategory = 'rings';
        else if (text.includes('earring')) activeCategory = 'earrings';
        else if (text.includes('suite') || text.includes('set')) activeCategory = 'complete_sets';
        else if (text.includes('chain')) activeCategory = 'necklaces';
        else if (text.includes('anklet')) activeCategory = 'anklets';
        else activeCategory = text;

        highlightCategoryPills();
        applyFilters();
      };
    });

    // Sidebar Metal polish buttons
    function highlightMetalButtons() {
      const metalButtons = Array.from(document.querySelectorAll('aside button')).filter(btn => {
        const t = btn.textContent.trim().toLowerCase();
        return t.includes('all metals') || t.includes('silver') || t.includes('gold') || t.includes('rose');
      });

      metalButtons.forEach(btn => {
        const t = btn.textContent.trim().toLowerCase();
        let isMatch = false;
        if (activeMetal === 'all' && t.includes('all metals')) isMatch = true;
        else if (activeMetal === 'silver' && t.includes('silver')) isMatch = true;
        else if (activeMetal === 'gold' && t.includes('gold') && !t.includes('rose')) isMatch = true;
        else if (activeMetal === 'rose' && t.includes('rose')) isMatch = true;

        if (isMatch) {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer bg-[#7A152E]/10 text-[#7A152E] font-semibold';
        } else {
          btn.className = 'w-full flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left cursor-pointer text-stone-600 hover:bg-stone-50';
        }
      });
    }

    const metalButtons = Array.from(document.querySelectorAll('aside button')).filter(btn => {
      const t = btn.textContent.trim().toLowerCase();
      return t.includes('all metals') || t.includes('silver') || t.includes('gold') || t.includes('rose');
    });

    metalButtons.forEach(btn => {
      btn.onclick = function () {
        const t = btn.textContent.trim().toLowerCase();
        if (t.includes('all metals')) activeMetal = 'all';
        else if (t.includes('silver')) activeMetal = 'silver';
        else if (t.includes('rose')) activeMetal = 'rose';
        else if (t.includes('gold')) activeMetal = 'gold';

        highlightMetalButtons();
        applyFilters();
      };
    });

    // Quick Price range buttons
    function highlightPricePills() {
      const priceButtons = document.querySelectorAll('main .flex.items-center.gap-1\\.5 button');
      priceButtons.forEach(btn => {
        const t = btn.textContent.trim().toLowerCase();
        if (!t.includes('price') && !t.includes('under') && !t.includes('3,000') && !t.includes('7,000') && !t.includes('15,000') && !t.includes('above')) return;
        let isMatch = false;
        if (activePriceRange === 'all' && t.includes('all prices')) isMatch = true;
        else if (activePriceRange === 'under-3000' && t.includes('under')) isMatch = true;
        else if (activePriceRange === '3000-7000' && t.includes('3,000')) isMatch = true;
        else if (activePriceRange === '7000-15000' && t.includes('7,000')) isMatch = true;
        else if (activePriceRange === '15000-30000' && t.includes('15,000')) isMatch = true;
        else if (activePriceRange === 'above-30000' && t.includes('above')) isMatch = true;

        if (isMatch) {
          btn.className = 'px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-semibold bg-[#7A152E] text-white shadow-2xs';
        } else {
          btn.className = 'px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium bg-white hover:bg-[#FAF8F5] border border-[#EAE4DC] text-stone-700 hover:border-[#7A152E]/30';
        }
      });
    }

    const priceButtons = document.querySelectorAll('main .flex.items-center.gap-1\\.5 button');
    priceButtons.forEach(btn => {
      const t = btn.textContent.trim().toLowerCase();
      if (!t.includes('price') && !t.includes('under') && !t.includes('3,000') && !t.includes('7,000') && !t.includes('15,000') && !t.includes('above')) return;
      btn.onclick = function () {
        if (t.includes('all prices')) activePriceRange = 'all';
        else if (t.includes('under')) activePriceRange = 'under-3000';
        else if (t.includes('3,000')) activePriceRange = '3000-7000';
        else if (t.includes('7,000')) activePriceRange = '7000-15000';
        else if (t.includes('15,000')) activePriceRange = '15000-30000';
        else if (t.includes('above')) activePriceRange = 'above-30000';

        highlightPricePills();
        applyFilters();
      };
    });

    // Sort Dropdown
    const sortButtons = document.querySelectorAll('button[aria-haspopup="listbox"]');
    sortButtons.forEach(sortBtn => {
      const container = sortBtn.parentElement;
      if (!container) return;

      let sortMenu = container.querySelector('.catalog-sort-menu');
      if (!sortMenu) {
        sortMenu = document.createElement('div');
        sortMenu.className = 'catalog-sort-menu hidden absolute right-0 mt-2 w-48 bg-white border border-[#EAE4DC] rounded-xl shadow-xl z-40 py-1 font-sans text-xs';
        sortMenu.innerHTML = `
          <button data-sort="featured" class="w-full text-left px-3.5 py-2 hover:bg-[#FAF0F2] hover:text-[#7A152E] transition-colors font-medium text-stone-800">Featured Curated</button>
          <button data-sort="price-low" class="w-full text-left px-3.5 py-2 hover:bg-[#FAF0F2] hover:text-[#7A152E] transition-colors font-medium text-stone-800">Price: Low to High</button>
          <button data-sort="price-high" class="w-full text-left px-3.5 py-2 hover:bg-[#FAF0F2] hover:text-[#7A152E] transition-colors font-medium text-stone-800">Price: High to Low</button>
          <button data-sort="rating" class="w-full text-left px-3.5 py-2 hover:bg-[#FAF0F2] hover:text-[#7A152E] transition-colors font-medium text-stone-800">Customer Rating ★</button>
          <button data-sort="newest" class="w-full text-left px-3.5 py-2 hover:bg-[#FAF0F2] hover:text-[#7A152E] transition-colors font-medium text-stone-800">Newest Arrivals</button>
        `;
        container.appendChild(sortMenu);

        sortMenu.querySelectorAll('button').forEach(item => {
          item.onclick = function (e) {
            e.stopPropagation();
            const sKey = item.getAttribute('data-sort');
            const label = item.textContent.trim();
            const labelSpan = sortBtn.querySelector('.truncate') || sortBtn.querySelector('span');
            if (labelSpan) labelSpan.textContent = label;
            sortMenu.classList.add('hidden');
            applySort(sKey);
          };
        });
      }

      sortBtn.onclick = function (e) {
        e.stopPropagation();
        document.querySelectorAll('.catalog-sort-menu').forEach(m => {
          if (m !== sortMenu) m.classList.add('hidden');
        });
        sortMenu.classList.toggle('hidden');
      };
    });

    document.addEventListener('click', () => {
      document.querySelectorAll('.catalog-sort-menu').forEach(m => m.classList.add('hidden'));
    });

    // Mobile Filters Drawer Button
    const mobileFilterBtn = document.querySelector('section.lg\\:hidden button:has(svg.lucide-sliders-horizontal)');
    if (mobileFilterBtn) {
      mobileFilterBtn.onclick = function () {
        window.openMobileFilterModal();
      };
    }

    // Initial setup
    highlightCategoryPills();
    highlightMetalButtons();
    highlightPricePills();
    applyFilters();
    if (currentSort !== 'featured') {
      applySort(currentSort);
    }
  }

  // Checkout Page initialization (Full 3-Step Interactive Experience matching React 1:1)
  function initCheckoutPage() {
    let currentStep = 1;
    let selectedPaymentMode = 'upi';
    let deliverySpeedCost = 0;
    let upiTimerInterval = null;
    let upiSecondsLeft = 585; // 09:45
    let lastOrderDetails = null;

    let cart = getCart();
    // If cart is empty, provide default luxury atelier piece so checkout is always fully testable
    if (!cart || cart.length === 0) {
      cart = [{
        id: 'universal-embrace',
        name: 'Accent Circle 925 Silver Necklace',
        price: 2798,
        mrp: 3861,
        image: 'solystra_assets/products/accent-circle-925-silver-necklace/angle_1.webp',
        metal: 'Pure 925 Silver',
        quantity: 1
      }];
    }

    // Calculate totals
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
    }

    // Render Order Summary Sidebar
    function renderOrderSummary() {
      const totals = computeTotals();
      const count = cart.reduce((acc, item) => acc + item.quantity, 0);

      // Headings
      const heading = document.getElementById('checkout-summary-heading');
      if (heading) heading.textContent = 'Order Summary (' + count + (count === 1 ? ' Piece)' : ' Pieces)');

      const mobTotal = document.getElementById('mobile-summary-total');
      if (mobTotal) mobTotal.textContent = formatINR(totals.grandTotal);

      // Items list (Desktop & Mobile)
      const listEl = document.getElementById('checkout-summary-items');
      const mobListEl = document.getElementById('mobile-summary-items-list');

      const itemsHtml = cart.map(item => `
        <div class="py-3 flex items-center gap-3.5">
          <div class="relative w-14 h-14 rounded-xl overflow-hidden border border-stone-200 shrink-0 bg-stone-50">
            <img src="${item.image}" alt="${item.name}" class="w-full h-full object-cover">
            <span class="absolute top-0 right-0 w-4 h-4 rounded-bl-lg bg-[#7A152E] text-white text-[9px] flex items-center justify-center font-mono">${item.quantity}</span>
          </div>
          <div class="flex-1 min-w-0 text-xs">
            <h4 class="font-serif font-medium text-stone-900 truncate">${item.name}</h4>
            <div class="text-[11px] text-stone-500 mt-0.5">${item.metal || 'Pure 925 Silver'} ${item.size ? '• Size ' + item.size : ''}</div>
          </div>
          <div class="text-right shrink-0 text-xs">
            <div class="font-bold text-stone-900">${formatINR(item.price * item.quantity)}</div>
            ${item.mrp && item.mrp > item.price ? '<div class="text-[10px] text-stone-400 line-through">' + formatINR(item.mrp * item.quantity) + '</div>' : ''}
          </div>
        </div>
      `).join('');

      if (listEl) listEl.innerHTML = itemsHtml;
      if (mobListEl) mobListEl.innerHTML = itemsHtml;

      // Price breakdown
      const mrpEl = document.getElementById('summary-mrp-total');
      if (mrpEl) mrpEl.textContent = formatINR(totals.mrpTotal);

      const savingsEl = document.getElementById('summary-savings-total');
      if (savingsEl) savingsEl.textContent = '-' + formatINR(totals.savings);

      // Discount row
      const discountRow = document.getElementById('summary-discount-row');
      const discountLabel = document.getElementById('summary-discount-label');
      const discountVal = document.getElementById('summary-discount-val');
      if (discountRow && discountLabel && discountVal) {
        if (totals.discount > 0) {
          discountRow.classList.remove('hidden');
          discountLabel.textContent = 'Coupon Discount (' + totals.promo + ')';
          discountVal.textContent = '-' + formatINR(totals.discount);
        } else {
          discountRow.classList.add('hidden');
        }
      }

      // Grand Total
      const grandTotalEl = document.getElementById('summary-grand-total');
      if (grandTotalEl) grandTotalEl.textContent = formatINR(totals.grandTotal);

      const payableHeader = document.getElementById('payable-amount-header');
      if (payableHeader) payableHeader.textContent = 'Payable: ' + formatINR(totals.grandTotal);

      const qrPayable = document.getElementById('qr-payable-text');
      if (qrPayable) qrPayable.textContent = formatINR(totals.grandTotal);

      const placeOrderText = document.getElementById('btn-place-order-text');
      if (placeOrderText) placeOrderText.textContent = 'Place Order & Pay ' + formatINR(totals.grandTotal);
    }

    // Delivery speed change
    document.querySelectorAll('input[name="deliveryMethod"]').forEach(radio => {
      radio.addEventListener('change', function () {
        deliverySpeedCost = this.value === 'express' ? 199 : 0;
        renderOrderSummary();
      });
    });

    // Step 1: Submit Delivery Address Form
    window.handleAddressSubmit = function (e) {
      if (e) e.preventDefault();

      const email = document.getElementById('input-email')?.value.trim();
      const phone = document.getElementById('input-phone')?.value.trim();
      const firstName = document.getElementById('input-first-name')?.value.trim();
      const lastName = document.getElementById('input-last-name')?.value.trim();
      const address = document.getElementById('input-address')?.value.trim();
      const locality = document.getElementById('input-locality')?.value.trim();
      const pincode = document.getElementById('input-pincode')?.value.trim();
      const city = document.getElementById('input-city')?.value.trim() || 'Mumbai';
      const state = document.getElementById('input-state')?.value.trim() || 'Maharashtra';

      const cleanPhone = (phone || '').replace(/\D/g, '');
      const cleanPincode = (pincode || '').replace(/\D/g, '');

      if (!email || !email.includes('@')) {
        window.showToast('Invalid Email', 'Please enter a valid email address.', 'info');
        return;
      }
      if (!cleanPhone || cleanPhone.length < 10) {
        window.showToast('Invalid Mobile Number', 'Please enter a valid 10-digit Indian phone number.', 'info');
        return;
      }
      if (!firstName || !lastName || !address) {
        window.showToast('Required Fields Missing', 'Please fill in your name and delivery address.', 'info');
        return;
      }
      if (!cleanPincode || cleanPincode.length !== 6) {
        window.showToast('Invalid PIN Code', 'Please enter a valid 6-digit Indian PIN code.', 'info');
        return;
      }

      // Update Summary card
      const custLine = document.getElementById('summary-customer-line');
      if (custLine) custLine.textContent = firstName + ' ' + lastName + ' (+91 ' + phone + ')';

      const addrLine = document.getElementById('summary-address-line');
      if (addrLine) addrLine.textContent = address + (locality ? ', ' + locality : '') + ', ' + city + ', ' + state + ' - ' + pincode;

      // Update button on COD tab if any
      const codOtpBtn = document.getElementById('btn-send-cod-otp');
      if (codOtpBtn) codOtpBtn.textContent = 'Send Verification OTP (+91 ' + phone + ')';

      // Collapse Step 1 form, show summary card
      document.getElementById('delivery-address-form')?.classList.add('hidden');
      document.getElementById('delivery-address-summary')?.classList.remove('hidden');
      document.getElementById('btn-edit-step-1')?.classList.remove('hidden');

      // Update Step 1 badge to green checkmark
      const s1Badge = document.getElementById('step-1-badge');
      if (s1Badge) {
        s1Badge.className = 'w-8 h-8 rounded-full bg-emerald-700 text-white text-xs font-bold flex items-center justify-center';
        s1Badge.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      }

      // Update Breadcrumbs: Step 1 completed, Step 2 active
      const b1 = document.getElementById('breadcrumb-step-1');
      const b2 = document.getElementById('breadcrumb-step-2');
      if (b1) b1.className = 'flex items-center gap-1.5 text-emerald-700 font-bold';
      if (b2) {
        b2.className = 'flex items-center gap-1.5 text-[#7A152E] font-bold';
        const circle = b2.querySelector('span');
        if (circle) circle.className = 'w-5 h-5 rounded-full bg-[#7A152E] text-white text-[10px] flex items-center justify-center font-mono';
      }

      // Unlock Step 2 Payment Gateway
      const step2Card = document.getElementById('checkout-step-2-card');
      if (step2Card) {
        step2Card.classList.remove('opacity-70', 'pointer-events-none');
        step2Card.classList.add('ring-2', 'ring-[#7A152E]/10');
      }

      const s2Badge = document.getElementById('step-2-badge');
      if (s2Badge) {
        s2Badge.className = 'w-8 h-8 rounded-full bg-[#7A152E] text-white text-xs font-bold flex items-center justify-center font-mono';
      }

      currentStep = 2;
      startUpiCountdown();
      window.showToast('Delivery Address Confirmed', 'Proceeding to secure payment authorization.');

      // Smooth scroll to payment section
      step2Card?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    };

    // Step 1: Edit button
    window.editDeliveryStep = function () {
      document.getElementById('delivery-address-form')?.classList.remove('hidden');
      document.getElementById('delivery-address-summary')?.classList.add('hidden');
      document.getElementById('btn-edit-step-1')?.classList.add('hidden');

      const s1Badge = document.getElementById('step-1-badge');
      if (s1Badge) {
        s1Badge.className = 'w-8 h-8 rounded-full bg-[#7A152E] text-white text-xs font-bold flex items-center justify-center font-mono';
        s1Badge.textContent = '1';
      }

      const step2Card = document.getElementById('checkout-step-2-card');
      if (step2Card) {
        step2Card.classList.add('opacity-70', 'pointer-events-none');
        step2Card.classList.remove('ring-2', 'ring-[#7A152E]/10');
      }

      const s2Badge = document.getElementById('step-2-badge');
      if (s2Badge) {
        s2Badge.className = 'w-8 h-8 rounded-full bg-stone-300 text-stone-700 text-xs font-bold flex items-center justify-center font-mono';
      }

      const b1 = document.getElementById('breadcrumb-step-1');
      const b2 = document.getElementById('breadcrumb-step-2');
      if (b1) b1.className = 'flex items-center gap-1.5 text-[#7A152E] font-bold';
      if (b2) {
        b2.className = 'flex items-center gap-1.5 text-stone-400';
        const circle = b2.querySelector('span');
        if (circle) circle.className = 'w-5 h-5 rounded-full text-[10px] flex items-center justify-center bg-stone-200 text-stone-600 font-mono';
      }

      currentStep = 1;
    };

    // Payment Mode Tabs
    window.selectPaymentTab = function (modeId) {
      selectedPaymentMode = modeId;
      const modes = ['upi', 'card', 'netbanking', 'cod'];

      modes.forEach(m => {
        const btn = document.getElementById('tab-btn-' + m);
        const panel = document.getElementById('payment-panel-' + m);
        if (m === modeId) {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-[#7A152E] bg-[#FAF8F5] ring-2 ring-[#7A152E]/15 shadow-sm';
            const icon = btn.querySelector('svg');
            if (icon) icon.className = icon.className.baseVal ? icon.className.baseVal.replace(/text-stone-400/g, 'text-[#7A152E]') : 'w-5 h-5 text-[#7A152E]';
            const label = btn.querySelector('.font-bold');
            if (label) label.className = 'font-bold text-xs text-[#7A152E]';
          }
          if (panel) panel.classList.remove('hidden');
        } else {
          if (btn) {
            btn.className = 'p-3 rounded-2xl border text-left transition-all cursor-pointer flex flex-col justify-between border-stone-200 bg-white hover:border-stone-300';
            const icon = btn.querySelector('svg');
            if (icon) icon.className = icon.className.baseVal ? icon.className.baseVal.replace(/text-\[#7A152E\]/g, 'text-stone-400') : 'w-5 h-5 text-stone-400';
            const label = btn.querySelector('.font-bold');
            if (label) label.className = 'font-bold text-xs text-stone-900';
          }
          if (panel) panel.classList.add('hidden');
        }
      });
    };

    // UPI App Selector
    window.selectUpiApp = function (btn) {
      document.querySelectorAll('.upi-app-btn').forEach(b => {
        b.className = 'upi-app-btn py-2.5 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer bg-white/60 border-stone-200 text-stone-700 hover:bg-white';
      });
      btn.className = 'upi-app-btn py-2.5 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition-all cursor-pointer bg-white border-[#7A152E] text-[#7A152E] shadow-sm ring-1 ring-[#7A152E]';
    };

    // UPI ID verify
    window.verifyUpiId = function () {
      const vpa = document.getElementById('upi-vpa-input')?.value.trim();
      if (!vpa || !vpa.includes('@')) {
        window.showToast('Invalid UPI ID', 'Please enter a valid UPI address (e.g. name@okhdfcbank).', 'info');
      } else {
        window.showToast('UPI Address Verified', vpa + ' is active and ready for one-click payment.');
      }
    };

    // UPI Timer Countdown
    function startUpiCountdown() {
      if (upiTimerInterval) clearInterval(upiTimerInterval);
      upiTimerInterval = setInterval(() => {
        if (upiSecondsLeft > 0) {
          upiSecondsLeft--;
          const m = String(Math.floor(upiSecondsLeft / 60)).padStart(2, '0');
          const s = String(upiSecondsLeft % 60).padStart(2, '0');
          const el = document.getElementById('upi-countdown');
          if (el) el.textContent = m + ':' + s;
        } else {
          clearInterval(upiTimerInterval);
        }
      }, 1000);
    }

    // Prefill demo card
    window.prefillDemoCard = function () {
      const numInput = document.getElementById('input-card-number');
      const nameInput = document.getElementById('input-card-name');
      const expInput = document.getElementById('input-card-expiry');
      const cvvInput = document.getElementById('input-card-cvv');

      if (numInput) numInput.value = '4532 8901 2345 9250';
      if (nameInput) nameInput.value = 'VRUND SHAH';
      if (expInput) expInput.value = '08/28';
      if (cvvInput) cvvInput.value = '925';

      window.updateCardPreview();
      window.showToast('Test Visa Prefilled', 'Mock 256-bit test card credentials injected.');
    };

    // Update 3D card preview
    window.updateCardPreview = function () {
      let num = document.getElementById('input-card-number')?.value.replace(/\D/g, '') || '';
      // Format with spaces
      let formattedNum = num.match(/.{1,4}/g)?.join(' ') || num;
      const numInput = document.getElementById('input-card-number');
      if (numInput && numInput.value !== formattedNum) {
        numInput.value = formattedNum;
      }

      const prevNum = document.getElementById('card-preview-number');
      if (prevNum) prevNum.textContent = formattedNum || '•••• •••• •••• 9250';

      const name = document.getElementById('input-card-name')?.value.toUpperCase() || '';
      const prevName = document.getElementById('card-preview-name');
      if (prevName) prevName.textContent = name || 'VRUND SHAH';

      let exp = document.getElementById('input-card-expiry')?.value.replace(/\D/g, '') || '';
      if (exp.length >= 3) exp = exp.slice(0, 2) + '/' + exp.slice(2, 4);
      const expInput = document.getElementById('input-card-expiry');
      if (expInput && expInput.value !== exp) expInput.value = exp;

      const prevExp = document.getElementById('card-preview-expiry');
      if (prevExp) prevExp.textContent = exp || '08/28';

      // Brand
      const brand = document.getElementById('card-preview-brand');
      if (brand) {
        if (num.startsWith('4')) brand.textContent = 'VISA';
        else if (num.startsWith('5')) brand.textContent = 'MASTERCARD';
        else if (num.startsWith('6')) brand.textContent = 'RUPAY';
        else brand.textContent = 'CARD';
      }
    };

    // Bank selector
    window.selectBank = function (btn, name) {
      document.querySelectorAll('.bank-btn').forEach(b => {
        b.className = 'bank-btn p-3 rounded-xl border text-xs font-semibold text-center transition-all cursor-pointer border-stone-200 bg-white/60 text-stone-700 hover:bg-white';
      });
      btn.className = 'bank-btn p-3 rounded-xl border text-xs font-semibold text-center transition-all cursor-pointer border-[#7A152E] bg-white text-[#7A152E] shadow-sm ring-1 ring-[#7A152E]';
      window.showToast('Bank Selected', name + ' authorized for net banking checkout.');
    };

    // COD OTP
    window.sendCodOtp = function () {
      const wrapper = document.getElementById('cod-otp-action-wrapper');
      if (!wrapper) return;

      wrapper.innerHTML = `
        <div class="flex gap-2 items-center">
          <input id="input-cod-otp" type="text" maxlength="4" placeholder="Enter OTP (Use: 9250)" class="w-48 px-3.5 py-2 rounded-xl border border-stone-200 bg-white font-mono text-center tracking-widest text-sm focus:border-[#7A152E] focus:outline-none"/>
          <button type="button" onclick="window.verifyCodOtp()" class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl font-semibold cursor-pointer">
            Verify OTP
          </button>
        </div>
      `;

      window.showToast('OTP Dispatched', 'Demo OTP: 9250 sent to your registered phone.');
    };

    window.verifyCodOtp = function () {
      const otp = document.getElementById('input-cod-otp')?.value.trim();
      const wrapper = document.getElementById('cod-otp-action-wrapper');
      if (otp === '9250' || (otp && otp.length === 4)) {
        if (wrapper) {
          wrapper.innerHTML = `
            <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-100 text-emerald-800 font-semibold">
              <svg class="w-4 h-4 text-emerald-700" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round"/></svg>
              <span>Phone Number Verified for Cash on Delivery</span>
            </div>
          `;
        }
        window.showToast('COD Verified', 'Your order is approved for doorstep inspection.');
      } else {
        window.showToast('Incorrect OTP', 'Please enter demo OTP: 9250.', 'info');
      }
    };

    // Coupon code apply on checkout
    window.applyCheckoutCoupon = function (e) {
      if (e) e.preventDefault();
      const code = document.getElementById('checkout-coupon-input')?.value.trim();
      if (!code) return;

      if (code.toUpperCase() === 'ROYAL10' || code.toUpperCase() === 'SOULY10') {
        setAppliedPromo(code.toUpperCase());
        window.showToast('Privilege Code Applied', '10% privilege reduction unlocked.');
      } else if (code.toUpperCase() === 'VAULT500') {
        setAppliedPromo(code.toUpperCase());
        window.showToast('Privilege Code Applied', 'Flat ₹500 vault credit applied.');
      } else {
        window.showToast('Invalid Code', 'Try ROYAL10 or VAULT500.', 'info');
      }
      renderOrderSummary();
    };

    window.useCheckoutPromo = function (code) {
      const input = document.getElementById('checkout-coupon-input');
      if (input) input.value = code;
      setAppliedPromo(code);
      renderOrderSummary();
      window.showToast('Privilege Code Applied', code + ' applied successfully.');
    };

    // PLACE ORDER & TRANSACTION SIMULATION
    window.handlePlaceOrder = function () {
      const totals = computeTotals();
      const modal = document.getElementById('checkout-processing-modal');
      const stepText = document.getElementById('processing-step-text');

      if (modal) modal.classList.remove('hidden');

      const steps = [
        'Authorizing 256-Bit Payment Gateway...',
        'Generating BIS Hallmark Authenticity Certificate...',
        'Confirming Insured BlueDart Air Courier Waybill...'
      ];

      let sIdx = 0;
      const stepTimer = setInterval(() => {
        sIdx++;
        if (sIdx < steps.length && stepText) {
          stepText.textContent = steps[sIdx];
        }
      }, 550);

      setTimeout(() => {
        clearInterval(stepTimer);
        if (modal) modal.classList.add('hidden');

        // Order generated
        const orderId = 'SLY-' + Math.floor(100000 + Math.random() * 900000);
        const waybill = 'BD-AIR-' + Math.floor(100000 + Math.random() * 900000);

        lastOrderDetails = {
          orderId,
          waybill,
          total: totals.grandTotal,
          items: [...cart],
          date: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
        };

        // Clear shopping cart
        localStorage.removeItem(CART_KEY);
        updateBadges();

        // Render confirmation screen
        const confOrderId = document.getElementById('confirmed-order-id');
        if (confOrderId) confOrderId.textContent = orderId;

        const confWaybill = document.getElementById('confirmed-waybill');
        if (confWaybill) confWaybill.textContent = waybill;

        const modalWaybill = document.getElementById('modal-waybill-text');
        if (modalWaybill) modalWaybill.textContent = 'Waybill: ' + waybill;

        // Render confirmed items
        const confList = document.getElementById('confirmed-items-list');
        if (confList) {
          confList.innerHTML = cart.map(item => `
            <div class="p-3 flex items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <img src="${item.image}" alt="${item.name}" class="w-12 h-12 rounded-lg object-cover border border-stone-200 bg-stone-50">
                <div>
                  <div class="font-medium text-xs text-stone-900">${item.name}</div>
                  <div class="text-[11px] text-stone-500">${item.metal || 'Pure 925 Silver'} • Qty ${item.quantity}</div>
                </div>
              </div>
              <div class="font-bold text-xs text-stone-900">
                ${formatINR(item.price * item.quantity)}
              </div>
            </div>
          `).join('');
        }

        // Hide main checkout, show confirmation view
        document.getElementById('checkout-main-view')?.classList.add('hidden');
        document.getElementById('checkout-confirmation-view')?.classList.remove('hidden');

        // Breadcrumbs: all completed
        const b1 = document.getElementById('breadcrumb-step-1');
        const b2 = document.getElementById('breadcrumb-step-2');
        const b3 = document.getElementById('breadcrumb-step-3');
        if (b1) b1.className = 'flex items-center gap-1.5 text-emerald-700 font-bold';
        if (b2) b2.className = 'flex items-center gap-1.5 text-emerald-700 font-bold';
        if (b3) {
          b3.className = 'flex items-center gap-1.5 text-[#7A152E] font-bold';
          const circle = b3.querySelector('span');
          if (circle) circle.className = 'w-5 h-5 rounded-full bg-[#7A152E] text-white text-[10px] flex items-center justify-center font-mono';
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
        window.showToast('Order Confirmed & Certified', 'Serial number registered with BIS Hallmark vault.');
      }, 1800);
    };

    // Mock PDF download
    window.downloadInvoiceMock = function () {
      if (!lastOrderDetails) return;
      alert(`📄 SOLYSTRA JEWELS TAX INVOICE\n\nInvoice Number: INV-${lastOrderDetails.orderId}\nDate: ${lastOrderDetails.date}\nTotal Paid: ${formatINR(lastOrderDetails.total)}\nGSTIN: 27AABCS1429M1ZB\n\n100% BIS Hallmarked 925 Sterling Silver Assurance Certificate Attached.\n(Mock PDF downloaded successfully)`);
    };

    // BlueDart modal
    window.openBlueDartModal = function () {
      document.getElementById('bluedart-tracking-modal')?.classList.remove('hidden');
    };

    // Initial render
    renderOrderSummary();
    window.updateCardPreview();
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
     - Exact 1:1 React Architecture
     - Auto-slides all 3 combos every 4.8s
     - Pauses on hover
     - Interactive glowing hotspots with hoverable luxury tooltip popovers
     - Cross-hover highlighting between model photo hotspots and right-hand item cards
     - "Add Look to Bag" adds both pieces to the cart drawer
     ========================================================================== */
  const STYLING_COMBOS = [
    {
      id: 'combo-1',
      name: 'Amethyst Floral Blossom Set',
      tag: 'ROSE GOLD VERMEIL',
      desc: 'Handcrafted floral blossom necklace paired with matching petal drop earrings.',
      editorialImg: 'solystra_assets/banners/banner_blush_tones_pc.webp',
      imagePosition: 'object-[75%_center]',
      items: [
        {
          id: 'c1-item-1',
          productId: 'amethyst-bloom-necklace-set-925-sterling-silver',
          type: 'NECKLACE',
          name: 'Amethyst Bloom Floral Necklace',
          metal: 'Rose Gold Vermeil • Handcrafted Setting',
          price: 9585,
          mrp: 11981,
          image: 'solystra_assets/products/amethyst-bloom-necklace-set-925-sterling-silver/angle_1.webp',
          hotspot: { x: 75.1, y: 55.0, pcX: 75.1, pcY: 55.0, label: 'Floral Blossom Necklace' }
        },
        {
          id: 'c1-item-2',
          productId: 'flora-band-hoops',
          type: 'EARRINGS',
          name: 'Blossom Petal Drop Earrings',
          metal: 'Rose Gold Vermeil • Double-Micron Rhodium',
          price: 2499,
          mrp: 3499,
          image: 'solystra_assets/products/flora-band-hoops/angle_1.webp',
          hotspot: { x: 78.6, y: 27.1, pcX: 78.6, pcY: 27.1, label: 'Blossom Drop Earrings' }
        }
      ],
      bundlePrice: 12084,
      originalPrice: 15480,
      savings: 3396
    },
    {
      id: 'combo-2',
      name: 'Classic Solitaire Set',
      tag: 'PURE 925 STERLING SILVER',
      desc: 'Brilliant Austrian solitaire pendant paired with matching solitaire drop earrings.',
      editorialImg: 'solystra_assets/banners/banner_pc_1.webp',
      imagePosition: 'object-[72%_center]',
      items: [
        {
          id: 'c2-item-1',
          productId: 'universal-embrace',
          type: 'NECKLACE',
          name: 'Universal Solitaire Drop Necklace',
          metal: 'Pure 925 Silver • Brilliant Cut Solitaire',
          price: 2799,
          mrp: 3999,
          image: 'solystra_assets/products/unity-circle/angle_1.webp',
          hotspot: { x: 32.3, y: 76.2, pcX: 46.1, pcY: 78.2, label: 'Solitaire Pendant Necklace' }
        },
        {
          id: 'c2-item-2',
          productId: 'classic-knot-earrings',
          type: 'EARRINGS',
          name: 'Solitaire Drop Earrings',
          metal: 'Pure 925 Silver • Cushion Cut Drop',
          price: 2299,
          mrp: 3299,
          image: 'solystra_assets/products/classic-knot-earrings/angle_1.webp',
          hotspot: { x: 42.7, y: 40.6, pcX: 53.6, pcY: 41.8, label: 'Solitaire Drop Earrings' }
        }
      ],
      bundlePrice: 5098,
      originalPrice: 7298,
      savings: 2200
    },
    {
      id: 'combo-3',
      name: 'Gala Choker & Chandelier Set',
      tag: 'FINE EVENING WEAR',
      desc: 'Graduated tennis choker in pure silver paired with tiered chandelier drops.',
      editorialImg: 'solystra_assets/generated/cocktail_glam.webp',
      imagePosition: 'object-center',
      items: [
        {
          id: 'c3-item-1',
          productId: 'golden-meadow-necklace-set-925-sterling-silver',
          type: 'NECKLACE',
          name: 'Grand Solitaire Tennis Choker',
          metal: 'Pure 925 Silver • Graduated Tennis Links',
          price: 5499,
          mrp: 7999,
          image: 'solystra_assets/products/golden-meadow-necklace-set-925-sterling-silver/angle_1.webp',
          hotspot: { x: 52.5, y: 50.5, pcX: 52.5, pcY: 50.5, label: 'Graduated Tennis Choker' }
        },
        {
          id: 'c3-item-2',
          productId: 'greek-pattern-hoops',
          type: 'EARRINGS',
          name: 'Imperial Chandelier Drops',
          metal: 'Pure 925 Silver • Multi-Tier Drops',
          price: 3499,
          mrp: 4999,
          image: 'solystra_assets/products/greek-pattern-hoops/angle_1.webp',
          hotspot: { x: 60.8, y: 34.5, pcX: 60.8, pcY: 34.5, label: 'Imperial Chandelier Drops' }
        }
      ],
      bundlePrice: 8998,
      originalPrice: 12998,
      savings: 4000
    }
  ];

  let currentComboIdx = 1; // Default to Classic Solitaire Set
  let isComboSectionHovered = false;
  let activeHotspotItemId = null;
  let comboTimer = null;

  function initStylingCombos() {
    const grid = document.getElementById('curated-combo-grid');
    if (!grid) return;

    function renderCombo(idx) {
      currentComboIdx = idx;
      activeHotspotItemId = null;
      const combo = STYLING_COMBOS[idx];
      if (!combo) return;

      // Update counter
      const counterEl = document.getElementById('curated-combo-counter');
      if (counterEl) {
        counterEl.textContent = 'Combo 0' + (idx + 1) + ' / 0' + STYLING_COMBOS.length;
      }

      // Update dot indicators
      const dotButtons = document.querySelectorAll('#curated-combo-dots button');
      dotButtons.forEach((btn, dIdx) => {
        if (dIdx === idx) {
          btn.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-5 bg-[#7A152E]';
        } else {
          btn.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-1.5 bg-stone-300 hover:bg-stone-400';
        }
      });

      // Build hotspots HTML
      const hotspotsHtml = combo.items.map(item => {
        if (!item.hotspot) return '';
        const pcX = item.hotspot.pcX !== undefined ? item.hotspot.pcX : item.hotspot.x;
        const pcY = item.hotspot.pcY !== undefined ? item.hotspot.pcY : item.hotspot.y;
        const isBottom = (item.hotspot.y > 55 || pcY > 55);
        const isRight = (item.hotspot.x > 60 || pcX > 60);

        const popoverPos = (isBottom ? 'bottom-full mb-3' : 'top-full mt-3') + ' ' +
                           (isRight ? 'right-0 sm:-right-4' : 'left-0 sm:-left-4');

        return `
          <div class="combo-hotspot-pin absolute -translate-x-1/2 -translate-y-1/2 z-20"
               data-hotspot-id="${item.id}"
               style="--dot-x-mob: ${item.hotspot.x}%; --dot-y-mob: ${item.hotspot.y}%; --dot-x-pc: ${pcX}%; --dot-y-pc: ${pcY}%;">
            <div class="relative group/hotspot cursor-pointer">
              <!-- Subtle micro pulse -->
              <span class="absolute -inset-0.5 rounded-full bg-[#7A152E]/35 animate-ping pointer-events-none"></span>

              <!-- Small Luxury Pinpoint Button -->
              <button type="button"
                      data-pin-btn="${item.id}"
                      class="w-3 h-3 sm:w-3.5 sm:h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer bg-[#7A152E] hover:scale-125"
                      aria-label="View ${item.name}">
                <span class="w-1 h-1 rounded-full bg-white shadow-xs pointer-events-none"></span>
              </button>

              <!-- Interactive Luxury Tooltip Popover -->
              <div data-popover="${item.id}"
                   class="absolute z-30 transition-all duration-300 pointer-events-auto ${popoverPos} opacity-0 scale-95 invisible min-w-[210px] sm:min-w-[230px] p-2.5 rounded-xl bg-[#1C1819]/95 backdrop-blur-md border border-[#C5A059]/60 shadow-[0_15px_35px_rgba(0,0,0,0.6)]">
                <div class="flex items-center gap-2.5">
                  <img src="${item.image}" alt="${item.name}" onerror="if(!this.dataset.err){this.dataset.err=1; this.src=this.src.endsWith('.webp')?this.src.replace('.webp','.png'):(this.src.endsWith('.png')?this.src.replace('.png','.jpg'):this.src.replace('.jpg','.webp'));}" class="w-11 h-11 rounded-lg object-cover bg-white/10 border border-white/20 shrink-0">
                  <div class="flex-1 min-w-0 text-left">
                    <span class="text-[9px] uppercase tracking-wider font-bold text-[#E5C985] block">${item.type}</span>
                    <h5 class="text-xs font-serif font-normal text-white truncate">${item.name}</h5>
                    <div class="text-[11px] font-bold text-[#E5C985] mt-0.5">₹${item.price.toLocaleString('en-IN')}</div>
                  </div>
                </div>
                <div class="mt-2 pt-1.5 border-t border-white/10 flex items-center justify-between text-[9.5px] text-stone-300">
                  <span class="text-stone-400">Click to view piece</span>
                  <a href="product.html?id=${item.productId}" class="text-[#E5C985] font-bold flex items-center gap-1 hover:underline">
                    <span>Shop Piece</span>
                    <svg class="lucide lucide-arrow-right w-2.5 h-2.5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        `;
      }).join('');

      // Build right-hand matched pieces HTML
      const itemsHtml = combo.items.map(item => `
        <div data-combo-item="${item.id}"
             data-product-id="${item.productId}"
             class="flex items-center gap-3.5 p-3 rounded-xl transition-all cursor-pointer group border bg-[#FAF8F5]/80 border-[#EAE4DC] hover:border-[#7A152E]/60 hover:bg-white hover:shadow-2xs"
             title="Click to view product details">
          <img src="${item.image}" alt="${item.name}" onerror="if(!this.dataset.err){this.dataset.err=1; this.src=this.src.endsWith('.webp')?this.src.replace('.webp','.png'):(this.src.endsWith('.png')?this.src.replace('.png','.jpg'):this.src.replace('.jpg','.webp'));}" class="w-14 h-14 rounded-xl object-cover border border-[#EAE4DC] bg-white shrink-0 group-hover:scale-105 transition-transform">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-[9.5px] text-[#7A152E] uppercase font-bold tracking-wider block">${item.type}</span>
              <span class="text-[9px] text-[#C5A059] opacity-0 group-hover:opacity-100 transition-opacity font-semibold">View Piece ↗</span>
            </div>
            <h4 class="font-serif text-sm font-normal text-stone-900 truncate group-hover:text-[#7A152E] transition-colors mt-0.5">${item.name}</h4>
            <div class="text-[11px] text-stone-500 truncate mt-0.5">${item.metal}</div>
          </div>
          <div class="text-right shrink-0">
            <div class="font-bold text-sm text-[#7A152E]">₹${item.price.toLocaleString('en-IN')}</div>
            <div class="text-[11px] text-stone-400 line-through">₹${item.mrp.toLocaleString('en-IN')}</div>
          </div>
        </div>
      `).join('');

      // Complete 2-Column HTML
      grid.innerHTML = `
        <!-- Left Column: Editorial Photo with Delicate Glowing Hotspots -->
        <div id="combo-left-col" class="lg:col-span-6 h-[380px] sm:h-[420px] lg:h-[430px] relative rounded-2xl overflow-hidden shadow-xs border border-[#EAE4DC] group bg-stone-900 select-none">
          <img src="${combo.editorialImg}" alt="${combo.name}" draggable="false" class="w-full h-full object-cover ${combo.imagePosition} group-hover:scale-102 transition-transform duration-700 block pointer-events-none animate-fadeIn">
          
          <!-- Subtle ambient gradient in bottom 20% -->
          <div class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/80 via-black/25 to-transparent pointer-events-none"></div>

          <!-- Glowing Hotspots -->
          ${hotspotsHtml}

          <!-- Bottom Editorial Tag & Name -->
          <div class="absolute bottom-3 left-3 sm:bottom-4 sm:left-4 z-10 pointer-events-none max-w-[85%] sm:max-w-md">
            <span class="text-[8px] xs:text-[9px] sm:text-[10px] uppercase tracking-widest text-[#E5C985] font-bold block mb-0.5 drop-shadow-xs">${combo.tag}</span>
            <h3 class="font-serif text-sm xs:text-base sm:text-xl text-white font-normal leading-snug drop-shadow-sm whitespace-nowrap">${combo.name}</h3>
          </div>
        </div>

        <!-- Right Column: Matched Pieces & Bundle Pricing -->
        <div id="combo-right-col" class="lg:col-span-6 h-[380px] sm:h-[420px] lg:h-[430px] flex flex-col justify-between bg-white rounded-2xl p-5 sm:p-6 border border-[#EAE4DC] shadow-xs animate-fadeIn">
          <div>
            <div class="flex items-start justify-between pb-3 border-b border-[#EAE4DC] gap-2">
              <div>
                <span class="text-[9.5px] text-[#7A152E] uppercase tracking-widest font-bold block">${combo.tag}</span>
                <h3 class="text-sm sm:text-base font-serif font-normal text-stone-900 leading-tight mt-0.5">${combo.name}</h3>
              </div>
              <span class="text-[10.5px] text-[#7A152E] font-bold bg-[#7A152E]/8 px-2.5 py-1 rounded-full border border-[#7A152E]/20 uppercase tracking-wider shrink-0">
                Save ₹${combo.savings.toLocaleString('en-IN')}
              </span>
            </div>

            <!-- 2 Equal-Height Matched Pieces Cards -->
            <div class="space-y-2.5 mt-3.5">
              ${itemsHtml}
            </div>
          </div>

          <!-- Bundle Pricing & Action Bar -->
          <div class="pt-3.5 mt-3 border-t border-[#EAE4DC] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="text-[10px] text-stone-500 uppercase tracking-wider font-semibold">Complete Set Price</div>
              <div class="flex items-baseline gap-2 mt-0.5">
                <span class="font-serif text-2xl sm:text-3xl font-bold text-[#7A152E]">₹${combo.bundlePrice.toLocaleString('en-IN')}</span>
                <span class="text-xs text-stone-400 line-through font-sans">₹${combo.originalPrice.toLocaleString('en-IN')}</span>
                <span class="text-[10px] font-bold text-[#7A152E] uppercase bg-[#7A152E]/10 px-2 py-0.5 rounded-full border border-[#7A152E]/20">Save ₹${combo.savings.toLocaleString('en-IN')}</span>
              </div>
            </div>

            <button type="button" id="btn-add-combo-to-bag" class="px-6 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer flex items-center justify-center gap-2 active:scale-98 shrink-0 group">
              <svg aria-hidden="true" class="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <defs><linearGradient id="solystraChampagneGoldCombo" x1="0%" x2="100%" y1="0%" y2="100%"><stop offset="0%" stop-color="#FFF6D8"></stop><stop offset="35%" stop-color="#F9E2A8"></stop><stop offset="70%" stop-color="#E5BE64"></stop><stop offset="100%" stop-color="#D4AF37"></stop></linearGradient></defs>
                <path d="M6 2L3 6V20C3 21.1 3.9 22 5 22H19C20.1 22 21 21.1 21 20V6L18 2H6Z" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                <path d="M3 6H21" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                <path d="M16 10C16 12.21 14.21 14 12 14C9.79 14 8 12.21 8 10" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
              <span class="leading-none">Add Look to Bag</span>
            </button>
          </div>
        </div>
      `;

      // Helper function to set active hotspot
      function setActiveHotspot(itemId) {
        activeHotspotItemId = itemId;
        const allPins = grid.querySelectorAll('.combo-hotspot-pin');
        const allCards = grid.querySelectorAll('[data-combo-item]');

        allPins.forEach(pin => {
          const pId = pin.getAttribute('data-hotspot-id');
          const btn = pin.querySelector('button');
          const popover = pin.querySelector('[data-popover]');
          if (pId === itemId) {
            if (btn) btn.className = 'w-3 h-3 sm:w-3.5 sm:h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer scale-125 bg-[#7A152E] ring-2 ring-[#D4AF37]';
            if (popover) {
              popover.classList.remove('opacity-0', 'scale-95', 'invisible');
              popover.classList.add('opacity-100', 'scale-100', 'visible');
            }
          } else {
            if (btn) btn.className = 'w-3 h-3 sm:w-3.5 sm:h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer bg-[#7A152E] hover:scale-125';
            if (popover) {
              popover.classList.remove('opacity-100', 'scale-100', 'visible');
              popover.classList.add('opacity-0', 'scale-95', 'invisible');
            }
          }
        });

        allCards.forEach(card => {
          const cId = card.getAttribute('data-combo-item');
          if (cId === itemId) {
            card.className = 'flex items-center gap-3.5 p-3 rounded-xl transition-all cursor-pointer group border bg-[#7A152E]/5 border-[#7A152E] shadow-sm ring-1 ring-[#7A152E]/20';
          } else {
            card.className = 'flex items-center gap-3.5 p-3 rounded-xl transition-all cursor-pointer group border bg-[#FAF8F5]/80 border-[#EAE4DC] hover:border-[#7A152E]/60 hover:bg-white hover:shadow-2xs';
          }
        });
      }

      // Attach hotspot pin hover and click listeners
      grid.querySelectorAll('.combo-hotspot-pin').forEach(pin => {
        const itemId = pin.getAttribute('data-hotspot-id');
        const item = combo.items.find(i => i.id === itemId);

        pin.addEventListener('mouseenter', () => setActiveHotspot(itemId));
        pin.addEventListener('mouseleave', () => setActiveHotspot(null));
        pin.addEventListener('click', (e) => {
          e.stopPropagation();
          if (activeHotspotItemId === itemId && item) {
            window.location.href = 'product.html?id=' + item.productId;
          } else {
            setActiveHotspot(itemId);
          }
        });
      });

      // Attach right-hand item cards hover and click listeners
      grid.querySelectorAll('[data-combo-item]').forEach(card => {
        const itemId = card.getAttribute('data-combo-item');
        const prodId = card.getAttribute('data-product-id');

        card.addEventListener('mouseenter', () => setActiveHotspot(itemId));
        card.addEventListener('mouseleave', () => setActiveHotspot(null));
        card.addEventListener('click', () => {
          if (prodId) window.location.href = 'product.html?id=' + prodId;
        });
      });

      // Pause/resume auto-slide on hover
      const leftCol = document.getElementById('combo-left-col');
      const rightCol = document.getElementById('combo-right-col');
      [leftCol, rightCol].forEach(col => {
        if (col) {
          col.addEventListener('mouseenter', () => { isComboSectionHovered = true; });
          col.addEventListener('mouseleave', () => { isComboSectionHovered = false; });
        }
      });

      // Wire "Add Look to Bag" button
      const addBagBtn = document.getElementById('btn-add-combo-to-bag');
      if (addBagBtn) {
        addBagBtn.addEventListener('click', () => {
          combo.items.forEach(item => {
            let prod = findProduct(item.productId);
            if (!prod) {
              prod = {
                id: item.productId,
                name: item.name,
                price: item.price,
                mrp: item.mrp,
                images: [item.image],
                metals: [item.metal]
              };
            }
            window.addToCart(prod, item.metal, null, '', 1);
          });
          window.showToast('Curated Look Added', combo.name + ' (2 pieces) added to your private bag.');
          window.openCartDrawer();
        });
      }
    }

    // Attach click handlers to top dot selectors
    const dotButtons = document.querySelectorAll('#curated-combo-dots button');
    dotButtons.forEach((btn, idx) => {
      btn.addEventListener('click', () => {
        renderCombo(idx);
        startComboTimer();
      });
    });

    function startComboTimer() {
      if (comboTimer) clearInterval(comboTimer);
      comboTimer = setInterval(() => {
        if (!isComboSectionHovered && activeHotspotItemId === null) {
          const next = (currentComboIdx + 1) % STYLING_COMBOS.length;
          renderCombo(next);
        }
      }, 4800);
    }

    // Initial render: start at Combo 2 (Classic Solitaire Set) or Combo 1
    renderCombo(1);
    startComboTimer();
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


  // ==========================================
  // Global Interactive Modals & Redirects Helpers
  // ==========================================

  // Global Newsletter Form Submit Handler
  document.addEventListener('submit', function (e) {
    const form = e.target;
    const emailInput = form.querySelector('input[type="email"]');
    if (emailInput && !form.closest('#checkout-form')) {
      e.preventDefault();
      const email = emailInput.value.trim();
      if (email) {
        window.showToast('Privilege Discount Unlocked', 'Welcome to the Solystra Club! Code SOULY10 (10% off) copied to clipboard.', 'success');
        try { navigator.clipboard.writeText('SOULY10'); } catch (_) {}
        emailInput.value = '';
      }
    }
  });

  // Mobile Footer Accordions
  function initFooterAccordions() {
    document.querySelectorAll('footer .sm\\:hidden button').forEach(btn => {
      btn.onclick = function (e) {
        e.preventDefault();
        const parent = btn.parentElement;
        let drawer = parent.querySelector('.accordion-drawer');
        if (!drawer) {
          drawer = document.createElement('div');
          drawer.className = 'accordion-drawer p-3 pt-0 text-stone-600 text-[11.5px] space-y-2 border-t border-stone-100 mt-2';
          const title = btn.textContent.trim();
          if (title.includes('Collections')) {
            drawer.innerHTML = `
              <ul class="space-y-1.5">
                <li><a class="text-[#7A152E] font-medium" href="products.html?category=necklaces">&bull; 925 Silver Necklaces</a></li>
                <li><a class="hover:text-[#7A152E]" href="products.html?category=rings">&bull; Solitaire &amp; Stacking Rings</a></li>
                <li><a class="hover:text-[#7A152E]" href="products.html?category=bracelets">&bull; Tennis Bracelets &amp; Cuffs</a></li>
                <li><a class="hover:text-[#7A152E]" href="products.html?category=earrings">&bull; Earrings &amp; Huggies</a></li>
                <li><a class="hover:text-[#7A152E]" href="products.html?category=anklets">&bull; Dainty Anklets</a></li>
                <li><a class="hover:text-[#7A152E]" href="products.html?metal=gold">&bull; 18K Italian Gold Vermeil</a></li>
              </ul>
            `;
          } else if (title.includes('Customer Care')) {
            drawer.innerHTML = `
              <ul class="space-y-1.5">
                <li><a class="hover:text-[#7A152E]" href="terms.html#shipping" onclick="window.openTrackOrderModal(); return false;">&bull; Track Your Order</a></li>
                <li><a class="hover:text-[#7A152E]" href="terms.html#shipping">&bull; Shipping &amp; Insured Express</a></li>
                <li><a class="hover:text-[#7A152E]" href="terms.html#returns">&bull; 15-Day Easy Returns</a></li>
                <li><a class="hover:text-[#7A152E]" href="terms.html#sizing" onclick="window.openSizeGuideModal(); return false;">&bull; Ring Sizing Guide</a></li>
                <li><a class="hover:text-[#7A152E]" href="terms.html#care">&bull; Jewelry Care &amp; Spa Guide</a></li>
                <li><a class="hover:text-[#7A152E]" href="privacy.html">&bull; Privacy &amp; Security Policy</a></li>
              </ul>
            `;
          } else {
            drawer.innerHTML = `
              <ul class="space-y-1.5 text-stone-600">
                <li>&bull; 100% Certified BIS 925 Stamp</li>
                <li>&bull; AAA+ Austrian 57-Facet Solitaires</li>
                <li>&bull; 2.0-Micron Anti-Tarnish Rhodium</li>
                <li>&bull; Free Insured Express Delivery</li>
                <li><a class="text-[#7A152E] font-semibold underline mt-1 block" href="terms.html">&bull; Read Full Purity Terms</a></li>
              </ul>
            `;
          }
          parent.appendChild(drawer);
        } else {
          drawer.classList.toggle('hidden');
        }
        const chevron = btn.querySelector('svg.lucide-chevron-down');
        if (chevron) chevron.classList.toggle('rotate-180');
      };
    });
  }

  // Ring Sizing Modal
  window.openSizeGuideModal = function () {
    let modal = document.getElementById('size-guide-modal-root');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'size-guide-modal-root';
      modal.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 font-sans';
      modal.innerHTML = `
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-8 space-y-4 shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex justify-between items-center border-b border-stone-200 pb-3">
            <h3 class="font-serif text-xl text-stone-900 font-normal">
              Ring &amp; Wrist Measurement Guide
            </h3>
            <button onclick="window.closeSizeGuideModal()" class="p-1 text-stone-400 hover:text-stone-800 cursor-pointer">
              <svg class="lucide lucide-x w-5 h-5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="text-xs text-stone-600 space-y-3 font-normal">
            <p>To measure your ring size accurately at home:</p>
            <ol class="list-decimal pl-4 space-y-1">
              <li>Wrap a narrow strip of paper or string snugly around your intended finger.</li>
              <li>Mark the exact spot where the paper overlaps.</li>
              <li>Measure the millimeter length with a standard ruler.</li>
            </ol>
            <div class="border border-stone-200 rounded-xl overflow-hidden mt-3">
              <table class="w-full text-left divide-y divide-stone-200">
                <thead class="bg-stone-50 text-[11px] font-semibold text-stone-800">
                  <tr>
                    <th class="p-2.5">Indian Ring Size</th>
                    <th class="p-2.5">Inner Diameter (mm)</th>
                    <th class="p-2.5">Circumference (mm)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-stone-200 text-[11px]">
                  <tr><td class="p-2.5 font-medium">10</td><td class="p-2.5">15.9 mm</td><td class="p-2.5">50.0 mm</td></tr>
                  <tr><td class="p-2.5 font-medium">12</td><td class="p-2.5">16.5 mm</td><td class="p-2.5">51.8 mm</td></tr>
                  <tr><td class="p-2.5 font-medium">14</td><td class="p-2.5">17.2 mm</td><td class="p-2.5">54.0 mm</td></tr>
                  <tr><td class="p-2.5 font-medium">16</td><td class="p-2.5">17.8 mm</td><td class="p-2.5">56.0 mm</td></tr>
                  <tr><td class="p-2.5 font-medium">18</td><td class="p-2.5">18.5 mm</td><td class="p-2.5">58.0 mm</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          <button onclick="window.closeSizeGuideModal()" class="w-full py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-wider font-semibold rounded-xl hover:bg-[#590D1E] transition-colors cursor-pointer">
            Close Guide
          </button>
        </div>
      `;
      document.body.appendChild(modal);
    }
    modal.classList.remove('hidden');
  };

  window.closeSizeGuideModal = function () {
    const modal = document.getElementById('size-guide-modal-root');
    if (modal) modal.classList.add('hidden');
  };

  // Track Order Modal
  window.openTrackOrderModal = function () {
    let modal = document.getElementById('track-order-modal-root');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'track-order-modal-root';
      modal.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 font-sans';
      modal.innerHTML = `
        <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex justify-between items-center border-b border-stone-200 pb-3">
            <div class="flex items-center gap-2">
              <svg class="lucide lucide-truck w-5 h-5 text-[#7A152E]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"></path><path d="M15 18H9"></path><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14v10h1"></path><circle cx="17" cy="18" r="2"></circle><circle cx="7" cy="18" r="2"></circle></svg>
              <h3 class="font-serif text-lg text-stone-900 font-bold">Track Insured Dispatch</h3>
            </div>
            <button onclick="window.closeTrackOrderModal()" class="p-1 text-stone-400 hover:text-stone-800 cursor-pointer">
              <svg class="lucide lucide-x w-5 h-5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-3 text-xs">
            <p class="text-stone-600">Enter your 10-digit Solystra Order ID or BlueDart Air Waybill (AWB) number:</p>
            <div class="flex gap-2">
              <input id="track-order-input" type="text" placeholder="e.g. SOL-98241 or 382910482" class="flex-1 px-3 py-2 border border-stone-200 rounded-xl text-xs focus:outline-none focus:border-[#7A152E]" />
              <button onclick="window.trackOrderSearch()" class="px-4 py-2 bg-[#7A152E] text-white font-semibold text-xs rounded-xl hover:bg-[#590D1E] cursor-pointer">Track</button>
            </div>
            <div id="track-order-result" class="p-3.5 bg-[#FAF8F5] rounded-xl border border-[#EAE4DC] hidden space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">IN TRANSIT &bull; ON SCHEDULE</span>
                <span class="text-[10px] text-stone-400">BlueDart Apex Express</span>
              </div>
              <div class="text-xs text-stone-800 font-medium">Estimated Delivery: Within 24-48 Business Hours</div>
              <div class="text-[11px] text-stone-500">Security: OTP-Verified Insured Handover with Tamper-Proof Holographic Seal.</div>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
    modal.classList.remove('hidden');
  };

  window.closeTrackOrderModal = function () {
    const modal = document.getElementById('track-order-modal-root');
    if (modal) modal.classList.add('hidden');
  };

  window.trackOrderSearch = function () {
    const input = document.getElementById('track-order-input');
    const res = document.getElementById('track-order-result');
    if (!input || !input.value.trim()) {
      window.showToast('Please enter an Order ID or AWB', 'Check your order confirmation email or SMS.', 'info');
      return;
    }
    if (res) res.classList.remove('hidden');
    window.showToast('Courier Verified', 'Tracking telemetry refreshed with BlueDart Express.');
  };

  // Review Modal with 5 Interactive Stars & Full Patron Submission
  let currentReviewProduct = null;
  let currentReviewRating = 5;

  const RATING_DESCRIPTIONS = {
    5: '★ 5.0 — Outstanding Luxury & Craftsmanship',
    4: '★ 4.0 — High Quality & Elegant Finish',
    3: '★ 3.0 — Satisfactory Design',
    2: '★ 2.0 — Fair / Average',
    1: '★ 1.0 — Needs Improvement'
  };

  window.openReviewModal = function (product, initialRating = 5) {
    currentReviewProduct = product || (window.PRODUCTS ? window.PRODUCTS[0] : null);
    currentReviewRating = initialRating || 5;

    let modal = document.getElementById('review-modal-root');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'review-modal-root';
      modal.className = 'fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4 font-sans';
      document.body.appendChild(modal);
    }

    modal.innerHTML = `
      <div class="bg-white rounded-2xl max-w-lg w-full p-6 sm:p-7 space-y-5 shadow-2xl border border-stone-200 animate-slide-up max-h-[92vh] overflow-y-auto no-scrollbar">
        <div class="flex justify-between items-center border-b border-stone-200 pb-3.5">
          <div>
            <span class="text-[10px] uppercase tracking-wider text-[#7A152E] font-bold block mb-0.5">Verified Patron Reflections</span>
            <h3 class="font-serif text-xl sm:text-2xl text-stone-900 font-normal">Share Patron Review</h3>
          </div>
          <button onclick="window.closeReviewModal()" class="w-8 h-8 rounded-full flex items-center justify-center text-stone-400 hover:text-stone-800 hover:bg-stone-100 transition-colors cursor-pointer">
            <svg class="lucide lucide-x w-5 h-5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
          </button>
        </div>

        <div class="flex items-center gap-3 p-3 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC]">
          <img src="${(currentReviewProduct && currentReviewProduct.images && currentReviewProduct.images[0]) || 'solystra_assets/solystra_logo.webp'}" class="w-12 h-12 rounded-lg object-cover bg-white border border-[#EAE4DC] shrink-0" alt="" />
          <div class="min-w-0 flex-1">
            <h4 class="font-semibold text-xs sm:text-sm text-stone-900 truncate">${currentReviewProduct ? currentReviewProduct.name : 'Solystra Fine Jewelry'}</h4>
            <p class="text-[11px] text-stone-500 truncate">100% Certified BIS 925 Hallmarked</p>
          </div>
        </div>

        <div class="space-y-1.5 p-3.5 rounded-xl bg-[#FAF6EE] border border-[#E8DCC4]/80">
          <label class="block text-stone-800 font-semibold text-xs uppercase tracking-wider">Overall Rating *</label>
          <div class="flex items-center gap-1.5 py-1 select-none" id="review-stars-row">
            ${[1, 2, 3, 4, 5].map(star => `
              <button type="button" data-star="${star}"
                onmouseenter="window.hoverReviewStars(${star})"
                onmouseleave="window.resetReviewStars()"
                onclick="window.selectReviewRating(${star})"
                class="review-star-btn p-1 transition-transform hover:scale-115 cursor-pointer focus:outline-none"
                title="Rate ${star} star${star > 1 ? 's' : ''}">
                <svg class="w-7 h-7 sm:w-8 sm:h-8 transition-colors ${star <= currentReviewRating ? 'text-[#C5A059] fill-[#C5A059]' : 'text-stone-300 fill-none'}" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
                </svg>
              </button>
            `).join('')}
          </div>
          <div id="review-rating-label" class="text-xs font-semibold text-[#8B6B38] font-serif pt-0.5">
            ${RATING_DESCRIPTIONS[currentReviewRating]}
          </div>
        </div>

        <div class="space-y-3 text-xs">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-stone-700 font-medium mb-1">Your Full Name *</label>
              <input id="rev-name-input" type="text" placeholder="e.g. Radhika Sharma" class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E] focus:bg-white text-xs transition-colors" />
            </div>
            <div>
              <label class="block text-stone-700 font-medium mb-1">City / Location</label>
              <input id="rev-city-input" type="text" placeholder="e.g. Mumbai, MH" class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E] focus:bg-white text-xs transition-colors" />
            </div>
          </div>

          <div>
            <label class="block text-stone-700 font-medium mb-1">Review Headline *</label>
            <input id="rev-title-input" type="text" placeholder="e.g. Immaculate Austrian stone sparkle and pure silver finish" class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E] focus:bg-white text-xs transition-colors" />
          </div>

          <div>
            <label class="block text-stone-700 font-medium mb-1">Detailed Patron Reflections *</label>
            <textarea id="rev-comment-input" rows="3" placeholder="Share your experience regarding the silver luster, chain weight, clasp comfort, or royal velvet unboxing..." class="w-full px-3.5 py-2.5 bg-stone-50 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E] focus:bg-white text-xs transition-colors"></textarea>
          </div>

          <label class="flex items-center gap-2 cursor-pointer text-stone-600 pt-1">
            <input id="rev-verified-check" type="checkbox" checked class="w-4 h-4 accent-[#7A152E] rounded cursor-pointer" />
            <span class="text-[11.5px]">Verified Solystra Patron Delivery (+100 Club Reward Points)</span>
          </label>
        </div>

        <div class="pt-2 flex gap-3">
          <button type="button" onclick="window.closeReviewModal()" class="w-1/3 py-3 border border-stone-300 text-stone-700 text-xs font-semibold rounded-xl hover:bg-stone-50 transition-colors cursor-pointer text-center">
            Cancel
          </button>
          <button type="button" onclick="window.submitReview()" class="w-2/3 py-3 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-widest rounded-xl shadow-md transition-all cursor-pointer active:scale-98 text-center flex items-center justify-center gap-2">
            <span>Publish Patron Review</span>
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
          </button>
        </div>
      </div>
    `;
    modal.classList.remove('hidden');
  };

  window.closeReviewModal = function () {
    const modal = document.getElementById('review-modal-root');
    if (modal) modal.classList.add('hidden');
  };

  window.hoverReviewStars = function (starIndex) {
    const starButtons = document.querySelectorAll('#review-stars-row button');
    starButtons.forEach((btn, idx) => {
      const svg = btn.querySelector('svg');
      if (idx < starIndex) {
        svg.setAttribute('class', 'w-7 h-7 sm:w-8 sm:h-8 transition-colors text-[#C5A059] fill-[#C5A059]');
      } else {
        svg.setAttribute('class', 'w-7 h-7 sm:w-8 sm:h-8 transition-colors text-stone-300 fill-none');
      }
    });
    const label = document.getElementById('review-rating-label');
    if (label && RATING_DESCRIPTIONS[starIndex]) {
      label.textContent = RATING_DESCRIPTIONS[starIndex];
    }
  };

  window.resetReviewStars = function () {
    window.hoverReviewStars(currentReviewRating);
  };

  window.selectReviewRating = function (rating) {
    currentReviewRating = rating;
    window.hoverReviewStars(rating);
  };

  window.submitReview = function () {
    const nameInput = document.getElementById('rev-name-input');
    const cityInput = document.getElementById('rev-city-input');
    const titleInput = document.getElementById('rev-title-input');
    const commentInput = document.getElementById('rev-comment-input');

    const name = nameInput ? nameInput.value.trim() : '';
    const city = cityInput ? cityInput.value.trim() : 'Verified Patron, India';
    const title = titleInput ? titleInput.value.trim() : 'Exceptional Handcrafted Piece';
    const comment = commentInput ? commentInput.value.trim() : '';

    if (!name) {
      window.showToast('Name Required', 'Please enter your name for the verified review.', 'info');
      if (nameInput) nameInput.focus();
      return;
    }
    if (!comment) {
      window.showToast('Review Required', 'Please write a brief reflection on your piece.', 'info');
      if (commentInput) commentInput.focus();
      return;
    }

    const prodId = currentReviewProduct ? currentReviewProduct.id : 'accent-circle-925-silver-necklace';
    const initials = name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() || 'SP';

    const newRev = {
      id: 'rev_' + Date.now(),
      author: name,
      initials: initials,
      city: city,
      title: title,
      comment: comment,
      rating: currentReviewRating,
      date: 'Just now',
      verified: true,
      helpful: 0
    };

    // Save to localStorage
    try {
      const storageKey = 'solystra_reviews_' + prodId;
      const existing = JSON.parse(localStorage.getItem(storageKey) || '[]');
      existing.unshift(newRev);
      localStorage.setItem(storageKey, JSON.stringify(existing));
    } catch (e) {
      console.warn('Could not save review to localStorage', e);
    }

    // Prepend to PDP reviews list
    const reviewsList = document.querySelector('.divide-y.divide-\\[\\#EAE4DC\\].pt-2');
    if (reviewsList) {
      const revArticle = document.createElement('article');
      revArticle.className = 'py-6 sm:py-7 space-y-3 animate-fade-in';
      revArticle.innerHTML = `
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-center gap-3 min-w-0">
            <div class="w-10 h-10 rounded-full bg-[#FAF0F2] text-[#7A152E] font-serif font-bold text-xs flex items-center justify-center shrink-0 border border-[#EAD5DA]">
              ${newRev.initials}
            </div>
            <div class="min-w-0">
              <div class="flex flex-wrap items-center gap-1.5">
                <span class="font-medium text-stone-900 text-sm">${newRev.author}</span>
                <span class="inline-flex items-center gap-1 text-[10px] font-semibold text-[#8B6B38] bg-[#FAF6EE] px-2 py-0.5 rounded-full border border-[#E8DCC4] shrink-0">
                  <svg class="lucide lucide-shield-check w-2.5 h-2.5 text-[#C5A059]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path></svg>
                  <span>Verified Patron</span>
                </span>
              </div>
              <div class="text-[11px] text-stone-400 mt-0.5 flex items-center gap-2">
                <span>${newRev.city}</span>
                <span>•</span>
                <span class="text-[#7A152E] font-medium">${newRev.date}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <div class="flex items-center gap-0.5">
            ${[...Array(5)].map((_, i) => `
              <svg class="w-3.5 h-3.5 ${i < newRev.rating ? 'text-[#C5A059] fill-[#C5A059]' : 'text-stone-300 fill-none'}" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"></path>
              </svg>
            `).join('')}
          </div>
          <h5 class="font-semibold text-stone-900 text-xs sm:text-sm">${newRev.title}</h5>
        </div>
        <p class="text-xs sm:text-[13px] text-stone-600 leading-relaxed font-light">${newRev.comment}</p>
      `;
      reviewsList.insertBefore(revArticle, reviewsList.firstChild);
    }

    window.closeReviewModal();
    window.showToast('Patron Review Published!', 'Thank you! Your verified reflection is now live for all atelier patrons.');
  };

  // Lightbox Magnifier Fullscreen Modal
  let lightboxCurrentIndex = 0;
  let lightboxImages = [];
  let lightboxZoomLevel = 1;

  window.openImageLightbox = function (initialSrc, product) {
    if (!product && window.PRODUCTS) {
      const params = new URLSearchParams(window.location.search);
      const prodId = params.get('id');
      product = window.PRODUCTS.find(p => p.id === prodId) || window.PRODUCTS[0];
    }
    lightboxImages = (product && product.images && product.images.length > 0)
      ? product.images
      : [initialSrc || 'solystra_assets/solystra_logo.webp'];

    lightboxCurrentIndex = Math.max(0, lightboxImages.indexOf(initialSrc));
    lightboxZoomLevel = 1;

    let lb = document.getElementById('pdp-lightbox-modal');
    if (!lb) {
      lb = document.createElement('div');
      lb.id = 'pdp-lightbox-modal';
      lb.className = 'fixed inset-0 z-50 bg-black/95 backdrop-blur-md flex flex-col justify-between p-3 sm:p-6 text-white font-sans select-none';
      document.body.appendChild(lb);
    }

    function renderLightbox() {
      const currentImg = lightboxImages[lightboxCurrentIndex] || lightboxImages[0];
      const prodName = product ? product.name : 'Solystra Fine Jewelry Atelier';

      lb.innerHTML = `
        <div class="flex items-center justify-between border-b border-white/10 pb-3 z-20">
          <div class="min-w-0 pr-4">
            <h3 class="font-serif text-base sm:text-lg text-white font-normal truncate">${prodName}</h3>
            <span class="text-[11px] text-[#EAD7AE] font-mono">Angle ${lightboxCurrentIndex + 1} of ${lightboxImages.length} • 100% Certified 925 Hallmark</span>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button onclick="window.zoomLightbox(0.25)" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors cursor-pointer text-sm font-bold" title="Zoom In">+</button>
            <button onclick="window.zoomLightbox(-0.25)" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors cursor-pointer text-sm font-bold" title="Zoom Out">-</button>
            <button onclick="window.resetLightboxZoom()" class="px-2.5 py-1 rounded-full bg-white/10 hover:bg-white/20 text-[11px] text-white transition-colors cursor-pointer font-mono" title="Reset Zoom">Reset</button>
            <button onclick="window.closeImageLightbox()" class="w-9 h-9 rounded-full bg-[#7A152E] hover:bg-[#590D1E] flex items-center justify-center text-white transition-colors cursor-pointer ml-1" title="Close Lightbox (Esc)">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
        </div>

        <div class="relative flex-1 flex items-center justify-center overflow-hidden my-2" onclick="if(event.target === this) window.closeImageLightbox()">
          <button onclick="window.prevLightboxImage(event)" class="absolute left-2 sm:left-4 z-20 w-11 h-11 rounded-full bg-black/60 hover:bg-[#7A152E] border border-white/20 flex items-center justify-center text-white transition-all cursor-pointer shadow-xl active:scale-95" title="Previous Angle (Left Arrow)">
            <svg class="w-5 h-5 -translate-x-px" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"></path></svg>
          </button>

          <div class="relative max-h-[75vh] max-w-[85vw] flex items-center justify-center overflow-hidden">
            <img id="lightbox-main-img" src="${currentImg}" alt="${prodName}"
              style="transform: scale(${lightboxZoomLevel}); transition: transform 0.25s ease;"
              class="max-h-[75vh] max-w-[85vw] object-contain rounded-xl shadow-2xl cursor-zoom-in"
              onclick="window.toggleLightboxZoom()" />
          </div>

          <button onclick="window.nextLightboxImage(event)" class="absolute right-2 sm:right-4 z-20 w-11 h-11 rounded-full bg-black/60 hover:bg-[#7A152E] border border-white/20 flex items-center justify-center text-white transition-all cursor-pointer shadow-xl active:scale-95" title="Next Angle (Right Arrow)">
            <svg class="w-5 h-5 translate-x-px" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"></path></svg>
          </button>
        </div>

        <div class="flex items-center justify-center gap-2 pt-2 border-t border-white/10 z-20 overflow-x-auto no-scrollbar">
          ${lightboxImages.map((src, i) => `
            <button onclick="window.selectLightboxIndex(${i})" class="relative w-14 h-14 sm:w-16 sm:h-16 rounded-xl overflow-hidden border-2 transition-all cursor-pointer shrink-0 ${i === lightboxCurrentIndex ? 'border-[#C5A059] ring-2 ring-[#C5A059]/40 scale-105' : 'border-white/20 opacity-60 hover:opacity-100'}">
              <img src="${src}" class="w-full h-full object-cover" alt="Angle ${i + 1}" />
            </button>
          `).join('')}
        </div>
      `;
      lb.classList.remove('hidden');
    }

    window.closeImageLightbox = function () {
      if (lb) lb.classList.add('hidden');
      lightboxZoomLevel = 1;
    };

    window.prevLightboxImage = function (e) {
      if (e) e.stopPropagation();
      lightboxCurrentIndex = (lightboxCurrentIndex - 1 + lightboxImages.length) % lightboxImages.length;
      lightboxZoomLevel = 1;
      renderLightbox();
    };

    window.nextLightboxImage = function (e) {
      if (e) e.stopPropagation();
      lightboxCurrentIndex = (lightboxCurrentIndex + 1) % lightboxImages.length;
      lightboxZoomLevel = 1;
      renderLightbox();
    };

    window.selectLightboxIndex = function (idx) {
      lightboxCurrentIndex = idx;
      lightboxZoomLevel = 1;
      renderLightbox();
    };

    window.zoomLightbox = function (delta) {
      lightboxZoomLevel = Math.min(3, Math.max(0.75, lightboxZoomLevel + delta));
      const img = document.getElementById('lightbox-main-img');
      if (img) img.style.transform = `scale(${lightboxZoomLevel})`;
    };

    window.resetLightboxZoom = function () {
      lightboxZoomLevel = 1;
      const img = document.getElementById('lightbox-main-img');
      if (img) img.style.transform = 'scale(1)';
    };

    window.toggleLightboxZoom = function () {
      lightboxZoomLevel = lightboxZoomLevel > 1.2 ? 1 : 2;
      const img = document.getElementById('lightbox-main-img');
      if (img) img.style.transform = `scale(${lightboxZoomLevel})`;
    };

    function handleKeyDown(e) {
      if (lb.classList.contains('hidden')) return;
      if (e.key === 'Escape') window.closeImageLightbox();
      else if (e.key === 'ArrowLeft') window.prevLightboxImage();
      else if (e.key === 'ArrowRight') window.nextLightboxImage();
      else if (e.key === '+' || e.key === '=') window.zoomLightbox(0.25);
      else if (e.key === '-') window.zoomLightbox(-0.25);
    }
    window.removeEventListener('keydown', handleKeyDown);
    window.addEventListener('keydown', handleKeyDown);

    renderLightbox();
  };

  // Mobile Filter Drawer Modal for Catalog
  window.openMobileFilterModal = function () {
    let m = document.getElementById('mobile-filter-modal');
    if (!m) {
      m = document.createElement('div');
      m.id = 'mobile-filter-modal';
      m.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-end sm:items-center justify-center font-sans';
      m.innerHTML = `
        <div class="bg-white w-full max-w-lg rounded-t-3xl sm:rounded-2xl p-6 space-y-4 max-h-[85vh] overflow-y-auto no-scrollbar shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex items-center justify-between pb-3 border-b border-stone-200">
            <h3 class="font-serif text-lg font-normal text-stone-900">Filter Atelier Creations</h3>
            <button onclick="window.closeMobileFilterModal()" class="p-1 text-stone-400 hover:text-stone-800">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-4 text-xs">
            <div>
              <span class="font-bold text-stone-800 uppercase tracking-wider block mb-2">Category</span>
              <div class="grid grid-cols-2 gap-2" id="mobile-filter-categories">
                <button type="button" onclick="window.applyMobileCategory('all')" class="p-2 rounded-xl border border-[#7A152E] bg-[#FAF0F2] text-[#7A152E] font-semibold text-center">All Creations</button>
                <button type="button" onclick="window.applyMobileCategory('bracelets')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Bracelets & Kadas</button>
                <button type="button" onclick="window.applyMobileCategory('necklaces')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Necklaces & Pendants</button>
                <button type="button" onclick="window.applyMobileCategory('rings')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Rings & Bands</button>
                <button type="button" onclick="window.applyMobileCategory('earrings')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Earrings & Studs</button>
                <button type="button" onclick="window.applyMobileCategory('complete_sets')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Gift Sets & Suites</button>
              </div>
            </div>
            <div>
              <span class="font-bold text-stone-800 uppercase tracking-wider block mb-2">Precious Finish</span>
              <div class="grid grid-cols-2 gap-2" id="mobile-filter-metals">
                <button type="button" onclick="window.applyMobileMetal('all')" class="p-2 rounded-xl border border-[#7A152E] bg-[#FAF0F2] text-[#7A152E] font-semibold text-center">All Finishes</button>
                <button type="button" onclick="window.applyMobileMetal('silver')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">Pure 925 Silver</button>
                <button type="button" onclick="window.applyMobileMetal('gold')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">18K Gold Vermeil</button>
                <button type="button" onclick="window.applyMobileMetal('rose')" class="p-2 rounded-xl border border-stone-200 hover:border-[#7A152E] text-stone-800 font-medium text-center">18K Rose Gold</button>
              </div>
            </div>
          </div>
          <div class="pt-3 flex gap-2">
            <button type="button" onclick="window.resetCatalogFilters(); window.closeMobileFilterModal();" class="w-1/2 py-2.5 border border-stone-300 rounded-xl text-xs font-semibold text-stone-700">Reset Filters</button>
            <button type="button" onclick="window.closeMobileFilterModal()" class="w-1/2 py-2.5 bg-[#7A152E] text-white rounded-xl text-xs font-bold uppercase tracking-wider">Apply Filters</button>
          </div>
        </div>
      `;
      document.body.appendChild(m);
    }
    m.classList.remove('hidden');
  };

  window.closeMobileFilterModal = function () {
    const m = document.getElementById('mobile-filter-modal');
    if (m) m.classList.add('hidden');
  };

  window.applyMobileCategory = function (cat) {
    const params = new URLSearchParams(window.location.search);
    params.set('category', cat);
    window.location.search = params.toString();
  };

  window.applyMobileMetal = function (metal) {
    const params = new URLSearchParams(window.location.search);
    params.set('metal', metal);
    window.location.search = params.toString();
  };

  // Size Guide Modal
  window.openSizeGuideModal = function () {
    let m = document.getElementById('size-guide-modal-root');
    if (!m) {
      m = document.createElement('div');
      m.id = 'size-guide-modal-root';
      m.className = 'fixed inset-0 z-50 bg-black/75 backdrop-blur-xs flex items-center justify-center p-4 font-sans';
      m.innerHTML = `
        <div class="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-stone-200 animate-slide-up max-h-[90vh] overflow-y-auto no-scrollbar">
          <div class="flex justify-between items-center border-b border-stone-200 pb-3">
            <div>
              <span class="text-[10px] uppercase tracking-wider text-[#7A152E] font-bold block mb-0.5">Atelier Fit Assurance</span>
              <h3 class="font-serif text-xl text-stone-900 font-normal">Fine Jewelry Sizing Guide</h3>
            </div>
            <button onclick="document.getElementById('size-guide-modal-root').classList.add('hidden')" class="p-1 text-stone-400 hover:text-stone-800 cursor-pointer">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-4 text-xs">
            <div>
              <h5 class="font-semibold text-stone-900 mb-2">Ring Sizing Chart (Indian Standard)</h5>
              <div class="grid grid-cols-3 gap-2 text-center text-[11px]">
                <div class="p-2 bg-stone-50 rounded-lg border border-stone-200 font-medium">Size 10 • 15.7 mm</div>
                <div class="p-2 bg-stone-50 rounded-lg border border-stone-200 font-medium">Size 12 • 16.5 mm</div>
                <div class="p-2 bg-stone-50 rounded-lg border border-stone-200 font-medium">Size 14 • 17.3 mm</div>
                <div class="p-2 bg-stone-50 rounded-lg border border-stone-200 font-medium">Size 16 • 18.1 mm</div>
                <div class="p-2 bg-stone-50 rounded-lg border border-stone-200 font-medium">Size 18 • 18.9 mm</div>
                <div class="p-2 bg-[#FAF0F2] text-[#7A152E] rounded-lg border border-[#7A152E]/30 font-semibold">Adjustable Fit</div>
              </div>
            </div>
            <div class="p-3 bg-[#FAF8F5] rounded-xl border border-[#EAE4DC] space-y-1">
              <span class="font-semibold text-stone-900 block">How to Measure at Home:</span>
              <p class="text-stone-600 leading-relaxed font-light">Wrap a strip of paper around the base of your finger. Mark where the paper overlaps and measure the millimeters with a ruler. All Solystra rings include complimentary size exchanges within 15 days.</p>
            </div>
          </div>
          <button onclick="document.getElementById('size-guide-modal-root').classList.add('hidden')" class="w-full py-2.5 bg-[#7A152E] text-white text-xs font-semibold uppercase tracking-wider rounded-xl cursor-pointer">Close Sizing Guide</button>
        </div>
      `;
      document.body.appendChild(m);
    }
    m.classList.remove('hidden');
  };

    // Ask Question Modal
  window.openAskQuestionModal = function (product) {
    let modal = document.getElementById('ask-question-modal-root');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'ask-question-modal-root';
      modal.className = 'fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4 font-sans';
      modal.innerHTML = `
        <div class="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-stone-200 animate-slide-up">
          <div class="flex justify-between items-center border-b border-stone-200 pb-3">
            <h3 class="font-serif text-lg text-stone-900 font-normal">Ask Concierge Desk</h3>
            <button onclick="window.closeAskQuestionModal()" class="p-1 text-stone-400 hover:text-stone-800 cursor-pointer">
              <svg class="lucide lucide-x w-5 h-5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M18 6 6 18"></path><path d="m6 6 12 12"></path></svg>
            </button>
          </div>
          <div class="space-y-3 text-xs">
            <div>
              <label class="block text-stone-700 font-medium mb-1">Your Email or Mobile</label>
              <input id="q-contact-input" type="text" placeholder="care@solystrajewels.com or +91 98..." class="w-full px-3 py-2 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E]" />
            </div>
            <div>
              <label class="block text-stone-700 font-medium mb-1">Inquiry Category</label>
              <select class="w-full px-3 py-2 border border-stone-200 rounded-xl bg-white text-stone-800 focus:outline-none focus:border-[#7A152E]">
                <option>Custom Ring/Wrist Sizing</option>
                <option>Laser Engraving Consultation</option>
                <option>BIS Hallmarking Verification</option>
                <option>Express Delivery Speed</option>
              </select>
            </div>
            <div>
              <label class="block text-stone-700 font-medium mb-1">Your Question</label>
              <textarea id="q-msg-input" rows="3" placeholder="Ask about metal finish, stone settings, custom gifts..." class="w-full px-3 py-2 border border-stone-200 rounded-xl focus:outline-none focus:border-[#7A152E]"></textarea>
            </div>
          </div>
          <button onclick="window.submitQuestion()" class="w-full py-2.5 bg-[#7A152E] text-white text-xs uppercase tracking-wider font-semibold rounded-xl hover:bg-[#590D1E] transition-colors cursor-pointer">
            Send Inquiry to Atelier
          </button>
        </div>
      `;
      document.body.appendChild(modal);
    }
    modal.classList.remove('hidden');
  };

  window.closeAskQuestionModal = function () {
    const modal = document.getElementById('ask-question-modal-root');
    if (modal) modal.classList.add('hidden');
  };

  window.submitQuestion = function () {
    const msg = document.getElementById('q-msg-input');
    if (!msg || !msg.value.trim()) {
      window.showToast('Please enter your inquiry', 'Describe your question for the atelier gemologist.', 'info');
      return;
    }
    window.closeAskQuestionModal();
    window.showToast('Inquiry Transmitted', 'Solystra luxury concierge will reply within 4 business hours.');
    if (msg) msg.value = '';
  };


  // Hook into DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(initFooterAccordions, 100);
    setTimeout(initTopCollectionsCoverflow, 50);
    setTimeout(initMotionReelsVideos, 100);
    setTimeout(initStylingCombos, 150);
    setTimeout(initProductCarousels, 200);
  });


  /* ==========================================================================
     PDP INTERACTIVE ENGINE (1:1 Complete Parity with React)
     - Desktop Details 5-Tab Switcher
     - Mobile Accordions
     - Reviews Filter (All, 5-Star, 4-Star)
     - Reviews Sort (Helpful, Highest, Lowest, Recent)
     - Reviews Helpful Like Counter
     - Reviews Read More / Read Less Expander
     - Reviews Report
     - Write Review Star Rating (1..N Gold Highlighting)
     - Floating Mobile Capsule CTA (Scroll-triggered Add to Cart & Buy Now)
     - PDP Add to Bag & Buy Now Handlers
     - PDP Wishlist Toggle with Header Badge sync
     - Luxury Atelier Boutiques Modal (Flagship Boutiques)
     - Global Newsletter Privilege Code (SOULY10 toast & clipboard)
     ========================================================================== */

  // 1. Desktop Tab Switcher
  window.switchPdpTab = function (tabIdx) {
    const tabHeaders = document.querySelectorAll('#pdp-tabs-header button, .hidden.md\\:grid.grid-cols-5 button');
    const contentContainer = document.getElementById('pdp-desktop-tab-content') || document.querySelector('.hidden.md\\:block.p-6.sm\\:p-10');

    if (tabHeaders.length > 0) {
      tabHeaders.forEach((b, i) => {
        if (i === tabIdx) {
          b.className = 'py-4 px-2 lg:px-3 text-[11px] lg:text-xs uppercase tracking-wider transition-all text-center cursor-pointer border-r border-stone-200 last:border-r-0 border-b-2 border-b-[#7A152E] text-[#7A152E] bg-white font-bold shadow-2xs';
        } else {
          b.className = 'py-4 px-2 lg:px-3 text-[11px] lg:text-xs uppercase tracking-wider transition-all text-center cursor-pointer border-r border-stone-200 last:border-r-0 text-stone-500 hover:text-stone-900 hover:bg-stone-100/60 font-medium';
        }
      });
    }

    if (!contentContainer) return;

    // Get active product details if available
    let currentProd = null;
    const urlParams = new URLSearchParams(window.location.search);
    const pId = urlParams.get('id');
    if (window.PRODUCTS && window.PRODUCTS.length > 0) {
      currentProd = window.PRODUCTS.find(p => p.id === pId) || window.PRODUCTS[0];
    }
    const specs = (currentProd && currentProd.specs) || {};

    const panels = [
      // Tab 0: Specifications & Purity
      `
      <div class="space-y-4 animate-fade-in font-sans">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
          <h3 class="font-serif text-2xl text-stone-900 font-normal">Certified Craftsmanship Specifications</h3>
          <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">BIS 925 Hallmark Verified</span>
        </div>
        <p class="text-xs text-stone-500 font-light mb-4">Every Solystra creation is individually hallmarked and micro-set in pure 925 sterling silver.</p>
        <div id="pdp-specs-grid" class="grid grid-cols-1 md:grid-cols-2 gap-3.5 sm:gap-4 text-xs">
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Metal Purity</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Metal Purity'] || 'BIS Certified 925 Sterling Silver'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Plating Finish</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Plating Finish'] || 'Anti-Tarnish Rhodium & Micron E-Coat'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Stone Setting</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Stone Setting'] || 'AAA+ Austrian Solitaire Crystals'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Hallmark Verification</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Hallmark Verification'] || 'Certified 925 Stamp on Clasp/Band'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Warranty Coverage</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Warranty Coverage'] || '6 Months Free Replating Assurance'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors">
            <span class="text-stone-500 font-medium text-xs">Packaging</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Packaging'] || 'Luxury Suede Box with Authenticity Card'}</span>
          </div>
          <div class="flex justify-between items-center p-3.5 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-stone-300 transition-colors col-span-1 md:col-span-2">
            <span class="text-stone-500 font-medium text-xs">Shipping</span>
            <span class="font-semibold text-stone-800 text-xs sm:text-[13px] text-right ml-2">${specs['Shipping'] || 'Free Insured Express Delivery Across India'}</span>
          </div>
        </div>
      </div>`,

      // Tab 1: Shipping & Details
      `
      <div class="space-y-5 animate-fade-in font-sans text-xs text-stone-700">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
          <h3 class="font-serif text-2xl text-stone-900 font-normal">Express Insured Courier & Seamless Returns</h3>
          <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">BlueDart Express Air</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <div class="flex items-center gap-2 text-stone-900 font-semibold text-sm">
              <svg class="w-4 h-4 text-[#7A152E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>24-48 Hr Dispatch</span>
            </div>
            <p class="text-stone-600 leading-relaxed font-light">Every creation undergoes a 7-point microscopic quality inspection and hallmarking verification before immediate dispatch.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <div class="flex items-center gap-2 text-stone-900 font-semibold text-sm">
              <svg class="w-4 h-4 text-[#7A152E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
              <span>Transit Insurance</span>
            </div>
            <p class="text-stone-600 leading-relaxed font-light">100% door-to-door transit coverage. In the rare event of transit damage or delay, replacement or full refund is expedited.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <div class="flex items-center gap-2 text-stone-900 font-semibold text-sm">
              <svg class="w-4 h-4 text-[#7A152E]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
              <span>15-Day Easy Returns</span>
            </div>
            <p class="text-stone-600 leading-relaxed font-light">Complimentary doorstep pickup across 19,000+ PIN codes with full refund to original payment source within 48 hours.</p>
          </div>
        </div>
      </div>`,

      // Tab 2: Jewelry Care Guide
      `
      <div class="space-y-5 animate-fade-in font-sans text-xs text-stone-700">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
          <h3 class="font-serif text-2xl text-stone-900 font-normal">Preserving Your Atelier Radiance</h3>
          <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Lifelong Silver Preservation</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">The "Last On, First Off" Rule</h5>
            <p class="text-stone-600 leading-relaxed font-light">Always wear your jewelry after applying makeup, perfumes, and lotions. Remove before swimming, showers, or intensive workouts to preserve the dual-micron rhodium shield.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">Signature Microfiber Buffing</h5>
            <p class="text-stone-600 leading-relaxed font-light">Gently polish stones and bands using the enclosed Solystra suede polishing cloth. Avoid abrasive chemical dips or ultrasonic bath solutions.</p>
          </div>
        </div>
      </div>`,

      // Tab 3: Packaging & Gifting
      `
      <div class="space-y-5 animate-fade-in font-sans text-xs text-stone-700">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
          <h3 class="font-serif text-2xl text-stone-900 font-normal">The Royal Solystra Unboxing Experience</h3>
          <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Complimentary Keepsake Vault</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">Burgundy Suede Vault</h5>
            <p class="text-stone-600 leading-relaxed font-light">Custom fitted plush velvet interior with anti-tarnish micro-cushioning and embossed gold foil branding.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">Embossed Purity Certificate</h5>
            <p class="text-stone-600 leading-relaxed font-light">Individual serial certificate confirming BIS hallmarked 925 sterling silver purity and Austrian crystal grade.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">Gift Ready Presentation</h5>
            <p class="text-stone-600 leading-relaxed font-light">Delivered in a rigid satin-ribbon gift carrier bag with a personalized handwritten greeting card upon request.</p>
          </div>
        </div>
      </div>`,

      // Tab 4: Warranty & Authenticity
      `
      <div class="space-y-5 animate-fade-in font-sans text-xs text-stone-700">
        <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 mb-2">
          <h3 class="font-serif text-2xl text-stone-900 font-normal">Authenticity & 6-Month Plating Warranty</h3>
          <span class="text-[11px] text-[#7A152E] font-semibold uppercase tracking-wider">Hallmark Certified</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">BIS 925 Hallmark Guarantee</h5>
            <p class="text-stone-600 leading-relaxed font-light">Bureau of Indian Standards certified pure silver content (92.5%). Every item carries the official triangular BIS stamp and Solystra atelier hallmark punch.</p>
          </div>
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#EAE4DC] space-y-2">
            <h5 class="font-semibold text-stone-900 text-sm">6 Months Free Replating</h5>
            <p class="text-stone-600 leading-relaxed font-light">Should your creation encounter unexpected tarnish or surface discoloration within 6 months, we replating and service your piece with complimentary reverse courier pickup.</p>
          </div>
        </div>
      </div>`
    ];

    contentContainer.innerHTML = panels[tabIdx] || panels[0];
  };

  // 2. Reviews Filter (All, 5-Star, 4-Star)
  window.filterPdpReviews = function (ratingScore, btn) {
    const filterButtons = document.querySelectorAll('#reviews-filter-bar button, .flex.items-center.gap-2.overflow-x-auto button');
    filterButtons.forEach(b => {
      b.className = 'px-3 py-1 rounded-full text-xs font-medium transition-all whitespace-nowrap cursor-pointer shrink-0 bg-[#FAF8F5] text-stone-700 border border-[#EAE4DC] hover:border-[#7A152E]/30';
    });
    if (btn) {
      btn.className = 'px-3 py-1 rounded-full text-xs font-medium transition-all whitespace-nowrap cursor-pointer shrink-0 bg-[#7A152E] text-white shadow-2xs';
    }

    const reviewsList = document.getElementById('pdp-reviews-list') || document.querySelector('.divide-y.divide-stone-200.pt-2') || document.querySelector('.divide-y.divide-\\[\\#EAE4DC\\].pt-2');
    if (!reviewsList) return;

    const articles = reviewsList.querySelectorAll('article');
    let visibleCount = 0;
    articles.forEach(art => {
      const artRating = art.getAttribute('data-rating') || '5';
      if (ratingScore === 'all' || artRating === String(ratingScore)) {
        art.style.display = 'block';
        visibleCount++;
      } else {
        art.style.display = 'none';
      }
    });

    const msg = ratingScore === 'all' ? `Displaying all ${visibleCount} patron reflections` : `Filtered to ${ratingScore}-Star reviews (${visibleCount})`;
    window.showToast('Patron Reviews Filtered', msg, 'info');
  };

  // 3. Reviews Sort Menu & Sorter
  window.toggleReviewsSortMenu = function () {
    const menu = document.getElementById('reviews-sort-menu');
    if (menu) {
      menu.classList.toggle('hidden');
    }
  };

  // Close sort menu on click outside
  document.addEventListener('click', function (e) {
    const sortBtn = document.getElementById('reviews-sort-btn');
    const sortMenu = document.getElementById('reviews-sort-menu');
    if (sortBtn && sortMenu && !sortBtn.contains(e.target) && !sortMenu.contains(e.target)) {
      sortMenu.classList.add('hidden');
    }
  });

  window.sortPdpReviews = function (mode, label) {
    const labelEl = document.getElementById('reviews-sort-label');
    if (labelEl) labelEl.textContent = label;

    const menu = document.getElementById('reviews-sort-menu');
    if (menu) menu.classList.add('hidden');

    const reviewsList = document.getElementById('pdp-reviews-list') || document.querySelector('.divide-y.divide-stone-200.pt-2') || document.querySelector('.divide-y.divide-\\[\\#EAE4DC\\].pt-2');
    if (!reviewsList) return;

    const articles = Array.from(reviewsList.querySelectorAll('article'));
    if (articles.length === 0) return;

    articles.sort((a, b) => {
      if (mode === 'helpful') {
        const getHelpful = (el) => {
          const btn = el.querySelector('button');
          if (!btn) return 0;
          const match = btn.textContent.match(/\d+/);
          return match ? parseInt(match[0], 10) : 0;
        };
        return getHelpful(b) - getHelpful(a);
      } else if (mode === 'highest') {
        const rA = parseInt(a.getAttribute('data-rating') || '5', 10);
        const rB = parseInt(b.getAttribute('data-rating') || '5', 10);
        return rB - rA;
      } else if (mode === 'lowest') {
        const rA = parseInt(a.getAttribute('data-rating') || '5', 10);
        const rB = parseInt(b.getAttribute('data-rating') || '5', 10);
        return rA - rB;
      }
      return 0; // Recent - preserve DOM order
    });

    articles.forEach(art => reviewsList.appendChild(art));
    window.showToast('Reviews Sorted', `Ordered by ${label}`);
  };

  // 4. Review Helpful Like Toggle
  window.toggleReviewHelpful = function (btn) {
    if (!btn) return;
    const isLiked = btn.getAttribute('data-liked') === 'true';
    const match = btn.textContent.match(/\d+/);
    let count = match ? parseInt(match[0], 10) : 20;

    if (!isLiked) {
      count++;
      btn.setAttribute('data-liked', 'true');
      btn.classList.add('text-[#7A152E]', 'border-[#7A152E]', 'bg-[#FAF0F2]', 'font-bold');
      btn.innerHTML = `
        <svg class="w-3.5 h-3.5 fill-[#7A152E] text-[#7A152E] shrink-0" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M7 10v12"></path><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"></path></svg>
        <span>Helpful (${count})</span>
      `;
      window.showToast('Feedback Recorded', 'Thank you for supporting our patron community!');
    } else {
      count = Math.max(0, count - 1);
      btn.removeAttribute('data-liked');
      btn.classList.remove('text-[#7A152E]', 'border-[#7A152E]', 'bg-[#FAF0F2]', 'font-bold');
      btn.innerHTML = `
        <svg class="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M7 10v12"></path><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"></path></svg>
        <span>Helpful (${count})</span>
      `;
    }
  };

  // 5. Review Read More / Read Less Expander
  window.toggleReviewReadMore = function (btn) {
    if (!btn) return;
    const pTag = btn.closest('p');
    if (!pTag) return;

    if (!pTag.hasAttribute('data-original-html')) {
      pTag.setAttribute('data-original-html', pTag.innerHTML);
    }

    const isExpanded = btn.getAttribute('data-expanded') === 'true';
    if (!isExpanded) {
      // Expanded state: replace ellipsis with full text
      const fullText = pTag.getAttribute('data-full-text') || pTag.textContent.replace('Read more', '').replace('Read less', '').trim();
      pTag.innerHTML = `"${fullText} The craftsmanship and polish are truly equivalent to high jewelry boutiques in Milan and Paris." <button onclick="window.toggleReviewReadMore(this)" data-expanded="true" class="text-[#7A152E] hover:underline font-semibold ml-1 cursor-pointer">Read less</button>`;
    } else {
      // Collapse back
      const orig = pTag.getAttribute('data-original-html');
      pTag.innerHTML = orig;
    }
  };

  // 6. Report Review Handler
  window.reportReview = function (btn) {
    window.showToast('Patron Reflection Flagged', 'Review reported for verification by the Solystra curator team.');
  };

  // 7. PDP Primary Action Handlers (Add to Bag & Buy Now)
  function getActiveProduct() {
    const urlParams = new URLSearchParams(window.location.search);
    const pId = urlParams.get('id');
    if (window.PRODUCTS && window.PRODUCTS.length > 0) {
      return window.PRODUCTS.find(p => p.id === pId) || window.PRODUCTS[0];
    }
    return {
      id: 'accent-circle-925-silver-necklace',
      name: 'Accent Circle 925 Silver Necklace',
      price: 2798,
      mrp: 3861,
      image: 'solystra_assets/products/accent-circle-925-silver-necklace/angle_1.webp',
      metal: 'Pure 925 Silver'
    };
  }

  window.handlePdpAddToCart = function () {
    const product = getActiveProduct();
    const selMetal = document.getElementById('pdp-selected-metal-name')?.textContent || 'Pure 925 Silver';
    window.addToCart(product, selMetal);
    window.openCartDrawer();
  };

  window.handlePdpBuyNow = function () {
    const product = getActiveProduct();
    const selMetal = document.getElementById('pdp-selected-metal-name')?.textContent || 'Pure 925 Silver';
    window.addToCart(product, selMetal);
    window.location.href = 'checkout.html';
  };

  window.handlePdpWishlistToggle = function (btn) {
    const product = getActiveProduct();
    window.toggleWishlist(product);
    if (btn) {
      const svg = btn.querySelector('svg');
      if (svg) {
        const inW = window.isInWishlist(product.id);
        if (inW) {
          svg.setAttribute('class', 'w-4 h-4 text-[#7A152E] fill-[#7A152E] transition-all scale-110');
          btn.classList.add('bg-[#FAF0F2]', 'text-[#7A152E]');
        } else {
          svg.setAttribute('class', 'w-4 h-4 text-stone-700 fill-none transition-all scale-100');
          btn.classList.remove('bg-[#FAF0F2]', 'text-[#7A152E]');
        }
      }
    }
  };

  // 8. Floating Mobile Capsule CTA Handlers
  window.handleCapsuleAddToCart = function () {
    window.handlePdpAddToCart();
  };

  window.handleCapsuleBuyNow = function () {
    window.handlePdpBuyNow();
  };

  // Floating capsule scroll listener
  window.addEventListener('scroll', function () {
    const capsule = document.getElementById('floating-capsule-cta');
    if (!capsule) return;

    if (window.scrollY > 220) {
      capsule.classList.remove('translate-y-20', 'scale-90', 'opacity-0', 'pointer-events-none');
      capsule.classList.add('translate-y-0', 'scale-100', 'opacity-100', 'pointer-events-auto');
    } else {
      capsule.classList.add('translate-y-20', 'scale-90', 'opacity-0', 'pointer-events-none');
      capsule.classList.remove('translate-y-0', 'scale-100', 'opacity-100', 'pointer-events-auto');
    }
  }, { passive: true });

  // 9. Luxury Atelier Boutique Modal
  window.openBoutiqueModal = function () {
    let modal = document.getElementById('boutique-modal-root');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'boutique-modal-root';
      modal.className = 'fixed inset-0 z-50 overflow-y-auto bg-black/75 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 font-sans';
      document.body.appendChild(modal);
    }

    modal.innerHTML = `
      <div class="bg-white rounded-3xl max-w-4xl w-full p-6 sm:p-8 shadow-2xl border border-stone-200 animate-slide-up max-h-[92vh] overflow-y-auto no-scrollbar space-y-6">
        <div class="flex items-center justify-between border-b border-[#EAE4DC] pb-4">
          <div>
            <span class="text-[10px] uppercase tracking-widest text-[#7A152E] font-bold block mb-1">Solystra Flagship Boutiques</span>
            <h3 class="font-serif text-2xl sm:text-3xl text-stone-900 font-normal">Visit Our Ateliers</h3>
          </div>
          <button onclick="window.closeBoutiqueModal()" class="w-9 h-9 rounded-full flex items-center justify-center text-stone-400 hover:text-stone-800 hover:bg-stone-100 transition-colors cursor-pointer">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
          </button>
        </div>

        <p class="text-xs text-stone-600 font-light">Experience the brilliance of BIS 925 sterling silver and 18K gold creations in person. Complimentary private styling consultations, ultrasonic jewelry cleaning, and custom bespoke sizing.</p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
          <!-- Delhi Flagship -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">New Delhi</span>
              <a href="https://maps.google.com/?q=DLF+Emporio+Vasant+Kunj+New+Delhi" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">DLF Emporio Flagship</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">Ground Floor, 4 Nelson Mandela Marg, Vasant Kunj, New Delhi 110070</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 11:00 AM - 9:00 PM</span>
              <a href="tel:+911149202200" class="hover:text-[#7A152E] font-medium">+91 11 4920 2200</a>
            </div>
          </div>

          <!-- Mumbai Bandra -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">Mumbai</span>
              <a href="https://maps.google.com/?q=Waterfield+Road+Bandra+West+Mumbai" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">Bandra West Studio</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">Plot 42, Waterfield Road, Bandra West, Mumbai 400050</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 11:00 AM - 9:00 PM</span>
              <a href="tel:+912226408820" class="hover:text-[#7A152E] font-medium">+91 22 2640 8820</a>
            </div>
          </div>

          <!-- Bengaluru Indiranagar -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">Bengaluru</span>
              <a href="https://maps.google.com/?q=100+Feet+Road+Indiranagar+Bengaluru" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">Indiranagar Galleria</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">100 Feet Road, HAL 2nd Stage, Indiranagar, Bengaluru 560038</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 10:30 AM - 8:30 PM</span>
              <a href="tel:+918041223340" class="hover:text-[#7A152E] font-medium">+91 80 4122 3340</a>
            </div>
          </div>

          <!-- Hyderabad Jubilee Hills -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">Hyderabad</span>
              <a href="https://maps.google.com/?q=Road+No+36+Jubilee+Hills+Hyderabad" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">Jubilee Hills Atelier</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">Road No. 36, Near Peddamma Temple, Jubilee Hills, Hyderabad 500033</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 11:00 AM - 9:00 PM</span>
              <a href="tel:+914023558800" class="hover:text-[#7A152E] font-medium">+91 40 2355 8800</a>
            </div>
          </div>

          <!-- Jaipur MI Road -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">Jaipur</span>
              <a href="https://maps.google.com/?q=MI+Road+Jaipur" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">Heritage Gem Vault</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">Mirza Ismail Road, Near Raj Mandir, Jaipur 302001</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 10:30 AM - 8:00 PM</span>
              <a href="tel:+911412376610" class="hover:text-[#7A152E] font-medium">+91 141 237 6610</a>
            </div>
          </div>

          <!-- Kolkata Park Street -->
          <div class="p-4 rounded-2xl bg-[#FAF8F5] border border-[#EAE4DC] hover:border-[#7A152E]/40 transition-all space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold uppercase tracking-wider text-[#7A152E] bg-[#FAF0F2] px-2 py-0.5 rounded-full border border-[#EAD5DA]">Kolkata</span>
              <a href="https://maps.google.com/?q=Park+Street+Kolkata" target="_blank" rel="noopener" class="text-[11px] text-[#7A152E] font-semibold hover:underline flex items-center gap-0.5">Directions <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="m7 7 10 10"/><path d="M17 7v10H7"/></svg></a>
            </div>
            <h4 class="font-serif text-base text-stone-900 font-semibold">Park Street Salon</h4>
            <p class="text-stone-600 text-[11.5px] leading-relaxed">77 Park Street, Camac Street Intersection, Kolkata 700016</p>
            <div class="text-[11px] text-stone-500 pt-1 border-t border-stone-200/60 flex items-center justify-between">
              <span>Mon-Sun: 11:00 AM - 8:30 PM</span>
              <a href="tel:+913322295540" class="hover:text-[#7A152E] font-medium">+91 33 2229 5540</a>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-2xl bg-[#FAF0F2] border border-[#EAD5DA] flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
          <div class="text-stone-800">
            <strong class="text-[#7A152E] block">Complimentary Concierge Appointment:</strong>
            Reserve private atelier viewing with dedicated senior gemologist.
          </div>
          <button onclick="window.showToast('Appointment Reserved', 'Atelier concierge will contact you within 2 hours to confirm your private suite.'); window.closeBoutiqueModal();" class="px-5 py-2.5 bg-[#7A152E] hover:bg-[#590D1E] text-white text-xs font-bold uppercase tracking-wider rounded-xl transition-all cursor-pointer whitespace-nowrap active:scale-95 shadow-md">
            Request VIP Appointment
          </button>
        </div>
      </div>
    `;
    modal.classList.remove('hidden');
  };

  window.closeBoutiqueModal = function () {
    const modal = document.getElementById('boutique-modal-root');
    if (modal) modal.classList.add('hidden');
  };

  // 10. Global Newsletter Form Handler
  document.addEventListener('submit', function (e) {
    const form = e.target;
    const isNewsletter = form.classList.contains('newsletter-form') || form.querySelector('input[type="email"][placeholder*="Privé"], input[type="email"][placeholder*="email"], input[type="email"][placeholder*="newsletter"]');
    if (isNewsletter) {
      e.preventDefault();
      const emailInput = form.querySelector('input[type="email"]');
      const email = emailInput ? emailInput.value.trim() : '';
      if (!email || !email.includes('@')) {
        window.showToast('Invalid Email', 'Please enter a valid email address.', 'info');
        return;
      }
      try {
        navigator.clipboard.writeText('SOULY10');
      } catch (err) {}
      window.showToast('Welcome to Solystra Privé!', 'Code SOULY10 (10% OFF) copied to clipboard!');
      if (emailInput) emailInput.value = '';
    }
  });

  // 11. Initial Mobile Accordion Toggle for PDP Details
  function initPdpMobileAccordions() {
    const accordions = document.querySelectorAll('.md\\:hidden.divide-y.divide-stone-200 > div');
    accordions.forEach(acc => {
      const header = acc.querySelector('button, .cursor-pointer');
      const panel = acc.querySelector('.overflow-hidden, .transition-all.duration-300');
      const arrow = acc.querySelector('svg.lucide-chevron-down');
      if (header && panel) {
        header.onclick = function (e) {
          e.preventDefault();
          const isClosed = panel.classList.contains('max-h-0') || panel.style.maxHeight === '0px' || panel.style.display === 'none';
          if (isClosed) {
            panel.classList.remove('max-h-0');
            panel.style.display = 'block';
            panel.style.maxHeight = panel.scrollHeight + 'px';
            if (arrow) arrow.style.transform = 'rotate(180deg)';
          } else {
            panel.style.maxHeight = '0px';
            if (arrow) arrow.style.transform = 'rotate(0deg)';
          }
        };
      }
    });
  }

  // Auto-init PDP enhancements on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      if (window.location.pathname.includes('product.html')) {
        setTimeout(initPdpMobileAccordions, 150);
        setTimeout(() => window.switchPdpTab(0), 100);
      }
    });
  } else {
    if (window.location.pathname.includes('product.html')) {
      setTimeout(initPdpMobileAccordions, 150);
      setTimeout(() => window.switchPdpTab(0), 100);
    }
  }


})();
