import sys

sys.stdout.reconfigure(encoding='utf-8')

react_path = 'src/pages/ProductDetailPage.jsx'
with open(react_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = """            {/* 5. Available Offers */}
            <div className="space-y-2 pt-1">
              <div className="text-xs font-semibold text-stone-900 tracking-wide">
                Available offers
              </div>
              <div className="flex sm:grid sm:grid-cols-3 gap-2.5 overflow-x-auto sm:overflow-visible hide-scrollbar py-1.5 px-1 -mx-1">
                {[
                  { discount: 'Flat ₹100 off', min: 'On Prepaid orders', code: 'PREPAID100' },
                  { discount: 'Get 5% off', min: 'above ₹5,000', code: 'SOL5' },
                  { discount: 'Get 10% off', min: 'above ₹10,000', code: 'SOL10' }
                ].map((offer) => (
                  <button
                    key={offer.code}
                    type="button"
                    onClick={() => handleApplyOffer(offer.code)}
                    className="min-w-[130px] sm:min-w-[140px] p-3 rounded-xl bg-[#FAF5F0] border border-[#EAE0D3] text-left hover:border-[#61532E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 active:scale-95 shadow-2xs"
                  >
                    <p className="text-xs font-semibold text-stone-900 leading-tight">{offer.discount}</p>
                    <p className="text-[10px] text-stone-600 mt-0.5">{offer.min}</p>
                    <div className="mt-2 text-[10.5px] font-mono tracking-wide flex items-center justify-between">
                      <span className="text-stone-700">use <strong className="text-[#61532E] font-bold">{offer.code}</strong></span>
                      <span className="text-[8.5px] uppercase font-sans font-semibold text-stone-400 group-hover:text-[#61532E]">Apply</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>"""

replacement = """            {/* 5. Available Offers */}
            <div className="space-y-2 pt-1">
              <div className="text-xs font-semibold text-stone-900 tracking-wide flex items-center justify-between">
                <span>Available offers</span>
                <span className="text-[10.5px] text-[#61532E] font-medium">Auto-applied at checkout</span>
              </div>
              <div className="flex sm:grid sm:grid-cols-3 gap-2 sm:gap-2.5 overflow-x-auto sm:overflow-visible hide-scrollbar py-1.5 px-1 -mx-1 snap-x snap-mandatory">
                {[
                  { discount: 'Flat ₹100 off', badge: 'PREPAID', min: 'On prepaid orders', code: 'PREPAID100' },
                  { discount: 'Get 5% off', badge: '> ₹5,000', min: 'On orders above ₹5k', code: 'SOL5' },
                  { discount: 'Get 10% off', badge: '> ₹10,000', min: 'On orders above ₹10k', code: 'SOL10' }
                ].map((offer) => (
                  <button
                    key={offer.code}
                    type="button"
                    onClick={() => handleApplyOffer(offer.code)}
                    className="pdp-offer-card p-2 sm:p-3 rounded-xl bg-[#FAF5F0] border border-[#CEBDA7] text-left hover:border-[#61532E] hover:bg-[#FDFBF7] transition-all cursor-pointer group shrink-0 sm:shrink active:scale-98 shadow-2xs flex flex-col justify-between snap-start"
                    style={{ flex: '0 0 calc((100% - 16px) / 2.45)', minWidth: 0 }}
                  >
                    <div>
                      <div className="flex items-center justify-between gap-1">
                        <p className="text-[11.5px] sm:text-xs font-bold text-stone-900 leading-tight">{offer.discount}</p>
                        <span className="text-[8px] sm:text-[9px] font-bold text-[#61532E] bg-[#61532E]/10 px-1 py-0.5 rounded shrink-0">{offer.badge}</span>
                      </div>
                      <p className="text-[9px] sm:text-[10.5px] text-stone-600 mt-1 leading-tight">{offer.min}</p>
                    </div>
                    <div className="mt-2 text-[9.5px] sm:text-[10.5px] font-mono tracking-tight flex items-center justify-between border-t border-[#CEBDA7]/40 pt-1.5">
                      <span className="text-stone-700 text-[9px] sm:text-[10px]">use <strong className="text-[#61532E] font-bold">{offer.code}</strong></span>
                      <span className="text-[8.5px] sm:text-[9px] uppercase font-sans font-bold text-stone-500 group-hover:text-[#61532E]">Apply</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>"""

text_crlf = text.replace('\r\n', '\n')
target_norm = target.replace('\r\n', '\n')
repl_norm = replacement.replace('\r\n', '\n')

if target_norm in text_crlf:
    text_crlf = text_crlf.replace(target_norm, repl_norm)
    with open(react_path, 'w', encoding='utf-8') as f:
        f.write(text_crlf)
    print("Updated React file successfully!")
else:
    print("Target not found in React file!")

