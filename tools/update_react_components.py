import os

# 1. Update MetalPurityBadge.jsx
badge_file = 'src/components/MetalPurityBadge.jsx'
with open(badge_file, 'r', encoding='utf-8') as f:
    badge_code = f.read()

# Update rose
old_rose = """  if (isRose) {
    return {
      type: 'rose',
      code: '18K',
      metal: 'ROSE',
      label: '18K Rose Gold',
      borderColor: '#DF9FA9',
      borderWidth: '1.4',
      innerRingColor: '#C47585',
      filter: 'drop-shadow(0 2px 4px rgba(180, 80, 100, 0.22))',
      codeTextClass: 'text-[#61532E]',
      subTextClass: 'text-[#9E2A44]',
      stops: [
        { offset: '0%', color: '#FFF9FA' },
        { offset: '30%', color: '#FDECEF' },
        { offset: '70%', color: '#F9D4DA' },
        { offset: '100%', color: '#EBB6C0' }
      ]
    };
  }"""

new_rose = """  if (isRose) {
    return {
      type: 'rose',
      code: '18K',
      metal: 'ROSE',
      label: '18K Rose Gold',
      borderColor: '#CEBDA7',
      borderWidth: '1',
      innerRingColor: '#61532E',
      filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
      codeTextClass: 'text-[#61532E]',
      subTextClass: 'text-[#61532E]',
      stops: [
        { offset: '0%', color: '#FAF8F5' },
        { offset: '100%', color: '#FAF8F5' }
      ]
    };
  }"""

old_gold = """  if (isGold) {
    return {
      type: 'gold',
      code: '18K',
      metal: 'GOLD',
      label: '18K Gold Vermeil',
      // Warm champagne gold shade
      borderColor: '#CBA64E',
      borderWidth: '1.5',
      innerRingColor: '#BF973A',
      filter: 'drop-shadow(0 2px 5px rgba(180, 130, 40, 0.25))',
      codeTextClass: 'text-[#6B4B13]',
      subTextClass: 'text-[#8A641E]',
      stops: [
        { offset: '0%', color: '#FFFDF7' },
        { offset: '25%', color: '#FEF8E7' },
        { offset: '65%', color: '#F7E5BA' },
        { offset: '100%', color: '#ECCF86' }
      ]
    };
  }"""

new_gold = """  if (isGold) {
    return {
      type: 'gold',
      code: '18K',
      metal: 'GOLD',
      label: '18K Gold Vermeil',
      borderColor: '#CEBDA7',
      borderWidth: '1',
      innerRingColor: '#61532E',
      filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
      codeTextClass: 'text-[#61532E]',
      subTextClass: 'text-[#61532E]',
      stops: [
        { offset: '0%', color: '#FAF8F5' },
        { offset: '100%', color: '#FAF8F5' }
      ]
    };
  }"""

old_silver = """  // Pure 925 Silver (Crisp White Silver Style)
  return {
    type: 'silver',
    code: '925',
    metal: 'SILVER',
    label: 'Pure 925 Silver',
    borderColor: '#CBD5E1',
    borderWidth: '1.35',
    innerRingColor: '#94A3B8',
    filter: 'drop-shadow(0 2px 4px rgba(15, 23, 42, 0.12))',
    codeTextClass: 'text-[#1E293B]',
    subTextClass: 'text-[#64748B]',
    stops: [
      { offset: '0%', color: '#FFFFFF' },
      { offset: '30%', color: '#F8FAFC' },
      { offset: '70%', color: '#EDF2F7' },
      { offset: '100%', color: '#E2E8F0' }
    ]
  };"""

new_silver = """  // Pure 925 Silver
  return {
    type: 'silver',
    code: '925',
    metal: 'SILVER',
    label: 'Pure 925 Silver',
    borderColor: '#CEBDA7',
    borderWidth: '1',
    innerRingColor: '#61532E',
    filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.04))',
    codeTextClass: 'text-[#61532E]',
    subTextClass: 'text-[#61532E]',
    stops: [
      { offset: '0%', color: '#FAF8F5' },
      { offset: '100%', color: '#FAF8F5' }
    ]
  };"""

def rep(content, old, new):
    if old in content:
        return content.replace(old, new)
    c_norm = content.replace('\r\n', '\n')
    if old.replace('\r\n', '\n') in c_norm:
        return c_norm.replace(old.replace('\r\n', '\n'), new.replace('\r\n', '\n'))
    return content

badge_code = rep(badge_code, old_rose, new_rose)
badge_code = rep(badge_code, old_gold, new_gold)
badge_code = rep(badge_code, old_silver, new_silver)

with open(badge_file, 'w', encoding='utf-8') as f:
    f.write(badge_code)
print("Updated MetalPurityBadge.jsx")

# 2. Update ProductCard.jsx
card_file = 'src/components/ProductCard.jsx'
with open(card_file, 'r', encoding='utf-8') as f:
    card_code = f.read()

old_card_row = """        {/* Rating & Hallmark Badges Row */}
        <div className="flex items-center justify-between gap-1 sm:gap-1.5 w-full">
          {/* Rating Tag */}
          <div className="inline-flex items-center gap-1 px-1.5 sm:px-2 py-0.5 rounded-lg bg-[#FAF8F5] border border-[#CEBDA7] shadow-2xs shrink-0">
            <svg className="w-3 h-3 sm:w-3.5 sm:h-3.5 fill-[#C5A059] text-[#C5A059] shrink-0 drop-shadow-2xs" viewBox="0 0 24 24">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
            <span className="font-sans font-bold text-[10.5px] sm:text-xs text-stone-900 leading-none">
              {product.rating}
            </span>
          </div>

          {/* Metal Purity Hallmark Badge moved to Corner at that row */}
          <div className="ml-auto shrink-0 flex items-center gap-1">
            <MetalPurityBadge product={product} size="rating" selectedMetal={selectedMetal} />
          </div>
        </div>"""

new_card_row = """        {/* Discount & Metal Hallmark Badges Row */}
        <div className="flex items-center justify-between gap-1 sm:gap-1.5 w-full">
          {/* Discount Tag placed where reviews used to be */}
          <span className="inline-flex items-center justify-center px-1.5 sm:px-2 py-0.5 rounded-md bg-[#61532E]/10 border border-[#61532E]/25 text-[#61532E] font-sans font-bold text-[8.5px] sm:text-[9.5px] uppercase tracking-wider leading-none shadow-2xs shrink-0">
            {discountText || 'BIS 925'}
          </span>

          {/* Metal Purity Hallmark Badge on the right */}
          <div className="ml-auto shrink-0 flex items-center gap-1">
            <MetalPurityBadge product={product} size="rating" selectedMetal={selectedMetal} />
          </div>
        </div>"""

card_code = rep(card_code, old_card_row, new_card_row)

with open(card_file, 'w', encoding='utf-8') as f:
    f.write(card_code)
print("Updated ProductCard.jsx")

# 3. Update Navbar.jsx (close silver by default)
nav_file = 'src/components/Navbar.jsx'
with open(nav_file, 'r', encoding='utf-8') as f:
    nav_code = f.read()

nav_code = rep(nav_code, "const [openMetalDesktop, setOpenMetalDesktop] = useState('silver');", "const [openMetalDesktop, setOpenMetalDesktop] = useState(null);")
nav_code = rep(nav_code, "const [openMetalMobile, setOpenMetalMobile] = useState('silver');", "const [openMetalMobile, setOpenMetalMobile] = useState(null);")

with open(nav_file, 'w', encoding='utf-8') as f:
    f.write(nav_code)
print("Updated Navbar.jsx")

