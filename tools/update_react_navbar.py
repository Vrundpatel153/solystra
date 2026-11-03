import os

navbar_path = os.path.abspath('src/components/Navbar.jsx')
with open(navbar_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update State & Handlers
OLD_STATE = """  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuContainerRef = useRef(null);

  const handleNavClick = (cat) => {
    if (onSelectCategory) {
      onSelectCategory(cat);
    }
    if (window.location.hash.startsWith('#/product/')) {
      window.location.hash = '#/';
    }
    setIsMenuOpen(false);
  };"""

NEW_STATE = """  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [openMetalDesktop, setOpenMetalDesktop] = useState('silver');
  const [openMetalMobile, setOpenMetalMobile] = useState('silver');
  const menuContainerRef = useRef(null);

  const handleNavClick = (cat) => {
    if (onSelectCategory) {
      onSelectCategory(cat);
    }
    if (window.location.hash.startsWith('#/product/')) {
      window.location.hash = '#/';
    }
    setIsMenuOpen(false);
  };

  const handleSubcatClick = (metal, category) => {
    window.location.hash = `#/products?metal=${metal}&category=${category}`;
    setIsMenuOpen(false);
  };

  const handleMetalClick = (metal) => {
    window.location.hash = `#/products?metal=${metal}`;
    setIsMenuOpen(false);
  };"""

if OLD_STATE in content:
    content = content.replace(OLD_STATE, NEW_STATE, 1)
else:
    # Try normalizing newlines
    c_norm = content.replace('\r\n', '\n')
    if OLD_STATE.replace('\r\n', '\n') in c_norm:
        content = c_norm.replace(OLD_STATE.replace('\r\n', '\n'), NEW_STATE.replace('\r\n', '\n'), 1)

# 2. Update Column 2 Desktop
OLD_COL2 = """            {/* Column 2: Jewelry Categories (3 cols) */}
            <div className="col-span-3 space-y-3 border-r border-[#CEBDA7]/80 pr-6">
              <div className="text-[11px] uppercase tracking-[0.2em] text-stone-800 font-bold pb-2 border-b border-[#CEBDA7]/60">
                Jewelry Categories
              </div>
              <div className="space-y-0.5 pt-1">
                {CATEGORY_ITEMS.map((cat, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(cat.category)}
                    className="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#FAF8F5] transition-all cursor-pointer group flex items-center justify-between"
                  >
                    <div>
                      <div className="text-[13px] font-sans font-semibold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight">
                        {cat.label}
                      </div>
                      <div className="text-[11px] text-stone-400 font-light mt-0.5">
                        {cat.desc}
                      </div>
                    </div>
                    <ChevronRight className="w-3.5 h-3.5 text-stone-300 group-hover:text-[#61532E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" />
                  </button>
                ))}
                
                <button
                  onClick={() => {
                    window.location.hash = '#/categories';
                    setIsMenuOpen(false);
                  }}
                  className="w-full text-left py-2 px-2.5 -mx-2.5 rounded-xl hover:bg-[#F6F3EE] transition-all cursor-pointer group flex items-center justify-between mt-2 pt-2 border-t border-[#CEBDA7]/60"
                >
                  <div className="text-[12px] font-semibold text-[#61532E] group-hover:text-[#3D341B] flex items-center gap-1.5">
                    <span>Explore All Categories</span>
                    <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </button>
              </div>
            </div>"""

NEW_COL2 = """            {/* Column 2: Jewelry Categories (3 cols) - 925 Silver & 18K Gold Dropdowns */}
            <div className="col-span-3 space-y-3 border-r border-[#CEBDA7]/80 pr-6">
              <div className="text-[11px] uppercase tracking-[0.2em] text-stone-800 font-bold pb-2 border-b border-[#CEBDA7]/60 flex items-center justify-between">
                <span>Jewelry Categories</span>
                <span className="text-[9.5px] text-[#61532E] font-semibold tracking-wider uppercase">By Metal</span>
              </div>
              <div className="space-y-2 pt-1">
                {/* 1. 925 Silver Accordion / Dropdown */}
                <div className="rounded-xl border border-[#CEBDA7] bg-white overflow-hidden shadow-2xs transition-all duration-300">
                  <button
                    type="button"
                    onClick={() => setOpenMetalDesktop(openMetalDesktop === 'silver' ? null : 'silver')}
                    className="w-full flex items-center justify-between p-2.5 bg-[#FAF8F5] hover:bg-[#F6F3EE] text-left cursor-pointer transition-colors group select-none"
                    aria-expanded={openMetalDesktop === 'silver'}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="w-3.5 h-3.5 rounded-full border border-white shadow-xs shrink-0" style={{ background: 'linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 50%, #64748B 100%)' }} />
                      <div>
                        <div className="text-[13px] font-sans font-bold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight flex items-center gap-1.5">
                          <span>925 Silver</span>
                          <span className="text-[8.5px] px-1.5 py-0.2 rounded bg-white text-[#61532E] border border-[#CEBDA7]/80 font-bold uppercase">Pure 92.5%</span>
                        </div>
                        <div className="text-[10px] text-stone-400 font-light mt-0.5">Handcrafted Sterling Silver</div>
                      </div>
                    </div>
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-300 ${openMetalDesktop === 'silver' ? 'rotate-180 text-[#61532E]' : 'text-stone-500 group-hover:text-[#61532E]'}`} />
                  </button>

                  {openMetalDesktop === 'silver' && (
                    <div className="space-y-0.5 p-1.5 bg-white border-t border-[#CEBDA7]/60 transition-all duration-300">
                      {CATEGORY_ITEMS.map((cat, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSubcatClick('silver', cat.category)}
                          className="w-full text-left py-1.5 px-2 rounded-lg hover:bg-[#FAF8F5] transition-all cursor-pointer group flex items-center justify-between"
                        >
                          <div>
                            <div className="text-[12.5px] font-sans font-semibold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight">
                              {cat.label}
                            </div>
                            <div className="text-[10px] text-stone-400 font-light mt-0.5">
                              {cat.desc}
                            </div>
                          </div>
                          <ChevronRight className="w-3.5 h-3.5 text-stone-300 group-hover:text-[#61532E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" />
                        </button>
                      ))}
                      <div className="pt-1.5 border-t border-stone-100 mt-1">
                        <button
                          onClick={() => handleMetalClick('silver')}
                          className="w-full py-1 text-center text-[11px] font-bold text-[#61532E] hover:underline flex items-center justify-center gap-1 cursor-pointer"
                        >
                          <span>Shop All 925 Silver Collection</span>
                          <ChevronRight className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {/* 2. 18K Gold Accordion / Dropdown */}
                <div className="rounded-xl border border-[#CEBDA7] bg-white overflow-hidden shadow-2xs transition-all duration-300">
                  <button
                    type="button"
                    onClick={() => setOpenMetalDesktop(openMetalDesktop === 'gold' ? null : 'gold')}
                    className="w-full flex items-center justify-between p-2.5 bg-[#FAF8F5] hover:bg-[#F6F3EE] text-left cursor-pointer transition-colors group select-none"
                    aria-expanded={openMetalDesktop === 'gold'}
                  >
                    <div className="flex items-center gap-2.5">
                      <span className="w-3.5 h-3.5 rounded-full border border-white shadow-xs shrink-0" style={{ background: 'linear-gradient(135deg, #F3DFB0 0%, #C5A059 50%, #8C6118 100%)' }} />
                      <div>
                        <div className="text-[13px] font-sans font-bold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight flex items-center gap-1.5">
                          <span>18K Gold</span>
                          <span className="text-[8.5px] px-1.5 py-0.2 rounded bg-white text-[#C5A059] border border-[#CEBDA7]/80 font-bold uppercase">Vermeil Suite</span>
                        </div>
                        <div className="text-[10px] text-stone-400 font-light mt-0.5">18K Gold Vermeil &amp; Italian Polish</div>
                      </div>
                    </div>
                    <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-300 ${openMetalDesktop === 'gold' ? 'rotate-180 text-[#61532E]' : 'text-stone-500 group-hover:text-[#61532E]'}`} />
                  </button>

                  {openMetalDesktop === 'gold' && (
                    <div className="space-y-0.5 p-1.5 bg-white border-t border-[#CEBDA7]/60 transition-all duration-300">
                      {CATEGORY_ITEMS.map((cat, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSubcatClick('gold', cat.category)}
                          className="w-full text-left py-1.5 px-2 rounded-lg hover:bg-[#FAF8F5] transition-all cursor-pointer group flex items-center justify-between"
                        >
                          <div>
                            <div className="text-[12.5px] font-sans font-semibold text-stone-900 group-hover:text-[#61532E] transition-colors leading-tight">
                              {cat.label}
                            </div>
                            <div className="text-[10px] text-stone-400 font-light mt-0.5">
                              {cat.desc}
                            </div>
                          </div>
                          <ChevronRight className="w-3.5 h-3.5 text-stone-300 group-hover:text-[#61532E] group-hover:translate-x-0.5 transition-all opacity-0 group-hover:opacity-100" />
                        </button>
                      ))}
                      <div className="pt-1.5 border-t border-stone-100 mt-1">
                        <button
                          onClick={() => handleMetalClick('gold')}
                          className="w-full py-1 text-center text-[11px] font-bold text-[#C5A059] hover:underline flex items-center justify-center gap-1 cursor-pointer"
                        >
                          <span>Shop All 18K Gold Collection</span>
                          <ChevronRight className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Explore All Categories Archive Link */}
                <button
                  onClick={() => {
                    window.location.hash = '#/categories';
                    setIsMenuOpen(false);
                  }}
                  className="w-full text-left py-2 px-2.5 rounded-xl hover:bg-[#F6F3EE] transition-all cursor-pointer group flex items-center justify-between pt-2 border-t border-[#CEBDA7]/60"
                >
                  <div className="text-[12px] font-semibold text-[#61532E] group-hover:text-[#3D341B] flex items-center gap-1.5">
                    <span>Explore All Categories Archive</span>
                    <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                  </div>
                </button>
              </div>
            </div>"""

if OLD_COL2 in content:
    content = content.replace(OLD_COL2, NEW_COL2, 1)
else:
    c_norm = content.replace('\r\n', '\n')
    if OLD_COL2.replace('\r\n', '\n') in c_norm:
        content = c_norm.replace(OLD_COL2.replace('\r\n', '\n'), NEW_COL2.replace('\r\n', '\n'), 1)

# 3. Update Mobile Categories
OLD_MOB = """            {/* Categories List */}
            <div className="space-y-1 pb-3 border-b border-[#CEBDA7]">
              <div className="text-[11px] font-bold uppercase tracking-wider text-stone-900 mb-1.5">
                Categories
              </div>
              <div className="grid grid-cols-2 gap-1.5">
                {CATEGORY_ITEMS.map((cat, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleNavClick(cat.category)}
                    className="p-2 bg-white rounded-lg border border-[#CEBDA7] text-left text-xs font-medium text-stone-800 cursor-pointer"
                  >
                    <div className="font-semibold">{cat.label.split(' ')[0]}</div>
                    <div className="text-[9.5px] text-stone-400 mt-0.5 truncate">{cat.label}</div>
                  </button>
                ))}

                <button
                  onClick={() => {
                    window.location.hash = '#/categories';
                    setIsMenuOpen(false);
                  }}
                  className="col-span-2 p-2.5 bg-[#F6F3EE] rounded-lg border border-[#61532E]/20 text-center text-xs font-semibold text-[#61532E] hover:bg-[#EFEAE3] transition-colors cursor-pointer flex items-center justify-center gap-1.5"
                >
                  <span>Explore All Categories Archive</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>"""

NEW_MOB = """            {/* Categories List (Mobile 925 Silver & 18K Gold Accordions) */}
            <div className="space-y-2 pb-3 border-b border-[#CEBDA7]">
              <div className="text-[11px] font-bold uppercase tracking-wider text-stone-900 mb-1.5 flex items-center justify-between">
                <span>Jewelry Categories</span>
                <span className="text-[9.5px] text-[#61532E] font-semibold">925 Silver &amp; 18K Gold</span>
              </div>

              {/* Mobile 925 Silver Accordion */}
              <div className="rounded-xl border border-[#CEBDA7] bg-white overflow-hidden shadow-2xs">
                <button
                  type="button"
                  onClick={() => setOpenMetalMobile(openMetalMobile === 'silver' ? null : 'silver')}
                  className="w-full flex items-center justify-between p-2.5 bg-[#FAF8F5] text-left cursor-pointer active:bg-[#F6F3EE]"
                >
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full border border-white shrink-0" style={{ background: 'linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 50%, #64748B 100%)' }} />
                    <div>
                      <div className="text-xs font-bold text-stone-900 flex items-center gap-1.5">
                        <span>925 Silver</span>
                        <span className="text-[8.5px] px-1 py-0.2 rounded bg-white text-[#61532E] border border-[#CEBDA7]/80 font-bold uppercase">Pure 92.5%</span>
                      </div>
                      <div className="text-[9.5px] text-stone-400">Handcrafted Sterling Silver</div>
                    </div>
                  </div>
                  <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-300 ${openMetalMobile === 'silver' ? 'rotate-180 text-[#61532E]' : 'text-stone-500'}`} />
                </button>

                {openMetalMobile === 'silver' && (
                  <div className="space-y-0.5 p-2 bg-white border-t border-[#CEBDA7]/60">
                    {CATEGORY_ITEMS.map((cat, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSubcatClick('silver', cat.category)}
                        className="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer"
                      >
                        <div>
                          <div className="font-semibold text-stone-900">{cat.label}</div>
                          <div className="text-[9.5px] text-stone-400">{cat.desc}</div>
                        </div>
                        <ChevronRight className="w-3 h-3 text-stone-400" />
                      </button>
                    ))}
                    <div className="pt-1.5 border-t border-stone-100">
                      <button
                        onClick={() => handleMetalClick('silver')}
                        className="w-full py-1 text-center text-[10.5px] font-bold text-[#61532E] hover:underline flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <span>Shop All 925 Silver</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Mobile 18K Gold Accordion */}
              <div className="rounded-xl border border-[#CEBDA7] bg-white overflow-hidden shadow-2xs">
                <button
                  type="button"
                  onClick={() => setOpenMetalMobile(openMetalMobile === 'gold' ? null : 'gold')}
                  className="w-full flex items-center justify-between p-2.5 bg-[#FAF8F5] text-left cursor-pointer active:bg-[#F6F3EE]"
                >
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full border border-white shrink-0" style={{ background: 'linear-gradient(135deg, #F3DFB0 0%, #C5A059 50%, #8C6118 100%)' }} />
                    <div>
                      <div className="text-xs font-bold text-stone-900 flex items-center gap-1.5">
                        <span>18K Gold</span>
                        <span className="text-[8.5px] px-1 py-0.2 rounded bg-white text-[#C5A059] border border-[#CEBDA7]/80 font-bold uppercase">Vermeil Suite</span>
                      </div>
                      <div className="text-[9.5px] text-stone-400">18K Gold Vermeil &amp; Polish</div>
                    </div>
                  </div>
                  <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-300 ${openMetalMobile === 'gold' ? 'rotate-180 text-[#61532E]' : 'text-stone-500'}`} />
                </button>

                {openMetalMobile === 'gold' && (
                  <div className="space-y-0.5 p-2 bg-white border-t border-[#CEBDA7]/60">
                    {CATEGORY_ITEMS.map((cat, idx) => (
                      <button
                        key={idx}
                        onClick={() => handleSubcatClick('gold', cat.category)}
                        className="w-full text-left py-1.5 px-2 rounded-lg hover:bg-stone-50 flex items-center justify-between text-xs cursor-pointer"
                      >
                        <div>
                          <div className="font-semibold text-stone-900">{cat.label}</div>
                          <div className="text-[9.5px] text-stone-400">{cat.desc}</div>
                        </div>
                        <ChevronRight className="w-3 h-3 text-stone-400" />
                      </button>
                    ))}
                    <div className="pt-1.5 border-t border-stone-100">
                      <button
                        onClick={() => handleMetalClick('gold')}
                        className="w-full py-1 text-center text-[10.5px] font-bold text-[#C5A059] hover:underline flex items-center justify-center gap-1 cursor-pointer"
                      >
                        <span>Shop All 18K Gold</span>
                        <ChevronRight className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {/* Mobile All Categories Link */}
              <button
                onClick={() => {
                  window.location.hash = '#/categories';
                  setIsMenuOpen(false);
                }}
                className="w-full p-2.5 bg-[#F6F3EE] rounded-lg border border-[#61532E]/20 text-center text-xs font-semibold text-[#61532E] hover:bg-[#EFEAE3] transition-colors cursor-pointer flex items-center justify-center gap-1.5"
              >
                <span>Explore All Categories Archive</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>"""

if OLD_MOB in content:
    content = content.replace(OLD_MOB, NEW_MOB, 1)
else:
    c_norm = content.replace('\r\n', '\n')
    if OLD_MOB.replace('\r\n', '\n') in c_norm:
        content = c_norm.replace(OLD_MOB.replace('\r\n', '\n'), NEW_MOB.replace('\r\n', '\n'), 1)

with open(navbar_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated React Navbar.jsx successfully!")

