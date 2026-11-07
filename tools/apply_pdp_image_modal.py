import os

app_js_path = os.path.abspath('jewellery-design-html/js/app.js')

with open(app_js_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "// Lightbox Magnifier Fullscreen Modal (Luxury Solystra Atelier UI/UX Matching React)"
end_marker = "// Mobile Filter Drawer Modal for Catalog (Interactive Multi-Select with In-Place Refresh & Curated Dropdown)"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error: Markers not found! start_idx={start_idx}, end_idx={end_idx}")
    exit(1)

new_modal_code = """// Lightbox Magnifier Fullscreen Modal (Luxury Centered Modal with Normal Zoom, Fullscreen & Simple Left/Right Arrows)
  let lightboxCurrentIndex = 0;
  let lightboxImages = [];
  let lightboxZoomLevel = 1;
  let lightboxIsFullscreen = false;
  let lightboxTouchStartX = 0;
  let lightboxTouchEndX = 0;
  let lightboxPrevOverflow = '';

  window.openImageLightbox = function (initialSrc, product) {
    if (!product && window.PRODUCTS) {
      const params = new URLSearchParams(window.location.search);
      const prodId = params.get('id');
      product = window.PRODUCTS.find(p => p.id === prodId) || window.PRODUCTS[0];
    }

    // Determine current images list
    if (product && product.images && product.images.length > 0) {
      lightboxImages = product.images;
    } else {
      const mainImg = document.getElementById('pdp-main-img');
      const thumbImgs = Array.from(document.querySelectorAll('#pdp-thumbnails img')).map(img => img.src);
      if (thumbImgs.length > 0) {
        lightboxImages = thumbImgs;
      } else if (mainImg && mainImg.src) {
        lightboxImages = [mainImg.src];
      } else {
        lightboxImages = [initialSrc || 'solystra_assets/solystra_logo.webp'];
      }
    }

    // Find current index
    const activeSrc = initialSrc || (document.getElementById('pdp-main-img') ? document.getElementById('pdp-main-img').src : '');
    lightboxCurrentIndex = 0;
    if (activeSrc) {
      const matchIdx = lightboxImages.findIndex(img => img.includes(activeSrc) || activeSrc.includes(img));
      if (matchIdx !== -1) lightboxCurrentIndex = matchIdx;
    }

    lightboxZoomLevel = 1;
    lightboxIsFullscreen = false;

    // Lock background scroll without shifting layout
    lightboxPrevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    let lb = document.getElementById('pdp-lightbox-modal');
    if (!lb) {
      lb = document.createElement('div');
      lb.id = 'pdp-lightbox-modal';
      document.body.appendChild(lb);
    }
    
    // Backdrop overlay: centered dialog container with luxury blur
    lb.style.cssText = 'position:fixed; inset:0; z-index:999999; background:rgba(18, 14, 10, 0.72); backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px); display:flex; align-items:center; justify-content:center; padding:12px; font-family:"Plus Jakarta Sans", sans-serif; box-sizing:border-box; user-select:none;';

    function renderLightbox() {
      const currentImg = lightboxImages[lightboxCurrentIndex] || lightboxImages[0];
      const prodName = (product && product.name) ? product.name : (document.getElementById('pdp-title') ? document.getElementById('pdp-title').textContent : 'Solystra Fine Jewelry Atelier');
      const totalImages = lightboxImages.length;
      const isZoomed = lightboxZoomLevel > 1.05;

      const dialogClass = lightboxIsFullscreen
        ? 'relative w-full max-w-[96vw] h-[92vh] bg-white rounded-2xl sm:rounded-3xl shadow-2xl border border-[#CEBDA7] flex flex-col overflow-hidden my-auto transition-all duration-300'
        : 'relative w-full max-w-2xl lg:max-w-3xl bg-white rounded-2xl sm:rounded-3xl shadow-2xl border border-[#CEBDA7] flex flex-col overflow-hidden my-auto transition-all duration-300';

      const stageHeightClass = lightboxIsFullscreen
        ? 'h-[72vh] sm:h-[76vh]'
        : 'max-h-[50vh] sm:max-h-[58vh]';

      lb.innerHTML = `
        <!-- Modal Backdrop Dismiss Layer -->
        <div class="absolute inset-0 -z-10 pdp-modal-backdrop-dismiss" onclick="window.closeImageLightbox()"></div>

        <!-- Centered Luxury Modal Dialog -->
        <div class="${dialogClass}" role="dialog" aria-modal="true" aria-label="Product Image Preview" onclick="event.stopPropagation()">
          
          <!-- Top Header Bar: Title, Angle Pill, Normal Zoom/Fullscreen toggle, Close Button -->
          <div class="flex items-center justify-between px-3.5 sm:px-5 py-2.5 sm:py-3 bg-white border-b border-[#E8DFC8]/70 shrink-0">
            <div class="min-w-0 pr-2 flex items-center gap-2">
              <h3 class="font-serif text-xs sm:text-sm font-medium text-stone-900 truncate tracking-wide max-w-[170px] sm:max-w-md">${prodName}</h3>
              <span class="inline-flex items-center text-[10px] sm:text-[11px] font-mono font-bold text-[#61532E] bg-[#FAF5F0] border border-[#CEBDA7]/70 px-2 py-0.5 rounded-full shrink-0 shadow-2xs">
                ${lightboxCurrentIndex + 1} / ${totalImages}
              </span>
            </div>

            <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
              <!-- Zoom Indicator / Toggle Button -->
              <button onclick="window.toggleLightboxZoom()" class="flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-mono font-medium transition-all cursor-pointer ${isZoomed ? 'bg-[#61532E] text-white shadow-2xs' : 'bg-stone-100 hover:bg-stone-200 text-stone-700'}" title="${isZoomed ? 'Click for Normal Zoom (1x)' : 'Click to Inspect Details (1.8x)'}">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  ${isZoomed 
                    ? '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/>'
                    : '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/>'}
                </svg>
                <span>${Math.round(lightboxZoomLevel * 100)}%</span>
              </button>

              <!-- Fullscreen / Theater Toggle Button -->
              <button onclick="window.toggleLightboxFullscreen()" class="p-1.5 sm:p-2 rounded-full bg-stone-100 hover:bg-[#61532E] hover:text-white text-stone-700 transition-all cursor-pointer border border-stone-200/60 flex items-center justify-center active:scale-95" title="${lightboxIsFullscreen ? 'Exit Fullscreen' : 'Expand Fullscreen'}">
                <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  ${lightboxIsFullscreen
                    ? '<path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3"/>'
                    : '<path d="M15 3h6v6m0-6-7 7M9 21H3v-6m0 6 7-7m11-5v6m0 0h-6m-8-12H3v6m0-6 7 7"/>'}
                </svg>
              </button>

              <!-- Close Button -->
              <button onclick="window.closeImageLightbox()" aria-label="Close" class="p-1.5 sm:p-2 rounded-full bg-stone-100 hover:bg-[#61532E] hover:text-white text-stone-700 transition-all cursor-pointer border border-stone-200/60 flex items-center justify-center active:scale-95 ml-0.5" title="Close (Esc)">
                <svg class="w-4 h-4 sm:w-4.5 sm:h-4.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
              </button>
            </div>
          </div>

          <!-- Center Stage with Image and Simple Left-Right Arrow Buttons -->
          <div class="relative w-full aspect-square sm:aspect-[4/3] ${stageHeightClass} bg-[#FAF8F5] flex items-center justify-center overflow-hidden p-3 sm:p-6 select-none" id="lightbox-stage">
            
            <!-- Left Navigation Button -->
            ${totalImages > 1 ? `
              <button onclick="window.prevLightboxImage(event)" aria-label="Previous Image" class="absolute left-2.5 sm:left-4 top-1/2 -translate-y-1/2 z-20 w-9 h-9 sm:w-11 sm:h-11 rounded-full bg-white/95 hover:bg-[#61532E] text-stone-800 hover:text-white border border-[#CEBDA7] shadow-md flex items-center justify-center transition-all cursor-pointer active:scale-95" title="Previous (Left Arrow)">
                <svg class="w-4.5 h-4.5 sm:w-5 sm:h-5 -translate-x-px" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg>
              </button>
            ` : ''}

            <!-- Main Product Image (Click to Toggle Normal / Zoom) -->
            <div class="relative w-full h-full flex items-center justify-center overflow-hidden">
              <img id="lightbox-main-img" src="${currentImg}" alt="${prodName}"
                class="max-w-full max-h-full object-contain mx-auto transition-transform duration-300 select-none ${isZoomed ? 'cursor-zoom-out' : 'cursor-zoom-in'}"
                style="transform: scale(${lightboxZoomLevel}); transform-origin: center center;"
                onclick="window.toggleLightboxZoom()" />
            </div>

            <!-- Right Navigation Button -->
            ${totalImages > 1 ? `
              <button onclick="window.nextLightboxImage(event)" aria-label="Next Image" class="absolute right-2.5 sm:right-4 top-1/2 -translate-y-1/2 z-20 w-9 h-9 sm:w-11 sm:h-11 rounded-full bg-white/95 hover:bg-[#61532E] text-stone-800 hover:text-white border border-[#CEBDA7] shadow-md flex items-center justify-center transition-all cursor-pointer active:scale-95" title="Next (Right Arrow)">
                <svg class="w-4.5 h-4.5 sm:w-5 sm:h-5 translate-x-px" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
              </button>
            ` : ''}
          </div>

          <!-- Bottom Footer Bar: Simple Angle Thumbnails -->
          ${totalImages > 1 ? `
            <div class="flex items-center justify-center gap-2 sm:gap-2.5 py-2.5 sm:py-3 px-3 bg-white border-t border-[#E8DFC8]/60 overflow-x-auto no-scrollbar shrink-0">
              ${lightboxImages.map((src, i) => `
                <button onclick="window.selectLightboxIndex(${i})" aria-label="Angle ${i + 1}" class="relative w-10 h-10 sm:w-12 sm:h-12 rounded-xl overflow-hidden border-2 transition-all cursor-pointer shrink-0 ${i === lightboxCurrentIndex ? 'border-[#61532E] ring-2 ring-[#61532E]/30 scale-105 shadow-xs' : 'border-[#CEBDA7]/60 opacity-60 hover:opacity-100 hover:border-[#61532E]/60'}">
                  <img src="${src}" class="w-full h-full object-cover" alt="Angle ${i + 1}" />
                </button>
              `).join('')}
            </div>
          ` : ''}

        </div>
      `;
      lb.style.display = 'flex';

      // Setup touch swiping for mobile
      const stage = document.getElementById('lightbox-stage');
      if (stage) {
        stage.ontouchstart = function (e) {
          lightboxTouchStartX = e.changedTouches[0].screenX;
        };
        stage.ontouchend = function (e) {
          lightboxTouchEndX = e.changedTouches[0].screenX;
          const diff = lightboxTouchEndX - lightboxTouchStartX;
          if (Math.abs(diff) > 40) {
            if (diff < 0) {
              window.nextLightboxImage();
            } else {
              window.prevLightboxImage();
            }
          }
        };
      }
    }

    window.closeImageLightbox = function () {
      if (lb) lb.style.display = 'none';
      lightboxZoomLevel = 1;
      lightboxIsFullscreen = false;
      document.body.style.overflow = lightboxPrevOverflow || '';
    };

    window.prevLightboxImage = function (e) {
      if (e) e.stopPropagation();
      lightboxCurrentIndex = (lightboxCurrentIndex - 1 + lightboxImages.length) % lightboxImages.length;
      lightboxZoomLevel = 1;
      renderLightbox();
      window.syncPdpMainImageFromLightbox && window.syncPdpMainImageFromLightbox(lightboxCurrentIndex);
    };

    window.nextLightboxImage = function (e) {
      if (e) e.stopPropagation();
      lightboxCurrentIndex = (lightboxCurrentIndex + 1) % lightboxImages.length;
      lightboxZoomLevel = 1;
      renderLightbox();
      window.syncPdpMainImageFromLightbox && window.syncPdpMainImageFromLightbox(lightboxCurrentIndex);
    };

    window.selectLightboxIndex = function (idx) {
      lightboxCurrentIndex = idx;
      lightboxZoomLevel = 1;
      renderLightbox();
      window.syncPdpMainImageFromLightbox && window.syncPdpMainImageFromLightbox(lightboxCurrentIndex);
    };

    window.toggleLightboxZoom = function () {
      lightboxZoomLevel = lightboxZoomLevel > 1.1 ? 1 : 1.8;
      renderLightbox();
    };

    window.toggleLightboxFullscreen = function () {
      lightboxIsFullscreen = !lightboxIsFullscreen;
      renderLightbox();
    };

    window.syncPdpMainImageFromLightbox = function (idx) {
      const thumbsContainer = document.getElementById('pdp-thumbnails');
      if (thumbsContainer) {
        const thumbBtns = thumbsContainer.querySelectorAll('button');
        if (thumbBtns[idx]) {
          thumbBtns[idx].click();
        }
      }
    };

    function handleKeyDown(e) {
      if (lb.style.display === 'none') return;
      if (e.key === 'Escape') window.closeImageLightbox();
      else if (e.key === 'ArrowLeft') window.prevLightboxImage();
      else if (e.key === 'ArrowRight') window.nextLightboxImage();
    }
    window.removeEventListener('keydown', handleKeyDown);
    window.addEventListener('keydown', handleKeyDown);

    renderLightbox();
  };

  """

new_content = content[:start_idx] + new_modal_code + content[end_idx:]

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully replaced Lightbox Magnifier code in app.js!")

