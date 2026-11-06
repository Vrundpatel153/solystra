# -*- coding: utf-8 -*-

new_init_code = '''window.initProductsPage = initProductsPage;
  function initProductsPage() {
    const grid = document.getElementById('products-catalog-grid') ||
                 document.querySelector('main .grid.grid-cols-2') ||
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

    // Pagination constants and state
    const ITEMS_PER_PAGE = 20; // Exactly 4 rows on 5-col desktop grid (or 10 rows on 2-col mobile)
    let currentPage = 1;

    // Filter states (supports single or multi-select array)
    const params = new URLSearchParams(window.location.search);
    const rawCat = (params.get('category') || 'all').toLowerCase();
    let activeCategories = rawCat.split(',').map(s => s.trim()).filter(Boolean);
    if (activeCategories.length === 0) activeCategories = ['all'];
    let activeCategory = activeCategories[0] || 'all';

    const rawMetal = (params.get('metal') || 'all').toLowerCase();
    let activeMetals = rawMetal.split(',').map(s => s.trim()).filter(Boolean);
    if (activeMetals.length === 0) activeMetals = ['all'];
    let activeMetal = activeMetals[0] || 'all';

    const rawCurated = (params.get('curated') || '').toLowerCase();
    let activeCurated = rawCurated.split(',').map(s => s.trim()).filter(Boolean);

    let activeFilter = (params.get('filter') || 'all').toLowerCase();
    let maxPrice = parseInt(params.get('maxPrice') || '80000', 10);
    let activePriceRange = params.get('priceRange') || 'all';
    let searchQuery = (params.get('search') || '').trim().toLowerCase();
    let currentSort = params.get('sort') || 'featured';

    const initPageParam = parseInt(params.get('page') || '1', 10);
    if (!isNaN(initPageParam) && initPageParam >= 1) {
      currentPage = initPageParam;
    }

    const searchInput = document.getElementById('catalog-search-input');
    if (searchInput && searchQuery) {
      searchInput.value = searchQuery;
    }

    // Function to apply filters and paginate
    function applyFilters() {
      const matchingCards = [];

      cards.forEach(card => {
        const cat = card.getAttribute('data-category') || '';
        const metal = card.getAttribute('data-metal') || '';
        const price = parseInt(card.getAttribute('data-price') || '0', 10);
        const name = card.getAttribute('data-name') || '';
        const isBestseller = card.getAttribute('data-bestseller') === 'true';
        const isNew = card.getAttribute('data-new') === 'true';

        // Helper for category matching
        function testSingleCat(cTarget) {
          if (cTarget === 'all') return true;
          if (cTarget === 'bestseller' || cTarget === 'bestsellers') return isBestseller;
          if (cTarget === 'new') return isNew;
          if (cTarget === 'complete_sets' || cTarget === 'gift sets & suites' || cTarget === 'sets') {
            return cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite');
          }
          if (cTarget === 'layering chains' || cTarget === 'chains') {
            return cat === 'necklaces' && (name.includes('chain') || name.includes('lariat'));
          }
          if (cTarget === 'silver anklets' || cTarget === 'anklets') {
            return cat === 'anklets' || name.includes('anklet');
          }
          if (cTarget === 'bracelets & kadas' || cTarget === 'bracelets') {
            return cat === 'bracelets' || name.includes('bracelet') || name.includes('bangle') || name.includes('cuff') || name.includes('kada');
          }
          if (cTarget === 'necklaces & pendants' || cTarget === 'necklaces') {
            return cat === 'necklaces' || name.includes('necklace') || name.includes('pendant');
          }
          if (cTarget === 'rings & bands' || cTarget === 'rings') {
            return cat === 'rings' || name.includes('ring') || name.includes('band') || name.includes('solitaire');
          }
          if (cTarget === 'earrings & studs' || cTarget === 'earrings') {
            return cat === 'earrings' || name.includes('earring') || name.includes('stud') || name.includes('hoop') || name.includes('drop');
          }
          return cat.includes(cTarget) || cTarget.includes(cat);
        }

        // Helper for metal matching
        function testSingleMetal(mTarget) {
          if (mTarget === 'all') return true;
          if (mTarget === 'silver' || mTarget === '925 silver') return metal === 'silver';
          if (mTarget === 'gold' || mTarget === '18k gold') return metal === 'gold';
          if (mTarget === 'rose' || mTarget === 'rose gold') return metal === 'rose';
          return metal.includes(mTarget) || mTarget.includes(metal);
        }

        // Helper for curated collection matching
        function testSingleCurated(curTarget) {
          if (curTarget === 'links_layers' || curTarget === 'links') {
            return cat === 'necklaces' || name.includes('chain') || name.includes('link') || name.includes('layer') || name.includes('choker') || name.includes('lariat');
          }
          if (curTarget === 'drops_halo' || curTarget === 'halo') {
            return name.includes('halo') || name.includes('drop') || name.includes('cocktail') || name.includes('stud') || cat === 'earrings';
          }
          if (curTarget === 'dainty_steps' || curTarget === 'anklets') {
            return cat === 'anklets' || name.includes('anklet') || name.includes('charm') || name.includes('payal');
          }
          if (curTarget === 'daily_luxe' || curTarget === 'gold') {
            return metal === 'gold' || name.includes('gold') || name.includes('vermeil');
          }
          if (curTarget === 'tennis_fever' || curTarget === 'tennis') {
            return name.includes('tennis') || (cat === 'bracelets' && (name.includes('bracelet') || name.includes('cuff')));
          }
          if (curTarget === 'heirloom_suites' || curTarget === 'suites' || curTarget === 'sets') {
            return cat === 'complete_sets' || cat === 'sets' || name.includes('set') || name.includes('suite') || name.includes('gift');
          }
          return true;
        }

        // Multi-select Category match
        let catMatch = false;
        if (activeCategories.includes('all') || activeCategories.length === 0) {
          catMatch = true;
        } else {
          catMatch = activeCategories.some(c => testSingleCat(c));
        }

        // Multi-select Metal match
        let metalMatch = false;
        if (activeMetals.includes('all') || activeMetals.length === 0) {
          metalMatch = true;
        } else {
          metalMatch = activeMetals.some(m => testSingleMetal(m));
        }

        // Multi-select Curated match
        let curatedMatch = false;
        if (activeCurated.length === 0 || activeCurated.includes('all')) {
          curatedMatch = true;
        } else {
          curatedMatch = activeCurated.some(cur => testSingleCurated(cur));
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

        if (catMatch && metalMatch && curatedMatch && filterMatch && priceMatch && searchMatch) {
          matchingCards.push(card);
        } else {
          card.style.display = 'none';
        }
      });

      const totalMatching = matchingCards.length;
      const totalPages = Math.ceil(totalMatching / ITEMS_PER_PAGE) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
      const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, totalMatching);

      // Show only cards for the active page
      matchingCards.forEach((card, idx) => {
        if (idx >= startIndex && idx < endIndex) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });

      // Update counters in desktop and mobile headers
      const desktopCountEl = document.getElementById('catalog-products-count');
      if (desktopCountEl) {
        desktopCountEl.textContent = `(${totalMatching} creations)`;
      }
      const mobileCountEl = document.getElementById('mobile-catalog-products-count');
      if (mobileCountEl) {
        mobileCountEl.textContent = `(${totalMatching} creations)`;
      }

      // Show/Hide Empty State
      let emptyState = document.getElementById('catalog-empty-state');
      if (totalMatching === 0) {
        if (!emptyState) {
          emptyState = document.createElement('div');
          emptyState.id = 'catalog-empty-state';
          emptyState.className = 'col-span-full py-16 text-center space-y-4 bg-white rounded-2xl border border-[#CEBDA7] p-8 shadow-xs';
          emptyState.innerHTML = `
            <div class="w-14 h-14 rounded-full bg-[#F6F3EE] text-[#61532E] flex items-center justify-center mx-auto border border-[#CEBDA7]">
              <svg class="w-6 h-6 stroke-[1.8]" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><circle cx="11" cy="11" r="8"></circle><path d="m21 21-4.3-4.3"></path></svg>
            </div>
            <h4 class="font-serif text-xl text-stone-900 font-normal">No creations match your filter criteria</h4>
            <p class="text-xs text-stone-500 max-w-md mx-auto leading-relaxed">Try adjusting your budget, selecting all precious finishes, or resetting your filter preferences to explore the complete Solystra atelier collection.</p>
            <button onclick="window.resetCatalogFilters()" class="px-5 py-2.5 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs font-semibold rounded-xl transition-all cursor-pointer shadow-xs">Reset All Filters</button>
          `;
          grid.appendChild(emptyState);
        }
        emptyState.style.display = '';
      } else if (emptyState) {
        emptyState.style.display = 'none';
      }

      // Render Pagination
      renderPagination(totalMatching, totalPages, startIndex, endIndex);

      // Update Filter Badges
      updateActiveFilterBadges();
    }

    // Render pagination controls
    function renderPagination(totalMatching, totalPages, startIndex, endIndex) {
      const container = document.getElementById('catalog-pagination-container');
      if (!container) return;

      if (totalMatching === 0) {
        container.style.display = 'none';
        return;
      }
      container.style.display = 'flex';

      const startEl = document.getElementById('pagination-start-range');
      const endEl = document.getElementById('pagination-end-range');
      const totalEl = document.getElementById('pagination-total-items');
      if (startEl) startEl.textContent = totalMatching === 0 ? 0 : startIndex + 1;
      if (endEl) endEl.textContent = endIndex;
      if (totalEl) totalEl.textContent = totalMatching;

      const prevBtn = document.getElementById('pagination-prev-btn');
      const nextBtn = document.getElementById('pagination-next-btn');
      if (prevBtn) prevBtn.disabled = (currentPage <= 1);
      if (nextBtn) nextBtn.disabled = (currentPage >= totalPages);

      const pagesList = document.getElementById('pagination-pages-list');
      if (!pagesList) return;
      pagesList.innerHTML = '';

      // Determine pages to show
      let pagesToShow = [];
      if (totalPages <= 7) {
        for (let i = 1; i <= totalPages; i++) pagesToShow.push(i);
      } else {
        pagesToShow.push(1);
        if (currentPage > 3) pagesToShow.push('...');
        const s = Math.max(2, currentPage - 1);
        const e = Math.min(totalPages - 1, currentPage + 1);
        for (let i = s; i <= e; i++) {
          if (!pagesToShow.includes(i)) pagesToShow.push(i);
        }
        if (currentPage < totalPages - 2) pagesToShow.push('...');
        if (!pagesToShow.includes(totalPages)) pagesToShow.push(totalPages);
      }

      pagesToShow.forEach(p => {
        if (p === '...') {
          const span = document.createElement('span');
          span.className = 'px-1.5 py-1 text-xs text-stone-400 font-medium select-none';
          span.textContent = '…';
          pagesList.appendChild(span);
        } else {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.textContent = p;
          const isActive = (p === currentPage);
          btn.className = isActive
            ? 'w-8 h-8 sm:w-9 sm:h-9 rounded-xl text-xs font-bold transition-all cursor-pointer bg-[#61532E] text-white border border-[#61532E] shadow-2xs flex items-center justify-center'
            : 'w-8 h-8 sm:w-9 sm:h-9 rounded-xl text-xs font-semibold transition-all cursor-pointer bg-white hover:bg-[#FAF8F5] text-stone-700 border border-[#CEBDA7] hover:border-[#61532E]/40 shadow-2xs flex items-center justify-center';
          btn.onclick = () => window.changeCatalogPage(p);
          pagesList.appendChild(btn);
        }
      });
    }

    // Global page switcher
    window.getCurrentCatalogPage = function () {
      return currentPage;
    };

    window.changeCatalogPage = function (targetPage) {
      if (targetPage < 1) return;
      currentPage = targetPage;
      applyFilters();

      // Smooth scroll back to top of catalog
      const anchor = document.getElementById('catalog-products-count') || document.getElementById('products-catalog-grid') || document.querySelector('main');
      if (anchor) {
        const topY = anchor.getBoundingClientRect().top + window.pageYOffset - 120;
        window.scrollTo({ top: Math.max(0, topY), behavior: 'smooth' });
      }

      // URL Sync without reload
      try {
        const url = new URL(window.location.href);
        if (currentPage > 1) {
          url.searchParams.set('page', currentPage);
        } else {
          url.searchParams.delete('page');
        }
        window.history.pushState({ page: currentPage }, '', url.toString());
      } catch (e) {}
    };

    // Active filter badge updater
    function updateActiveFilterBadges() {
      let activeCount = 0;
      if (!activeCategories.includes('all') && activeCategories.length > 0) activeCount += activeCategories.length;
      if (!activeMetals.includes('all') && activeMetals.length > 0) activeCount += activeMetals.length;
      if (activeCurated.length > 0) activeCount += activeCurated.length;
      if (maxPrice < 80000) activeCount += 1;

      const desktopBadge = document.getElementById('desktop-filter-count-badge');
      if (desktopBadge) {
        if (activeCount > 0) {
          desktopBadge.textContent = activeCount;
          desktopBadge.classList.remove('hidden');
        } else {
          desktopBadge.classList.add('hidden');
        }
      }
      const mobileBadge = document.getElementById('mobile-filter-count-badge');
      if (mobileBadge) {
        if (activeCount > 0) {
          mobileBadge.textContent = activeCount;
          mobileBadge.classList.remove('hidden');
        } else {
          mobileBadge.classList.add('hidden');
        }
      }
    }

    // Sorting Engine
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
      currentPage = 1;
      applyFilters();

      // Update sort button text & checkmarks
      const sortLabels = {
        'featured': 'Featured',
        'price-low': 'Price: Low to High',
        'price-high': 'Price: High to Low',
        'rating': 'Customer Rating',
        'newest': 'Newest First'
      };
      const labelText = sortLabels[sortKey] || 'Featured';

      const deskLabel = document.getElementById('desktop-sort-label');
      if (deskLabel) deskLabel.textContent = labelText;
      const mobLabel = document.getElementById('mobile-sort-label');
      if (mobLabel) mobLabel.textContent = labelText;

      document.querySelectorAll('.sort-check, .mobile-sort-check').forEach(chk => {
        const val = chk.getAttribute('data-sort-val');
        if (val === sortKey) {
          chk.classList.remove('hidden');
        } else {
          chk.classList.add('hidden');
        }
      });
    }

    // Attach global filterCatalog for oninput/onchange
    window.filterCatalog = function () {
      if (searchInput) searchQuery = searchInput.value.trim().toLowerCase();
      currentPage = 1;
      applyFilters();
    };

    window.setCatalogMaxPrice = function (val) {
      maxPrice = parseInt(val, 10);
      currentPage = 1;
      applyFilters();
    };

    window.setCatalogFilterState = function (newCats, newMetals, newCurated) {
      if (Array.isArray(newCats) && newCats.length > 0) activeCategories = newCats;
      else if (newCats && typeof newCats === 'string') activeCategories = [newCats];
      else activeCategories = ['all'];
      activeCategory = activeCategories[0] || 'all';

      if (Array.isArray(newMetals) && newMetals.length > 0) activeMetals = newMetals;
      else if (newMetals && typeof newMetals === 'string') activeMetals = [newMetals];
      else activeMetals = ['all'];
      activeMetal = activeMetals[0] || 'all';

      if (Array.isArray(newCurated)) activeCurated = newCurated;
      else if (newCurated && typeof newCurated === 'string') activeCurated = [newCurated];
      else activeCurated = [];

      currentPage = 1;
      highlightCategoryPills();
      highlightPricePills();
      applyFilters();

      try {
        const url = new URL(window.location.href);
        if (activeCategories.includes('all') || activeCategories.length === 0) url.searchParams.delete('category');
        else url.searchParams.set('category', activeCategories.join(','));
        if (activeMetals.includes('all') || activeMetals.length === 0) url.searchParams.delete('metal');
        else url.searchParams.set('metal', activeMetals.join(','));
        if (activeCurated.length === 0) url.searchParams.delete('curated');
        else url.searchParams.set('curated', activeCurated.join(','));
        url.searchParams.delete('page');
        window.history.replaceState({}, '', url.toString());
      } catch (e) {}
    };

    window.getCatalogFilterState = function () {
      return {
        categories: [...activeCategories],
        metals: [...activeMetals],
        curated: [...activeCurated]
      };
    };

    window.resetCatalogFilters = function () {
      activeCategories = ['all'];
      activeCategory = 'all';
      activeMetals = ['all'];
      activeMetal = 'all';
      activeCurated = [];
      activeFilter = 'all';
      maxPrice = 80000;
      activePriceRange = 'all';
      searchQuery = '';
      currentPage = 1;
      if (searchInput) searchInput.value = '';
      highlightCategoryPills();
      highlightPricePills();
      applyFilters();
      applySort('featured');

      try {
        const url = new URL(window.location.href);
        url.searchParams.delete('category');
        url.searchParams.delete('metal');
        url.searchParams.delete('curated');
        url.searchParams.delete('search');
        url.searchParams.delete('priceRange');
        url.searchParams.delete('maxPrice');
        url.searchParams.delete('page');
        window.history.replaceState({}, '', url.toString());
      } catch (e) {}
    };

    // Category button click handlers (Top category bar)
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
          btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all cursor-pointer active:scale-95 bg-[#61532E] text-white shadow-xs';
        } else {
          btn.className = 'px-3.5 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all cursor-pointer active:scale-95 bg-stone-100 hover:bg-stone-200/80 text-stone-700';
        }
      });
    }

    // Top Category Bar click binding
    const topCategoryPills = document.querySelectorAll('section.bg-white.border-b button');
    topCategoryPills.forEach(btn => {
      btn.onclick = function () {
        const text = btn.textContent.trim().toLowerCase();
        if (text.includes('all')) activeCategory = 'all';
        else if (text.includes('bracelet')) activeCategory = 'bracelets';
        else if (text.includes('necklace')) activeCategory = 'necklaces';
        else if (text.includes('ring')) activeCategory = 'rings';
        else if (text.includes('earring')) activeCategory = 'earrings';
        else if (text.includes('gift sets') || text.includes('suites') || text.includes('suite')) activeCategory = 'complete_sets';
        else if (text.includes('chain')) activeCategory = 'necklaces';
        else if (text.includes('anklet')) activeCategory = 'anklets';
        else if (text.includes('bestseller')) activeCategory = 'bestseller';
        else activeCategory = text;

        activeCategories = [activeCategory];
        currentPage = 1;
        highlightCategoryPills();
        applyFilters();

        try {
          const url = new URL(window.location.href);
          if (activeCategory === 'all') url.searchParams.delete('category');
          else url.searchParams.set('category', activeCategory);
          url.searchParams.delete('page');
          window.history.replaceState({}, '', url.toString());
        } catch (e) {}
      };
    });

    // Price Pills Highlighting & Click Handling (Desktop & Mobile)
    function highlightPricePills() {
      const priceButtons = document.querySelectorAll('#desktop-price-pills button, #mobile-price-pills button');
      priceButtons.forEach(btn => {
        const pr = btn.getAttribute('data-price-range') || '';
        const isMatch = (pr === activePriceRange);
        if (isMatch) {
          btn.className = 'px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-semibold whitespace-nowrap bg-[#61532E] text-white shadow-2xs shrink-0';
        } else {
          btn.className = 'px-3 py-1.5 rounded-xl text-xs transition-all cursor-pointer font-medium whitespace-nowrap bg-white hover:bg-[#FAF8F5] border border-[#CEBDA7] text-stone-700 hover:border-[#61532E]/30 shrink-0';
        }
      });
    }

    const priceButtons = document.querySelectorAll('#desktop-price-pills button, #mobile-price-pills button');
    priceButtons.forEach(btn => {
      btn.onclick = function () {
        const pr = btn.getAttribute('data-price-range') || 'all';
        activePriceRange = pr;
        currentPage = 1;
        highlightPricePills();
        applyFilters();
      };
    });

    // Sort Dropdown Controls
    window.toggleDesktopSortMenu = function (e) {
      if (e) e.stopPropagation();
      const menu = document.getElementById('desktop-sort-dropdown');
      const chev = document.getElementById('desktop-sort-chevron');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      // close mobile if open
      const mobMenu = document.getElementById('mobile-sort-dropdown');
      if (mobMenu) mobMenu.classList.add('hidden');

      if (isHidden) {
        menu.classList.remove('hidden');
        if (chev) chev.classList.add('rotate-180');
      } else {
        menu.classList.add('hidden');
        if (chev) chev.classList.remove('rotate-180');
      }
    };

    window.toggleMobileSortMenu = function (e) {
      if (e) e.stopPropagation();
      const menu = document.getElementById('mobile-sort-dropdown');
      const chev = document.getElementById('mobile-sort-chevron');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      const deskMenu = document.getElementById('desktop-sort-dropdown');
      if (deskMenu) deskMenu.classList.add('hidden');

      if (isHidden) {
        menu.classList.remove('hidden');
        if (chev) chev.classList.add('rotate-180');
      } else {
        menu.classList.add('hidden');
        if (chev) chev.classList.remove('rotate-180');
      }
    };

    window.setSortOption = function (sortKey) {
      applySort(sortKey);
      const deskMenu = document.getElementById('desktop-sort-dropdown');
      if (deskMenu) deskMenu.classList.add('hidden');
      const deskChev = document.getElementById('desktop-sort-chevron');
      if (deskChev) deskChev.classList.remove('rotate-180');

      const mobMenu = document.getElementById('mobile-sort-dropdown');
      if (mobMenu) mobMenu.classList.add('hidden');
      const mobChev = document.getElementById('mobile-sort-chevron');
      if (mobChev) mobChev.classList.remove('rotate-180');
    };

    document.addEventListener('click', function (e) {
      const deskWrap = document.getElementById('desktop-sort-wrapper');
      if (deskWrap && !deskWrap.contains(e.target)) {
        const menu = document.getElementById('desktop-sort-dropdown');
        if (menu) menu.classList.add('hidden');
        const chev = document.getElementById('desktop-sort-chevron');
        if (chev) chev.classList.remove('rotate-180');
      }
      const mobWrap = document.getElementById('mobile-sort-wrapper');
      if (mobWrap && !mobWrap.contains(e.target)) {
        const menu = document.getElementById('mobile-sort-dropdown');
        if (menu) menu.classList.add('hidden');
        const chev = document.getElementById('mobile-sort-chevron');
        if (chev) chev.classList.remove('rotate-180');
      }
    });

    // Initial setup
    highlightCategoryPills();
    highlightPricePills();
    applyFilters();
    if (currentSort !== 'featured') {
      applySort(currentSort);
    }
  }
'''

def write_update():
    js_path = 'jewellery-design-html/js/app.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    pos_start = js.find('window.initProductsPage = initProductsPage;')
    if pos_start == -1:
        pos_start = js.find('function initProductsPage()')
    pos_end = js.find('// Checkout Page initialization', pos_start)

    print("Replacing initProductsPage between", pos_start, "and", pos_end)
    js = js[:pos_start] + new_init_code + '\n\n  ' + js[pos_end:]

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Successfully replaced initProductsPage in app.js!")

if __name__ == '__main__':
    write_update()

