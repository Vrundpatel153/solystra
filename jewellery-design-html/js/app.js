// ============================================================
// SOLYSTRA JEWELS - Master Client-side Application Logic
// Pure Vanilla JavaScript (Cart, Wishlist, Drawers, Search, Modals)
// ============================================================

(function () {
  'use strict';

  // ------------------------------------------------------------
  // 1. STATE MANAGEMENT (LocalStorage)
  // ------------------------------------------------------------
  const CART_KEY = 'solystra_cart_items_v2';
  const WISHLIST_KEY = 'solystra_wishlist_items_v2';

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
    } catch (e) {}
    updateBadgeCounts();
    renderCartDrawer();
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
    } catch (e) {}
    updateBadgeCounts();
    renderWishlistDrawer();
    updateWishlistIcons();
  }

  // ------------------------------------------------------------
  // 2. CART ACTIONS
  // ------------------------------------------------------------
  window.addToCart = function (productId, selectedMetal, size, customNote, quantity) {
    const qty = quantity || 1;
    const products = window.PRODUCTS || [];
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const metal = selectedMetal || (product.metals && product.metals[0]) || 'Pure 925 Silver';
    const ringSize = size || (product.category === 'rings' ? '12' : null);
    const cart = getCart();

    const existingIndex = cart.findIndex(item =>
      item.id === productId &&
      item.selectedMetal === metal &&
      item.size === ringSize
    );

    if (existingIndex > -1) {
      cart[existingIndex].quantity += qty;
    } else {
      cart.push({
        id: product.id,
        name: product.name,
        price: product.price,
        mrp: product.mrp,
        image: product.images && product.images[0] ? product.images[0] : '',
        selectedMetal: metal,
        size: ringSize,
        customNote: customNote || '',
        quantity: qty
      });
    }

    saveCart(cart);
    showToast(`Added "${product.shortName || product.name}" to your Bag`);
    openCartDrawer();
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

  window.removeFromCart = function (index) {
    const cart = getCart();
    if (!cart[index]) return;
    const removedName = cart[index].name;
    cart.splice(index, 1);
    saveCart(cart);
    showToast(`Removed "${removedName}" from Bag`);
  };

  // ------------------------------------------------------------
  // 3. WISHLIST ACTIONS
  // ------------------------------------------------------------
  window.toggleWishlist = function (productId) {
    const products = window.PRODUCTS || [];
    const product = products.find(p => p.id === productId);
    if (!product) return;

    let wishlist = getWishlist();
    const index = wishlist.indexOf(productId);

    if (index > -1) {
      wishlist.splice(index, 1);
      saveWishlist(wishlist);
      showToast(`Removed from Wishlist`);
    } else {
      wishlist.push(productId);
      saveWishlist(wishlist);
      showToast(`Saved to Wishlist`);
    }
  };

  window.isInWishlist = function (productId) {
    return getWishlist().includes(productId);
  };

  function updateWishlistIcons() {
    const wishlist = getWishlist();
    document.querySelectorAll('[data-wishlist-btn]').forEach(btn => {
      const pid = btn.getAttribute('data-wishlist-btn');
      const heartIcon = btn.querySelector('svg');
      if (wishlist.includes(pid)) {
        btn.classList.add('text-[#7A152E]');
        btn.classList.remove('text-stone-400', 'text-stone-600');
        if (heartIcon) heartIcon.setAttribute('fill', '#7A152E');
      } else {
        btn.classList.remove('text-[#7A152E]');
        btn.classList.add('text-stone-400');
        if (heartIcon) heartIcon.setAttribute('fill', 'none');
      }
    });
  }

  // ------------------------------------------------------------
  // 4. HEADER BADGE COUNTS
  // ------------------------------------------------------------
  function updateBadgeCounts() {
    const cart = getCart();
    const wishlist = getWishlist();

    const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    const totalWishlistCount = wishlist.length;

    // Cart counts
    document.querySelectorAll('.cart-count-badge').forEach(el => {
      el.textContent = totalCartCount;
      if (totalCartCount > 0) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    });

    // Cart text counts e.g. "Bag (2)"
    document.querySelectorAll('.cart-count-text').forEach(el => {
      el.textContent = `Bag (${totalCartCount})`;
    });

    // Wishlist counts
    document.querySelectorAll('.wishlist-count-badge').forEach(el => {
      el.textContent = totalWishlistCount;
      if (totalWishlistCount > 0) {
        el.classList.remove('hidden');
      } else {
        el.classList.add('hidden');
      }
    });
  }

  // ------------------------------------------------------------
  // 5. TOAST SYSTEM
  // ------------------------------------------------------------
  window.showToast = function (message) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast-item';
    toast.innerHTML = `
      <svg class="w-4 h-4 text-[#C5A059] flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span>${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('toast-out');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 2800);
  };

  // ------------------------------------------------------------
  // 6. DRAWERS & MODALS (Cart, Wishlist, Search, QuickView, Menu)
  // ------------------------------------------------------------
  window.openCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer');
    const backdrop = document.getElementById('cart-drawer-backdrop');
    if (drawer && backdrop) {
      backdrop.classList.remove('hidden', 'opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100', 'pointer-events-auto');
      drawer.classList.remove('translate-x-full');
      document.body.style.overflow = 'hidden';
      renderCartDrawer();
    }
  };

  window.closeCartDrawer = function () {
    const drawer = document.getElementById('cart-drawer');
    const backdrop = document.getElementById('cart-drawer-backdrop');
    if (drawer && backdrop) {
      drawer.classList.add('translate-x-full');
      backdrop.classList.remove('opacity-100', 'pointer-events-auto');
      backdrop.classList.add('opacity-0', 'pointer-events-none');
      setTimeout(() => backdrop.classList.add('hidden'), 350);
      document.body.style.overflow = '';
    }
  };

  window.openWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer');
    const backdrop = document.getElementById('wishlist-drawer-backdrop');
    if (drawer && backdrop) {
      backdrop.classList.remove('hidden', 'opacity-0', 'pointer-events-none');
      backdrop.classList.add('opacity-100', 'pointer-events-auto');
      drawer.classList.remove('translate-x-full');
      document.body.style.overflow = 'hidden';
      renderWishlistDrawer();
    }
  };

  window.closeWishlistDrawer = function () {
    const drawer = document.getElementById('wishlist-drawer');
    const backdrop = document.getElementById('wishlist-drawer-backdrop');
    if (drawer && backdrop) {
      drawer.classList.add('translate-x-full');
      backdrop.classList.remove('opacity-100', 'pointer-events-auto');
      backdrop.classList.add('opacity-0', 'pointer-events-none');
      setTimeout(() => backdrop.classList.add('hidden'), 350);
      document.body.style.overflow = '';
    }
  };

  window.openSearchModal = function () {
    const modal = document.getElementById('search-modal');
    if (modal) {
      modal.classList.remove('hidden');
      setTimeout(() => {
        modal.classList.remove('opacity-0');
        const input = document.getElementById('search-input');
        if (input) input.focus();
      }, 10);
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeSearchModal = function () {
    const modal = document.getElementById('search-modal');
    if (modal) {
      modal.classList.add('opacity-0');
      setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }, 250);
    }
  };

  window.openBoutiqueModal = function () {
    const modal = document.getElementById('boutique-modal');
    if (modal) {
      modal.classList.remove('hidden');
      setTimeout(() => modal.classList.remove('opacity-0'), 10);
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeBoutiqueModal = function () {
    const modal = document.getElementById('boutique-modal');
    if (modal) {
      modal.classList.add('opacity-0');
      setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }, 250);
    }
  };

  window.closeQuickViewModal = function () {
    const modal = document.getElementById('quickview-modal');
    if (modal) {
      modal.classList.add('opacity-0');
      setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }, 250);
    }
  };

  // ------------------------------------------------------------
  // 7. RENDER CART DRAWER CONTENT
  // ------------------------------------------------------------
  function renderCartDrawer() {
    const container = document.getElementById('cart-items-container');
    const footer = document.getElementById('cart-drawer-footer');
    if (!container) return;

    const cart = getCart();

    if (cart.length === 0) {
      container.innerHTML = `
        <div class="h-full flex flex-col items-center justify-center p-8 text-center text-stone-500">
          <div class="w-16 h-16 rounded-full bg-stone-100 flex items-center justify-center mb-4 text-[#7A152E]">
            <svg class="w-8 h-8 stroke-[1.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
          </div>
          <h4 class="font-serif text-xl text-stone-900 mb-2">Your Shopping Bag is Empty</h4>
          <p class="text-xs text-stone-500 max-w-xs mb-6">Explore our curated collections of hallmarked 925 silver and 18K gold heirloom jewelry.</p>
          <a href="products.html" onclick="closeCartDrawer()" class="px-6 py-2.5 bg-[#7A152E] text-white text-xs font-semibold rounded-full hover:bg-[#590D1E] transition-all shadow-md">
            Discover Atelier Pieces
          </a>
        </div>
      `;
      if (footer) footer.classList.add('hidden');
      return;
    }

    if (footer) footer.classList.remove('hidden');

    let subtotal = 0;
    let html = '';

    cart.forEach((item, index) => {
      const itemTotal = item.price * item.quantity;
      subtotal += itemTotal;

      html += `
        <div class="flex gap-4 p-4 border-b border-[#EAE4DC] bg-white rounded-2xl mb-3 shadow-2xs">
          <img src="${item.image}" alt="${item.name}" class="w-20 h-20 rounded-xl object-cover border border-[#EAE4DC] bg-[#FAF8F5] flex-shrink-0" />
          <div class="flex-1 min-w-0 flex flex-col justify-between">
            <div class="flex items-start justify-between gap-2">
              <h5 class="font-serif text-sm font-semibold text-stone-900 truncate">${item.name}</h5>
              <button onclick="removeFromCart(${index})" class="text-stone-400 hover:text-[#7A152E] p-1 transition-colors" title="Remove">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div class="text-[11px] text-stone-500">
              <span>${item.selectedMetal}</span>
              ${item.size ? `<span class="mx-1">•</span><span>Size: ${item.size}</span>` : ''}
            </div>
            <div class="flex items-center justify-between mt-2">
              <div class="flex items-center border border-[#EAE4DC] rounded-lg overflow-hidden bg-stone-50">
                <button onclick="updateCartQuantity(${index}, -1)" class="w-7 h-7 flex items-center justify-center text-stone-600 hover:bg-stone-200 transition-colors">-</button>
                <span class="w-7 h-7 flex items-center justify-center text-xs font-semibold text-stone-900">${item.quantity}</span>
                <button onclick="updateCartQuantity(${index}, 1)" class="w-7 h-7 flex items-center justify-center text-stone-600 hover:bg-stone-200 transition-colors">+</button>
              </div>
              <div class="text-right">
                <span class="text-xs font-bold text-stone-900">₹${itemTotal.toLocaleString('en-IN')}</span>
              </div>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;

    // Update Subtotal in Drawer
    const subtotalEl = document.getElementById('cart-drawer-subtotal');
    if (subtotalEl) {
      subtotalEl.textContent = `₹${subtotal.toLocaleString('en-IN')}`;
    }

    // Free Shipping Progress
    const freeShipThreshold = 999;
    const progressEl = document.getElementById('cart-free-shipping-progress');
    const freeShipTextEl = document.getElementById('cart-free-shipping-text');
    if (progressEl && freeShipTextEl) {
      if (subtotal >= freeShipThreshold) {
        progressEl.style.width = '100%';
        freeShipTextEl.innerHTML = `<span class="text-emerald-700 font-semibold">🎉 You've unlocked Free Insured Express Delivery!</span>`;
      } else {
        const remaining = freeShipThreshold - subtotal;
        const pct = Math.min(100, Math.round((subtotal / freeShipThreshold) * 100));
        progressEl.style.width = `${pct}%`;
        freeShipTextEl.innerHTML = `Add <strong class="text-[#7A152E]">₹${remaining.toLocaleString('en-IN')}</strong> more for Free Insured Delivery`;
      }
    }
  }

  // ------------------------------------------------------------
  // 8. RENDER WISHLIST DRAWER CONTENT
  // ------------------------------------------------------------
  function renderWishlistDrawer() {
    const container = document.getElementById('wishlist-items-container');
    if (!container) return;

    const wishlist = getWishlist();
    const products = window.PRODUCTS || [];
    const wishlistProducts = products.filter(p => wishlist.includes(p.id));

    if (wishlistProducts.length === 0) {
      container.innerHTML = `
        <div class="h-full flex flex-col items-center justify-center p-8 text-center text-stone-500">
          <div class="w-16 h-16 rounded-full bg-stone-100 flex items-center justify-center mb-4 text-[#7A152E]">
            <svg class="w-8 h-8 stroke-[1.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
          <h4 class="font-serif text-xl text-stone-900 mb-2">Your Wishlist is Empty</h4>
          <p class="text-xs text-stone-500 max-w-xs mb-6">Save your favorite handcrafted rings, solitaire pendants, and bracelets to revisit later.</p>
          <a href="products.html" onclick="closeWishlistDrawer()" class="px-6 py-2.5 bg-[#7A152E] text-white text-xs font-semibold rounded-full hover:bg-[#590D1E] transition-all shadow-md">
            Explore Collection
          </a>
        </div>
      `;
      return;
    }

    let html = '';
    wishlistProducts.forEach(product => {
      html += `
        <div class="flex gap-4 p-4 border-b border-[#EAE4DC] bg-white rounded-2xl mb-3 shadow-2xs">
          <img src="${product.images[0]}" alt="${product.name}" class="w-20 h-20 rounded-xl object-cover border border-[#EAE4DC] bg-[#FAF8F5] flex-shrink-0" />
          <div class="flex-1 min-w-0 flex flex-col justify-between">
            <div class="flex items-start justify-between gap-2">
              <h5 class="font-serif text-sm font-semibold text-stone-900 truncate">${product.name}</h5>
              <button onclick="toggleWishlist('${product.id}')" class="text-stone-400 hover:text-[#7A152E] p-1 transition-colors" title="Remove">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            <div class="flex items-center gap-2 mt-1">
              <span class="text-xs font-bold text-stone-900">₹${product.price.toLocaleString('en-IN')}</span>
              ${product.mrp ? `<span class="text-[11px] text-stone-400 line-through">₹${product.mrp.toLocaleString('en-IN')}</span>` : ''}
            </div>
            <div class="flex items-center gap-2 mt-2">
              <button onclick="addToCart('${product.id}'); toggleWishlist('${product.id}')" class="flex-1 py-1.5 px-3 bg-[#7A152E] text-white text-[11px] font-semibold rounded-lg hover:bg-[#590D1E] transition-colors text-center">
                Move to Bag
              </button>
              <a href="product.html?id=${product.id}" class="py-1.5 px-3 border border-stone-200 text-stone-700 text-[11px] font-medium rounded-lg hover:border-[#7A152E] hover:text-[#7A152E] transition-colors">
                View
              </a>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  // ------------------------------------------------------------
  // 9. QUICK VIEW MODAL
  // ------------------------------------------------------------
  window.openQuickView = function (productId) {
    const products = window.PRODUCTS || [];
    const product = products.find(p => p.id === productId);
    if (!product) return;

    const modal = document.getElementById('quickview-modal');
    const container = document.getElementById('quickview-modal-content');
    if (!modal || !container) return;

    const discountText = product.discount || (product.mrp ? `${Math.round(((product.mrp - product.price) / product.mrp) * 100)}% OFF` : '');

    const metals = product.metals || ['Pure 925 Silver', '18K Yellow Gold', 'Rose Gold Plated'];
    const metalOptions = metals.map((m, idx) => `
      <label class="flex items-center gap-2 text-xs text-stone-700 cursor-pointer">
        <input type="radio" name="qv-metal" value="${m}" ${idx === 0 ? 'checked' : ''} class="accent-[#7A152E]">
        <span>${m}</span>
      </label>
    `).join('');

    container.innerHTML = `
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
        <!-- Gallery -->
        <div class="space-y-3">
          <div class="aspect-[4/5] rounded-2xl overflow-hidden bg-[#FAF8F5] border border-[#EAE4DC] relative">
            <img id="qv-main-img" src="${product.images[0]}" alt="${product.name}" class="w-full h-full object-cover">
            ${discountText ? `<span class="absolute top-3 left-3 bg-[#7A152E] text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">${discountText}</span>` : ''}
          </div>
          <div class="flex gap-2 overflow-x-auto pb-1">
            ${product.images.map((img, i) => `
              <img src="${img}" onclick="document.getElementById('qv-main-img').src='${img}'" class="w-14 h-14 rounded-lg object-cover border border-[#EAE4DC] cursor-pointer hover:border-[#7A152E] transition-all bg-[#FAF8F5]" />
            `).join('')}
          </div>
        </div>

        <!-- Info -->
        <div class="flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-[10px] uppercase tracking-widest text-[#7A152E] font-bold">${product.categoryName || product.category}</span>
              <div class="flex items-center gap-1 text-xs text-amber-500">
                <span>★</span>
                <span class="font-semibold text-stone-800">${product.rating || '4.8'}</span>
                <span class="text-stone-400">(${product.reviewsCount || '24'})</span>
              </div>
            </div>

            <h3 class="font-serif text-2xl font-semibold text-stone-900 mb-2">${product.name}</h3>
            
            <div class="flex items-baseline gap-3 mb-4">
              <span class="text-2xl font-bold text-stone-900">₹${product.price.toLocaleString('en-IN')}</span>
              ${product.mrp ? `<span class="text-sm text-stone-400 line-through">₹${product.mrp.toLocaleString('en-IN')}</span>` : ''}
              <span class="text-xs text-emerald-700 font-semibold">Taxes Included</span>
            </div>

            <!-- Metal Purity Badge -->
            <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-200/80 mb-4">
              <span class="text-xs">🛡️</span>
              <span class="text-[11px] font-semibold text-amber-900">${product.specs ? product.specs['Metal Purity'] : 'BIS Certified 925 Sterling Silver'}</span>
            </div>

            <!-- Metal Choice -->
            <div class="mb-4">
              <span class="block text-xs font-semibold text-stone-800 mb-2">Select Metal / Tone:</span>
              <div class="flex flex-wrap gap-4">
                ${metalOptions}
              </div>
            </div>

            <p class="text-xs text-stone-600 line-clamp-3 leading-relaxed mb-6">
              ${product.desc || 'Meticulously handcrafted in pure 925 silver with dual-micron protective anti-tarnish rhodium barrier.'}
            </p>
          </div>

          <div class="space-y-3">
            <button onclick="
              const sel = document.querySelector('input[name=qv-metal]:checked');
              addToCart('${product.id}', sel ? sel.value : null);
              closeQuickViewModal();
            " class="w-full py-3.5 bg-[#7A152E] text-white text-xs font-bold uppercase tracking-wider rounded-xl hover:bg-[#590D1E] transition-all shadow-md cursor-pointer">
              Add to Shopping Bag
            </button>
            <a href="product.html?id=${product.id}" class="block text-center text-xs font-semibold text-stone-700 hover:text-[#7A152E] transition-colors py-1">
              View Full Product Specifications & Details →
            </a>
          </div>
        </div>
      </div>
    `;

    modal.classList.remove('hidden');
    setTimeout(() => modal.classList.remove('opacity-0'), 10);
    document.body.style.overflow = 'hidden';
  };

  // ------------------------------------------------------------
  // 10. SEARCH AUTOCOMPLETE / FILTER
  // ------------------------------------------------------------
  function initSearch() {
    const input = document.getElementById('search-input');
    const resultsContainer = document.getElementById('search-results');
    if (!input || !resultsContainer) return;

    input.addEventListener('input', function (e) {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        resultsContainer.innerHTML = '<p class="text-center text-xs text-stone-400 py-8">Search over 60+ handcrafted jewelry pieces by name, metal, or category</p>';
        return;
      }

      const products = window.PRODUCTS || [];
      const matches = products.filter(p =>
        (p.name && p.name.toLowerCase().includes(q)) ||
        (p.category && p.category.toLowerCase().includes(q)) ||
        (p.metalType && p.metalType.toLowerCase().includes(q)) ||
        (p.desc && p.desc.toLowerCase().includes(q))
      ).slice(0, 10);

      if (matches.length === 0) {
        resultsContainer.innerHTML = `<p class="text-center text-xs text-stone-400 py-8">No pieces found matching "${q}". Try searching for 'ring', 'silver', or 'gold'.</p>`;
        return;
      }

      let html = '<div class="divide-y divide-[#EAE4DC]">';
      matches.forEach(product => {
        html += `
          <a href="product.html?id=${product.id}" onclick="closeSearchModal()" class="flex items-center gap-3 p-3 hover:bg-[#FAF8F5] transition-colors rounded-xl">
            <img src="${product.images[0]}" alt="${product.name}" class="w-12 h-12 rounded-lg object-cover border border-[#EAE4DC]" />
            <div class="flex-1 min-w-0">
              <h6 class="font-serif text-sm font-semibold text-stone-900 truncate">${product.name}</h6>
              <div class="flex items-center gap-2 text-xs">
                <span class="text-[#7A152E] font-bold">₹${product.price.toLocaleString('en-IN')}</span>
                <span class="text-stone-400 uppercase tracking-widest text-[10px]">${product.category}</span>
              </div>
            </div>
          </a>
        `;
      });
      html += '</div>';

      resultsContainer.innerHTML = html;
    });
  }

  // ------------------------------------------------------------
  // 11. REUSABLE PRODUCT CARD GENERATOR (Exact visual match)
  // ------------------------------------------------------------
  window.renderProductCardHTML = function (product) {
    const isWish = isInWishlist(product.id);
    const primaryImg = product.images[0];
    const hoverImg = product.images.length > 1 ? product.images[1] : product.images[0];

    const discountText = product.discount || (product.mrp && product.mrp > product.price
      ? `${Math.round(((product.mrp - product.price) / product.mrp) * 100)}% OFF`
      : null);

    // Clean title
    const cleanTitle = (product.shortName || product.name || '')
      .replace(/\s*-\s*(925\s*)?(sterling\s*)?silver/gi, '')
      .replace(/\s*-\s*pure\s*silver/gi, '')
      .trim();

    const metalPurity = product.specs ? product.specs['Metal Purity'] : 'Pure 925 Silver';
    const isGold = (product.metalType === 'gold') || (product.name && product.name.toLowerCase().includes('gold'));

    return `
      <div class="group bg-white rounded-2xl border border-[#EAE4DC] overflow-hidden shadow-xs hover:shadow-xl hover:border-[#7A152E]/60 transition-all duration-300 flex flex-col relative w-full" data-product-id="${product.id}">
        <!-- Image Viewport (4:5 Aspect Ratio) -->
        <div class="relative w-full aspect-[4/5] bg-[#FAF8F5] overflow-hidden cursor-pointer product-card-img-wrap" onclick="window.location.href='product.html?id=${product.id}'">
          <img src="${primaryImg}" alt="${product.name}" loading="lazy" class="primary-img w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
          <img src="${hoverImg}" alt="${product.name}" loading="lazy" class="absolute inset-0 w-full h-full object-cover opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          <!-- Discount / Badge -->
          ${discountText ? `
            <div class="absolute top-2.5 left-2.5 z-10">
              <span class="bg-[#7A152E] text-white text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider shadow-xs">
                ${discountText}
              </span>
            </div>
          ` : ''}

          <!-- Quick Actions on Image (Quick View) -->
          <div class="absolute bottom-2.5 left-2.5 right-2.5 flex items-center justify-between opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10">
            <button onclick="event.stopPropagation(); openQuickView('${product.id}')" class="flex-1 py-1.5 bg-white/95 backdrop-blur-sm text-stone-900 text-[11px] font-semibold rounded-lg shadow-md hover:bg-[#7A152E] hover:text-white transition-all text-center">
              Quick View
            </button>
          </div>
        </div>

        <!-- Details -->
        <div class="p-3.5 flex flex-col flex-1 justify-between gap-2">
          <div>
            <!-- Hallmark Purity Pill -->
            <div class="flex items-center gap-1 text-[10px] font-medium text-stone-500 mb-1">
              <span class="w-1.5 h-1.5 rounded-full ${isGold ? 'bg-amber-400' : 'bg-slate-400'}"></span>
              <span class="truncate">${metalPurity}</span>
            </div>

            <!-- Title -->
            <a href="product.html?id=${product.id}" class="block">
              <h4 class="font-serif text-[14px] sm:text-[15px] font-semibold text-stone-900 group-hover:text-[#7A152E] transition-colors line-clamp-1 leading-snug">
                ${cleanTitle}
              </h4>
            </a>
          </div>

          <!-- Price & Wishlist Row -->
          <div class="flex items-center justify-between pt-1 border-t border-stone-100 mt-auto">
            <div>
              <span class="text-sm sm:text-[15px] font-bold text-stone-900">₹${product.price.toLocaleString('en-IN')}</span>
              ${product.mrp ? `<span class="text-[11px] text-stone-400 line-through ml-1.5">₹${product.mrp.toLocaleString('en-IN')}</span>` : ''}
            </div>

            <div class="flex items-center gap-1">
              <!-- Wishlist Button -->
              <button onclick="event.stopPropagation(); toggleWishlist('${product.id}')" data-wishlist-btn="${product.id}" class="p-1.5 text-stone-400 hover:text-[#7A152E] transition-colors rounded-full hover:bg-stone-50" title="Wishlist">
                <svg class="w-4 h-4" fill="${isWish ? '#7A152E' : 'none'}" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                </svg>
              </button>

              <!-- Add to Bag Button -->
              <button onclick="event.stopPropagation(); addToCart('${product.id}')" class="p-1.5 text-stone-700 hover:text-[#7A152E] transition-colors rounded-full hover:bg-stone-50" title="Add to Bag">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  };

  // ------------------------------------------------------------
  // 12. INITIALIZATION ON DOM READY
  // ------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    updateBadgeCounts();
    initSearch();

    // Mobile menu toggle
    const menuBtn = document.getElementById('mobile-menu-toggle');
    const menuDrawer = document.getElementById('mobile-menu-drawer');
    const menuBackdrop = document.getElementById('mobile-menu-backdrop');

    if (menuBtn && menuDrawer && menuBackdrop) {
      menuBtn.addEventListener('click', function () {
        menuDrawer.classList.toggle('translate-x-full');
        menuBackdrop.classList.toggle('hidden');
      });
      menuBackdrop.addEventListener('click', function () {
        menuDrawer.classList.add('translate-x-full');
        menuBackdrop.classList.add('hidden');
      });
    }

    // Escape key closes open modals/drawers
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeCartDrawer();
        closeWishlistDrawer();
        closeSearchModal();
        closeBoutiqueModal();
        closeQuickViewModal();
      }
    });
  });

})();
