with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "const STYLING_COMBOS = ["
end_marker = "/* ==========================================================================\n     Newly Launched & Product Carousels Loop & Drag Engine"

idx_start = text.find(start_marker)
idx_end = text.find(end_marker)

print("idx_start:", idx_start, "idx_end:", idx_end)

new_curated_code = '''const STYLING_COMBOS = [
    {
      id: 'combo-1',
      name: 'Classic Solitaire Set',
      tag: 'PURE 925 STERLING SILVER',
      desc: 'Brilliant Austrian solitaire pendant paired with matching solitaire drop earrings.',
      editorialImg: 'solystra_assets/curated/curated_look_combo2.webp',
      imagePosition: 'object-[center_40%]',
      items: [
        {
          id: 'c1-item-1',
          productId: 'universal-embrace',
          type: 'NECKLACE',
          name: 'Universal Solitaire Drop Necklace',
          metal: 'Pure 925 Silver • Brilliant Cut Solitaire',
          price: 2799,
          mrp: 3999,
          image: 'solystra_assets/products/unity-circle/angle_1.webp',
          hotspot: { x: 43.4, y: 79.5, pcX: 43.4, pcY: 79.5, label: 'Solitaire Pendant Necklace' }
        },
        {
          id: 'c1-item-2',
          productId: 'classic-knot-earrings',
          type: 'EARRINGS',
          name: 'Solitaire Drop Earrings',
          metal: 'Pure 925 Silver • Cushion Cut Drop',
          price: 2299,
          mrp: 3299,
          image: 'solystra_assets/products/classic-knot-earrings/angle_1.webp',
          hotspot: { x: 65.4, y: 37.0, pcX: 65.4, pcY: 37.0, label: 'Solitaire Drop Earrings' }
        }
      ],
      bundlePrice: 5098,
      originalPrice: 7298,
      savings: 2200
    },
    {
      id: 'combo-2',
      name: 'Golden Meadow 18K Gold Set',
      tag: '18K GOLD VERMEIL',
      desc: 'Inspired by blooming wildflowers: a graduated tennis choker with matching delicate floral drop earrings in 18K gold vermeil.',
      editorialImg: 'solystra_assets/curated/curated_look_golden_meadow.webp',
      imagePosition: 'object-[center_40%]',
      items: [
        {
          id: 'c2-item-1',
          productId: 'golden-meadow-necklace-set-925-sterling-silver',
          type: 'JEWELRY SUITE',
          name: 'Golden Meadow Tennis Choker & Earrings Set in 18K Gold',
          metal: '18K Gold Vermeil • AAA+ Austrian Solitaires',
          price: 5499,
          mrp: 7999,
          image: 'solystra_assets/products/golden-meadow-necklace-set-925-sterling-silver/angle_1.webp',
          hotspot: { x: 43.0, y: 80.0, pcX: 43.0, pcY: 80.0, label: 'Golden Meadow Choker & Earrings Suite' }
        }
      ],
      bundlePrice: 5499,
      originalPrice: 7999,
      savings: 2500
    }
  ];

  let currentComboIdx = 0; // Default to Classic Solitaire Set
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
          btn.className = 'h-1.5 rounded-full transition-all duration-300 cursor-pointer w-5 bg-[#61532E]';
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
              <span class="absolute -inset-0.5 rounded-full bg-[#61532E]/35 animate-ping pointer-events-none"></span>

              <!-- Small Luxury Pinpoint Button -->
              <button type="button"
                      data-pin-btn="${item.id}"
                      class="w-3.5 h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer bg-[#61532E] hover:scale-125"
                      aria-label="View ${item.name}">
                <span class="w-1.5 h-1.5 rounded-full bg-white shadow-xs pointer-events-none"></span>
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
             class="flex items-center gap-3.5 p-3.5 rounded-xl transition-all cursor-pointer group border bg-[#FAF8F5]/80 border-[#CEBDA7] hover:border-[#61532E]/60 hover:bg-white hover:shadow-2xs"
             title="Click to view product details">
          <img src="${item.image}" alt="${item.name}" onerror="if(!this.dataset.err){this.dataset.err=1; this.src=this.src.endsWith('.webp')?this.src.replace('.webp','.png'):(this.src.endsWith('.png')?this.src.replace('.png','.jpg'):this.src.replace('.jpg','.webp'));}" class="w-16 h-16 rounded-xl object-cover border border-[#CEBDA7] bg-white shrink-0 group-hover:scale-105 transition-transform">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-[9.5px] text-[#61532E] uppercase font-bold tracking-wider block">${item.type}</span>
              <span class="text-[9px] text-[#C5A059] opacity-0 group-hover:opacity-100 transition-opacity font-semibold">View Piece ↗</span>
            </div>
            <h4 class="font-serif text-sm sm:text-base font-normal text-stone-900 truncate group-hover:text-[#61532E] transition-colors mt-0.5">${item.name}</h4>
            <div class="text-[11.5px] text-stone-500 truncate mt-0.5">${item.metal}</div>
          </div>
          <div class="text-right shrink-0">
            <div class="font-bold text-sm sm:text-base text-[#61532E]">₹${item.price.toLocaleString('en-IN')}</div>
            <div class="text-xs text-stone-400 line-through">₹${item.mrp.toLocaleString('en-IN')}</div>
          </div>
        </div>
      `).join('');

      // Complete 2-Column HTML with Proportional Portrait Framing (Full Model & Jewelry Visible)
      grid.innerHTML = `
        <!-- Left Column: Editorial Photo with Delicate Glowing Hotspots (Full Portrait View) -->
        <div id="combo-left-col" class="lg:col-span-5 h-[460px] sm:h-[520px] lg:h-[580px] relative rounded-2xl overflow-hidden shadow-xs border border-[#CEBDA7] group bg-stone-900 select-none">
          <img src="${combo.editorialImg}" alt="${combo.name}" draggable="false" class="w-full h-full object-cover ${combo.imagePosition} group-hover:scale-102 transition-transform duration-700 block pointer-events-none animate-fadeIn">
          
          <!-- Subtle ambient gradient in bottom 20% -->
          <div class="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/80 via-black/25 to-transparent pointer-events-none"></div>

          <!-- Glowing Hotspots -->
          ${hotspotsHtml}

          <!-- Bottom Editorial Tag & Name -->
          <div class="absolute bottom-3.5 left-3.5 sm:bottom-4 sm:left-4 z-10 pointer-events-none max-w-[85%] sm:max-w-md">
            <span class="text-[8.5px] xs:text-[9.5px] sm:text-[10px] uppercase tracking-widest text-[#E5C985] font-bold block mb-0.5 drop-shadow-xs">${combo.tag}</span>
            <h3 class="font-serif text-sm xs:text-base sm:text-lg text-white font-normal leading-snug drop-shadow-sm whitespace-nowrap">${combo.name}</h3>
          </div>
        </div>

        <!-- Right Column: Matched Pieces & Bundle Pricing -->
        <div id="combo-right-col" class="lg:col-span-7 h-[460px] sm:h-[520px] lg:h-[580px] flex flex-col justify-between bg-white rounded-2xl p-5 sm:p-7 border border-[#CEBDA7] shadow-xs animate-fadeIn">
          <div>
            <div class="flex items-start justify-between pb-3.5 border-b border-[#CEBDA7] gap-2">
              <div>
                <span class="text-[10px] text-[#61532E] uppercase tracking-widest font-bold block">${combo.tag}</span>
                <h3 class="text-base sm:text-lg font-serif font-normal text-stone-900 leading-tight mt-0.5">${combo.name}</h3>
                <p class="text-xs text-stone-500 mt-1 leading-relaxed hidden sm:block">${combo.desc}</p>
              </div>
              <span class="text-[11px] text-[#61532E] font-bold bg-[#61532E]/8 px-3 py-1 rounded-full border border-[#61532E]/20 uppercase tracking-wider shrink-0">
                Save ₹${combo.savings.toLocaleString('en-IN')}
              </span>
            </div>

            <!-- Matched Pieces Cards -->
            <div class="space-y-3 mt-4">
              ${itemsHtml}
              ${combo.items.length === 1 ? `
                <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#CEBDA7]/70 text-stone-600 text-xs space-y-2 mt-2">
                  <div class="flex items-center gap-1.5 text-[#61532E] font-bold text-[11px] uppercase tracking-wider">
                    <svg class="w-4 h-4 text-[#61532E]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    <span>Complete Atelier Gala Suite</span>
                  </div>
                  <p class="text-[11.5px] text-stone-500 leading-relaxed">Harmonized 18K gold vermeil graduated tennis choker and matching drop earrings suite, packaged in our signature velvet keepsake vault with certified hallmark card.</p>
                </div>
              ` : ''}
            </div>
          </div>

          <!-- Bundle Pricing & Action Bar -->
          <div class="pt-4 border-t border-[#CEBDA7] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="text-[10px] text-stone-500 uppercase tracking-wider font-semibold">Complete Set Price</div>
              <div class="flex items-baseline gap-2 mt-0.5">
                <span class="font-serif text-2xl sm:text-3xl font-bold text-[#61532E]">₹${combo.bundlePrice.toLocaleString('en-IN')}</span>
                <span class="text-xs text-stone-400 line-through font-sans">₹${combo.originalPrice.toLocaleString('en-IN')}</span>
                <span class="text-[10px] font-bold text-[#61532E] uppercase bg-[#61532E]/10 px-2 py-0.5 rounded-full border border-[#61532E]/20">Save ₹${combo.savings.toLocaleString('en-IN')}</span>
              </div>
            </div>

            <button type="button" id="btn-add-combo-to-bag" class="px-7 py-3 bg-[#61532E] hover:bg-[#3D341B] text-white text-xs font-bold uppercase tracking-wider rounded-xl shadow-md hover:shadow-lg transition-all cursor-pointer flex items-center justify-center gap-2 active:scale-98 shrink-0 group">
              <svg aria-hidden="true" class="w-4 h-4 shrink-0 -translate-y-px transition-transform group-hover:-translate-y-0.5" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <defs><linearGradient id="solystraChampagneGoldCombo" x1="0%" x2="100%" y1="0%" y2="100%"><stop offset="0%" stop-color="#FFF6D8"></stop><stop offset="35%" stop-color="#F9E2A8"></stop><stop offset="70%" stop-color="#E5BE64"></stop><stop offset="100%" stop-color="#D4AF37"></stop></linearGradient></defs>
                <path d="M6 2L3 6V20C3 21.1 3.9 22 5 22H19C20.1 22 21 21.1 21 20V6L18 2H6Z" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                <path d="M3 6H21" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                <path d="M16 10C16 12.21 14.21 14 12 14C9.79 14 8 12.21 8 10" stroke="url(#solystraChampagneGoldCombo)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
              <span class="leading-none">${combo.items.length === 1 ? 'Add Suite to Bag' : 'Add Look to Bag'}</span>
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
            if (btn) btn.className = 'w-3.5 h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer scale-125 bg-[#61532E] ring-2 ring-[#D4AF37]';
            if (popover) {
              popover.classList.remove('opacity-0', 'scale-95', 'invisible');
              popover.classList.add('opacity-100', 'scale-100', 'visible');
            }
          } else {
            if (btn) btn.className = 'w-3.5 h-3.5 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer bg-[#61532E] hover:scale-125';
            if (popover) {
              popover.classList.remove('opacity-100', 'scale-100', 'visible');
              popover.classList.add('opacity-0', 'scale-95', 'invisible');
            }
          }
        });

        allCards.forEach(card => {
          const cId = card.getAttribute('data-combo-item');
          if (cId === itemId) {
            card.className = 'flex items-center gap-3.5 p-3.5 rounded-xl transition-all cursor-pointer group border bg-[#61532E]/5 border-[#61532E] shadow-sm ring-1 ring-[#61532E]/20';
          } else {
            card.className = 'flex items-center gap-3.5 p-3.5 rounded-xl transition-all cursor-pointer group border bg-[#FAF8F5]/80 border-[#CEBDA7] hover:border-[#61532E]/60 hover:bg-white hover:shadow-2xs';
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
          const countDesc = combo.items.length === 1 ? 'Complete suite' : combo.items.length + ' pieces';
          window.showToast('Curated Look Added', combo.name + ' (' + countDesc + ') added to your private bag.');
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

    // Initial render: start at first Combo (Classic Solitaire Set)
    renderCombo(0);
    startComboTimer();
  }

  '''

if idx_start != -1 and idx_end != -1:
    new_text = text[:idx_start] + new_curated_code + text[idx_end:]
    with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully replaced curated section in app.js!")
else:
    print("Failed to find start or end marker!")

