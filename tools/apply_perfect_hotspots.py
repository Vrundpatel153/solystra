with open('jewellery-design-html/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate renderCombo definition
start_marker = "  function initStylingCombos() {"
end_marker = "    // Attach click handlers to top dot selectors\n    const dotButtons = document.querySelectorAll('#curated-combo-dots button');"

s_idx = content.find(start_marker)
e_idx = content.find(end_marker, s_idx)

if s_idx == -1 or e_idx == -1:
    print(f"Markers not found! s_idx={s_idx}, e_idx={e_idx}")
    exit(1)

new_init_styling_combos = """  function initStylingCombos() {
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

      // Build hotspot pins HTML (Pins positioned on jewelry)
      const pinsHtml = combo.items.map(item => {
        if (!item.hotspot) return '';
        const pcX = item.hotspot.pcX !== undefined ? item.hotspot.pcX : item.hotspot.x;
        const pcY = item.hotspot.pcY !== undefined ? item.hotspot.pcY : item.hotspot.y;

        return `
          <div class="combo-hotspot-pin absolute -translate-x-1/2 -translate-y-1/2 z-20 cursor-pointer"
               data-hotspot-id="${item.id}"
               style="--dot-x-mob: ${item.hotspot.x}%; --dot-y-mob: ${item.hotspot.y}%; --dot-x-pc: ${pcX}%; --dot-y-pc: ${pcY}%;">
            <div class="relative group/hotspot">
              <!-- Subtle micro pulse -->
              <span class="absolute -inset-1.5 rounded-full bg-[#D4AF37]/35 animate-ping pointer-events-none"></span>

              <!-- Luxury Pinpoint Button -->
              <button type="button"
                      data-pin-btn="${item.id}"
                      class="w-4 h-4 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-md cursor-pointer bg-[#61532E] hover:scale-125"
                      aria-label="View ${item.name}">
                <span class="w-1.5 h-1.5 rounded-full bg-white shadow-xs pointer-events-none"></span>
              </button>
            </div>
          </div>
        `;
      }).join('');

      // Build popovers HTML (Direct children of card container - strictly bounded, zero clipping)
      const popoversHtml = combo.items.map(item => {
        if (!item.hotspot) return '';
        return `
          <div data-popover="${item.id}"
               class="combo-popover absolute z-30 transition-all duration-300 pointer-events-auto opacity-0 scale-95 invisible
                      p-2.5 rounded-xl bg-[#1C1819]/95 backdrop-blur-md border border-[#C5A059]/60 shadow-[0_12px_32px_rgba(0,0,0,0.7)] text-white"
               style="display: block;"
               onclick="window.location.href='product.html?id=${item.productId}'">
            <div class="flex items-center gap-2.5">
              <img src="${item.image}" alt="${item.name}"
                   onerror="if(!this.dataset.err){this.dataset.err=1; this.src=this.src.endsWith('.webp')?this.src.replace('.webp','.png'):(this.src.endsWith('.png')?this.src.replace('.png','.jpg'):this.src.replace('.jpg','.webp'));}"
                   class="w-10 h-10 rounded-lg object-cover bg-white/10 border border-[#C5A059]/40 shrink-0">
              <div class="flex-1 min-w-0 text-left">
                <div class="flex items-center justify-between gap-1">
                  <span class="text-[8.5px] uppercase tracking-wider font-bold text-[#E5C985] block truncate">${item.type}</span>
                  <span class="text-[11px] font-bold text-[#E5C985] shrink-0">₹${item.price.toLocaleString('en-IN')}</span>
                </div>
                <h5 class="text-xs font-serif font-normal text-white truncate leading-snug">${item.name}</h5>
                <div class="mt-1 pt-1 border-t border-white/10 flex items-center justify-between text-[9px] text-stone-300">
                  <span class="text-stone-400">Click to view piece</span>
                  <span class="text-[#E5C985] font-bold flex items-center gap-1 hover:underline">
                    <span>Shop Piece</span>
                    <svg class="lucide lucide-arrow-right w-2.5 h-2.5" fill="none" height="24" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="24"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg>
                  </span>
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
          <img src="${item.image}" alt="${item.name}" onerror="if(!this.dataset.err){this.dataset.err=1; this.src=this.src.endsWith('.webp')?this.src.replace('.webp','.png'):(this.src.endsWith('.png')?this.src.replace('.png','.jpg'):this.src.replace('.jpg','.webp'));}" class="w-14 h-14 rounded-xl object-cover border border-[#CEBDA7] bg-white shrink-0 group-hover:scale-105 transition-transform">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-[8.5px] uppercase tracking-wider font-bold text-[#61532E]">${item.type}</span>
            </div>
            <h4 class="font-serif text-sm sm:text-base font-normal text-stone-900 group-hover:text-[#61532E] transition-colors truncate">${item.name}</h4>
            <p class="text-[11px] text-stone-500 font-light truncate mt-0.5">${item.metal}</p>
          </div>
          <div class="text-right shrink-0">
            <div class="font-bold text-sm text-[#61532E]">₹${item.price.toLocaleString('en-IN')}</div>
            <div class="text-[11px] text-stone-400 line-through">₹${item.mrp.toLocaleString('en-IN')}</div>
          </div>
        </div>
      `).join('');

      // Ultra-Clean, Professional Layout
      grid.innerHTML = `
        <!-- Left Column: Pure Editorial Portrait with Perfectly Contained Hotspots -->
        <div class="lg:col-span-5 flex justify-center items-center">
          <div id="combo-left-col" class="h-[380px] xs:h-[410px] sm:h-[440px] aspect-[2/3] relative rounded-2xl overflow-hidden shadow-xs border border-[#CEBDA7] group bg-stone-900 select-none">
            <img src="${combo.editorialImg}" alt="${combo.name}" draggable="false" class="w-full h-full object-cover block pointer-events-none animate-fadeIn">
            
            <!-- Glowing Hotspots (Pinpoint calibrated on jewelry) -->
            ${pinsHtml}

            <!-- Smart Popovers (Direct children of card, strictly clamped inside container) -->
            ${popoversHtml}
          </div>
        </div>

        <!-- Right Column: Refined Luxury Card (Zero redundant text, perfectly balanced whitespace) -->
        <div id="combo-right-col" class="lg:col-span-7 h-auto lg:h-[440px] flex flex-col justify-between bg-white rounded-2xl p-5 sm:p-6 lg:p-7 border border-[#CEBDA7] shadow-xs animate-fadeIn">
          <div>
            <!-- Clean Header: Eyebrow + Title + Savings Badge -->
            <div class="flex items-start justify-between pb-4 border-b border-[#CEBDA7] gap-2">
              <div>
                <span class="text-[9.5px] text-[#61532E] uppercase tracking-widest font-bold block">${combo.tag}</span>
                <h3 class="text-lg sm:text-xl font-serif font-normal text-stone-900 leading-tight mt-0.5">${combo.name}</h3>
              </div>
              <span class="text-[11px] text-[#61532E] font-bold bg-[#61532E]/8 px-3 py-1 rounded-full border border-[#61532E]/20 uppercase tracking-wider shrink-0">
                Save ₹${combo.savings.toLocaleString('en-IN')}
              </span>
            </div>

            <!-- Matched Pieces List -->
            <div class="space-y-3 mt-4">
              ${itemsHtml}
            </div>
          </div>

          <!-- Bundle Pricing & Immediate CTA -->
          <div class="pt-4 border-t border-[#CEBDA7] flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-4">
            <div>
              <div class="text-[9.5px] text-stone-500 uppercase tracking-wider font-semibold">Complete Set Price</div>
              <div class="flex items-baseline gap-2 mt-0.5">
                <span class="font-serif text-2xl font-bold text-[#61532E]">₹${combo.bundlePrice.toLocaleString('en-IN')}</span>
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

      // Helper function to set active hotspot (with smart clamping & zero clipping)
      function setActiveHotspot(itemId) {
        activeHotspotItemId = itemId;
        const isDesktop = window.innerWidth >= 1024;
        const allPins = grid.querySelectorAll('.combo-hotspot-pin');
        const allCards = grid.querySelectorAll('[data-combo-item]');
        const allPopovers = grid.querySelectorAll('[data-popover]');

        allPins.forEach(pin => {
          const pId = pin.getAttribute('data-hotspot-id');
          const btn = pin.querySelector('button');
          if (pId === itemId) {
            if (btn) btn.className = 'w-4 h-4 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer scale-125 bg-[#61532E] ring-2 ring-[#D4AF37] shadow-[0_0_12px_rgba(212,175,55,0.7)]';
          } else {
            if (btn) btn.className = 'w-4 h-4 rounded-full flex items-center justify-center transition-all duration-300 border border-[#D4AF37] shadow-sm cursor-pointer bg-[#61532E] hover:scale-125';
          }
        });

        allPopovers.forEach(popover => {
          const pId = popover.getAttribute('data-popover');
          if (pId === itemId) {
            const item = combo.items.find(i => i.id === itemId);
            if (item && item.hotspot) {
              if (isDesktop) {
                const pcX = item.hotspot.pcX !== undefined ? item.hotspot.pcX : item.hotspot.x;
                const pcY = item.hotspot.pcY !== undefined ? item.hotspot.pcY : item.hotspot.y;

                // Smart positioning: stay strictly 12px inside the card boundaries
                popover.style.right = (pcX > 50) ? '12px' : 'auto';
                popover.style.left = (pcX <= 50) ? '12px' : 'auto';
                popover.style.bottom = (pcY >= 45) ? `calc(${100 - pcY}% + 14px)` : 'auto';
                popover.style.top = (pcY < 45) ? `calc(${pcY}% + 14px)` : 'auto';
                popover.style.width = '230px';
              } else {
                // Mobile: Clean bottom banner card that never obstructs model or clips
                popover.style.bottom = '10px';
                popover.style.left = '10px';
                popover.style.right = '10px';
                popover.style.top = 'auto';
                popover.style.width = 'auto';
              }
            }
            popover.classList.remove('opacity-0', 'scale-95', 'invisible');
            popover.classList.add('opacity-100', 'scale-100', 'visible');
          } else {
            popover.classList.remove('opacity-100', 'scale-100', 'visible');
            popover.classList.add('opacity-0', 'scale-95', 'invisible');
          }
        });

        allCards.forEach(card => {
          const cId = card.getAttribute('data-combo-item');
          if (cId === itemId) {
            card.className = 'flex items-center gap-3.5 p-3.5 rounded-xl transition-all cursor-pointer group border bg-[#61532E]/10 border-[#61532E] shadow-sm ring-1 ring-[#61532E]/30 scale-[1.01]';
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

      // Dismiss popover when clicking anywhere outside pins on mobile
      document.addEventListener('click', (e) => {
        if (!e.target.closest('#combo-left-col')) {
          setActiveHotspot(null);
        }
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
\n"""

updated_content = content[:s_idx] + new_init_styling_combos + content[e_idx:]
with open('jewellery-design-html/js/app.js', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Successfully updated app.js with smart clamping and zero clipping!")
