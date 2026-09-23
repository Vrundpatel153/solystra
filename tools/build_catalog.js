import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, '..');

// 1. Ensure any HEIC masquerading as JPEGs are available as .jpg for full browser compatibility
const productsDir = path.join(rootDir, 'solystra_assets/products');
if (fs.existsSync(productsDir)) {
  for (const d of fs.readdirSync(productsDir)) {
    const dir = path.join(productsDir, d);
    if (!fs.statSync(dir).isDirectory()) continue;
    for (const f of fs.readdirSync(dir)) {
      if (f.toLowerCase().endsWith('.heic')) {
        const src = path.join(dir, f);
        const dst = path.join(dir, f.replace(/\.heic$/i, '.jpg'));
        if (!fs.existsSync(dst)) {
          fs.copyFileSync(src, dst);
        }
      }
    }
  }
}

// 2. Category metadata definition
const categoryMeta = {
  'necklaces': {
    name: 'Necklaces & Lariats',
    tagline: 'Timeless cascading pendants, solitaires & bridal lariats in 925 silver',
    bannerImg: 'solystra_assets/categories/cat_necklaces.png'
  },
  'bracelets': {
    name: 'Tennis & Charm Bracelets',
    tagline: 'Gleaming wristwear adorned with Austrian crystals & fine enamel charms',
    bannerImg: 'solystra_assets/categories/cat_bracelets.png'
  },
  'earrings': {
    name: 'Fine Earrings & Studs',
    tagline: 'From minimalist solitaires to statement floral drop earrings',
    bannerImg: 'solystra_assets/categories/cat_earrings.png'
  },
  'rings': {
    name: 'Crowned Solitaires & Bands',
    tagline: 'Precision micro-pave eternity bands & certified solitaire showstoppers',
    bannerImg: 'solystra_assets/categories/cat_rings.png'
  },
  'complete_sets': {
    name: 'Gift Suites & Sets',
    tagline: 'Complete matching necklace, earring & bracelet sets in luxury boxes',
    bannerImg: 'solystra_assets/categories/cat_complete_sets.png'
  },
  'chains': {
    name: 'Classic Layering Chains',
    tagline: 'Italian curb, rope & box link chains in pure 925 silver and 18K vermeil',
    bannerImg: 'solystra_assets/categories/zavya_style/chains.png'
  },
  'anklets': {
    name: 'Sterling Anklets & Sets',
    tagline: 'Dainty anklet chains with anti-tarnish micro-shield finish',
    bannerImg: 'solystra_assets/categories/cat_anklets.png'
  }
};

// Known price overrides & editorial metadata
const knownOverrides = {
  // Editorial Styling Combo Pieces
  'golden-meadow-necklace-set-925-sterling-silver': {
    name: 'Golden Meadow Tennis Choker & Earrings Set in 18K Gold',
    shortName: 'Golden Meadow 18K Gold Set',
    price: 5499,
    mrp: 7999,
    badge: 'Atelier Gala',
    category: 'necklaces',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'amethyst-bloom-necklace-set-925-sterling-silver': {
    name: 'Amethyst Bloom Rose Gold Floral Necklace Set',
    shortName: 'Amethyst Bloom Rose Gold Set',
    price: 9585,
    mrp: 11981,
    badge: 'Atelier Gala',
    category: 'necklaces',
    metals: ['Rose Gold Plated', 'Pure 925 Silver', '18K Yellow Gold']
  },
  'greek-pattern-hoops': {
    name: 'Greek Geometric Pattern 18K Gold Imperial Hoops',
    shortName: 'Greek Pattern 18K Gold Hoops',
    price: 3499,
    mrp: 4999,
    badge: 'Bestseller',
    category: 'earrings',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'classic-knot-earrings': {
    name: 'Classic Artisan Solitaire Knot Earrings',
    shortName: 'Classic Knot Earrings',
    price: 2299,
    mrp: 3299,
    badge: 'Trending',
    category: 'earrings',
    metals: ['Pure 925 Silver', 'Rose Gold Plated']
  },
  'clover-charm-bracelet': {
    name: 'Imperial Clover Charm 18K Gold Vermeil Bracelet',
    shortName: 'Clover Charm 18K Gold Bracelet',
    price: 3899,
    mrp: 5299,
    badge: 'Bestseller',
    category: 'bracelets',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'clover-lock-charm-925-sterling-silver-bracelet': {
    name: 'Clover Padlock Charm 18K Gold Bracelet',
    shortName: 'Clover Lock 18K Gold Bracelet',
    price: 3699,
    mrp: 4999,
    badge: 'Trending',
    category: 'bracelets',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'classic-ridge-band': {
    name: 'Classic Fluted 18K Gold Vermeil Ridge Band',
    shortName: 'Classic Ridge 18K Gold Band',
    price: 2699,
    mrp: 3799,
    badge: 'Bestseller',
    category: 'rings',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'flora-band-hoops': {
    name: 'Blossom Petal Rose Gold Flora Band Hoops',
    shortName: 'Flora Band Rose Gold Hoops',
    price: 2499,
    mrp: 3499,
    badge: 'Bestseller',
    category: 'earrings',
    metals: ['Rose Gold Plated', 'Pure 925 Silver']
  },
  'blush-spark-tennis-bracelet-925-sterling-silver': {
    name: 'Blush Spark Rose Gold Tennis Bracelet',
    shortName: 'Blush Spark Rose Gold Bracelet',
    price: 3699,
    mrp: 4999,
    badge: 'Newly Launched',
    category: 'bracelets',
    metals: ['Rose Gold Plated', 'Pure 925 Silver']
  },
  'rose-round-spark-tennis-bracelet-925-sterling-silver': {
    name: 'Rose Round Spark Tennis Bracelet in 18K Rose Gold',
    shortName: 'Rose Round Spark Tennis Bracelet',
    price: 3899,
    mrp: 5299,
    badge: 'Trending',
    category: 'bracelets',
    metals: ['Rose Gold Plated', 'Pure 925 Silver']
  },
  'azure-daisy-tennis-bracelet-925-sterling-silver': {
    name: 'Azure Daisy Austrian Tennis Bracelet',
    shortName: 'Azure Daisy Tennis Bracelet',
    price: 3899,
    mrp: 5299,
    badge: 'Bestseller',
    category: 'bracelets',
    metals: ['Pure 925 Silver', 'Rose Gold Plated']
  },
  'unity-circle': {
    name: 'Universal Solitaire Unity Circle Drop Necklace',
    shortName: 'Unity Circle Solitaire Necklace',
    price: 2799,
    mrp: 3999,
    badge: 'Bestseller',
    category: 'necklaces',
    metals: ['Pure 925 Silver', 'Rose Gold Plated']
  }
};

function formatTitle(id, rawTitle) {
  if (rawTitle && rawTitle.trim()) {
    let clean = rawTitle
      .replace(/\s*\?\s*/g, ' - ')
      .replace(/[\uFFFD\u200B\u200E\u200F]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    return clean;
  }
  let clean = id
    .replace(/-925-sterling-silver/gi, '')
    .replace(/-925-silver/gi, '')
    .replace(/-sterling-silver/gi, '');
  return clean
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

// Load official Shopify dump if available
let shopifyData = null;
const dumpPath = path.join(rootDir, 'src/data/solystra_shopify_dump.json');
if (fs.existsSync(dumpPath)) {
  try {
    shopifyData = JSON.parse(fs.readFileSync(dumpPath, 'utf8'));
    console.log(`Loaded ${shopifyData.products?.length || 0} products from solystra_shopify_dump.json`);
  } catch (err) {
    console.warn('Could not parse solystra_shopify_dump.json:', err);
  }
}

const colMap = shopifyData?.collections_map || {};
const goldHandles = new Set(colMap['gold'] || []);
const silverHandles = new Set(colMap['silver'] || []);
const blushHandles = new Set(colMap['blush-tones'] || []);

function determineCategory(id, rawTitle = '', productType = '') {
  const handle = id.toLowerCase();
  const title = rawTitle.toLowerCase();
  const pt = productType.toLowerCase();

  // 1. Shopify collection matches
  if (colMap['silver-anklets']?.includes(id)) return 'anklets';
  if (colMap['complete-sets']?.includes(id) || colMap['pendant-sets']?.includes(id)) return 'complete_sets';
  if (colMap['rings']?.includes(id)) return 'rings';
  if (colMap['earrings']?.includes(id)) return 'earrings';
  if (colMap['bracelets']?.includes(id)) return 'bracelets';
  if (colMap['chains']?.includes(id)) return 'chains';
  if (colMap['necklaces']?.includes(id)) return 'necklaces';

  // 2. Text heuristics
  if (title.includes('anklet') || handle.includes('anklet') || title.includes('payal')) return 'anklets';
  if (title.includes('mangalsutra') || handle.includes('mangalsutra')) return 'necklaces';
  if (title.includes('nose pin') || title.includes('nosepin')) return 'earrings';
  if ((title.includes('set') || handle.includes('set') || title.includes('suite')) &&
      (title.includes('necklace') || title.includes('pendant') || title.includes('earring') || title.includes('bloom') || title.includes('meadow') || title.includes('wreath'))) {
    return 'complete_sets';
  }
  if (title.includes('ring') || title.includes('band') || handle.includes('ring') || handle.includes('band') || pt === 'rings') return 'rings';
  if (title.includes('earring') || title.includes('stud') || title.includes('hoop') || title.includes('huggie') || handle.includes('earring') || handle.includes('hoop')) return 'earrings';
  if (title.includes('bracelet') || title.includes('bangle') || title.includes('kada') || title.includes('cuff') || handle.includes('bracelet') || handle.includes('bangle')) return 'bracelets';
  if (title.includes('chain') || handle.includes('chain')) return 'chains';
  if (title.includes('necklace') || title.includes('pendant') || title.includes('lariat') || title.includes('choker') || handle.includes('necklace') || handle.includes('pendant')) return 'necklaces';
  return 'bracelets';
}

function determineMetals(id, p = {}) {
  const metals = [];
  const handle = id.toLowerCase();
  const title = (p.title || id).toLowerCase();
  
  if (goldHandles.has(id)) metals.push('18K Yellow Gold');
  if (silverHandles.has(id)) metals.push('Pure 925 Silver');
  if (blushHandles.has(id)) metals.push('Rose Gold Plated');

  if (p.options) {
    for (const opt of p.options) {
      for (const val of opt.values || []) {
        const v = String(val).toLowerCase();
        if (v.includes('rose')) metals.push('Rose Gold Plated');
        else if (v.includes('gold') || v.includes('18k')) metals.push('18K Yellow Gold');
        else if (v.includes('silver') || v.includes('925')) metals.push('Pure 925 Silver');
      }
    }
  }

  if (p.variants) {
    for (const v of p.variants) {
      const vt = (v.title || '').toLowerCase();
      if (vt.includes('rose')) metals.push('Rose Gold Plated');
      else if (vt.includes('gold')) metals.push('18K Yellow Gold');
      else if (vt.includes('silver')) metals.push('Pure 925 Silver');
    }
  }

  if (title.includes('rose')) metals.push('Rose Gold Plated');
  else if (title.includes('gold') || title.includes('vermeil')) metals.push('18K Yellow Gold');
  else if (title.includes('silver') || title.includes('925')) metals.push('Pure 925 Silver');

  if (metals.length === 0) {
    metals.push('Pure 925 Silver', 'Rose Gold Plated', '18K Yellow Gold');
  }

  const unique = [];
  for (const m of metals) {
    if (!unique.includes(m)) unique.push(m);
  }
  return unique;
}

const products = [];
const categoryCounts = {};

// Build a map of shopify products by handle
const shopifyMap = {};
if (shopifyData && shopifyData.products) {
  for (const sp of shopifyData.products) {
    shopifyMap[sp.handle] = sp;
  }
}

// Read all product directories from solystra_assets/products
const dirs = fs.readdirSync(productsDir)
  .filter(d => fs.statSync(path.join(productsDir, d)).isDirectory())
  .sort();

dirs.forEach((id, index) => {
  const dir = path.join(productsDir, id);
  const sp = shopifyMap[id] || {};
  const override = knownOverrides[id] || {};
  const rawTitle = sp.title || id;
  const catKey = override.category || determineCategory(id, rawTitle, sp.product_type || '');
  categoryCounts[catKey] = (categoryCounts[catKey] || 0) + 1;

  // Collect all valid images
  let images = [];
  const files = fs.readdirSync(dir)
    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
    .sort((a, b) => {
      const getScore = (name) => {
        if (name.includes('angle_1')) return 1;
        if (name.includes('angle_2')) return 2;
        if (name.includes('angle_3')) return 3;
        if (name.includes('angle_4')) return 4;
        return 10;
      };
      return getScore(a) - getScore(b);
    })
    .map(f => `solystra_assets/products/${id}/${f}`);

  images.push(...files);

  if (images.length === 1) {
    images.push('assets/craftsmanship-atelier.jpg');
    images.push('assets/bento-craftsmanship-macro.jpg');
  } else if (images.length === 0) {
    images.push('assets/craftsmanship-atelier.jpg');
  }

  // Pricing from Shopify variants or overrides
  const variant0 = sp.variants?.[0] || {};
  const shopifyPrice = variant0.price ? Math.round(parseFloat(variant0.price)) : null;
  const shopifyMrp = variant0.compare_at_price ? Math.round(parseFloat(variant0.compare_at_price)) : null;

  const price = override.price || shopifyPrice || 2999;
  const mrp = override.mrp || shopifyMrp || Math.round(price * 1.38);
  const discountPercent = Math.max(5, Math.round(((mrp - price) / mrp) * 100));

  const formattedName = formatTitle(id, rawTitle);
  const shortName = override.shortName || (formattedName.length > 38 ? formattedName.split(' - ')[0].substring(0, 35) + '...' : formattedName);
  const name = override.name || formattedName;

  const badges = ['Bestseller', 'Newly Launched', 'Trending', 'Atelier Pick', 'Popular Choice'];
  const badge = override.badge || (price > 12000 ? 'Atelier Gala' : badges[index % badges.length]);

  const metals = override.metals || determineMetals(id, sp);

  // Clean description
  let cleanDesc = `Exquisitely handcrafted by master artisans at Solystra Atelier. Cast in solid, hypoallergenic 925 sterling silver with high-precision micro-prong setting and finished with protective anti-tarnish rhodium coating to maintain enduring showroom brilliance.`;
  if (sp.body_html) {
    const stripped = sp.body_html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    if (stripped.length > 30) {
      cleanDesc = stripped;
    }
  }

  const primaryMetal = metals[0] || 'Pure 925 Silver';
  const isGold = primaryMetal.includes('Gold') && !primaryMetal.includes('Rose');
  const isRose = primaryMetal.includes('Rose');

  products.push({
    id,
    name,
    shortName,
    sku: `SOL-${id.replace(/[^a-zA-Z0-9]/g, '').substring(0, 8).toUpperCase()}`,
    category: catKey,
    categoryName: categoryMeta[catKey]?.name || 'Fine Jewelry',
    price,
    mrp,
    discount: `${discountPercent}% OFF`,
    rating: Number((4.7 + ((index % 4) * 0.08)).toFixed(1)),
    reviewsCount: 18 + ((index * 7) % 75),
    badge,
    isNew: badge === 'Newly Launched',
    metals,
    desc: cleanDesc,
    images,
    specs: {
      "Metal Purity": override.specs?.["Metal Purity"] || (isGold ? "18K Gold Vermeil (BIS Certified)" : isRose ? "18K Rose Gold Micron (BIS Certified)" : "BIS Certified 925 Sterling Silver"),
      "Plating Finish": override.specs?.["Plating Finish"] || (isGold ? "2.5-Micron 18K Gold Vermeil & Protective E-Coat" : isRose ? "18K Rose Gold Micron Vermeil & Protective E-Coat" : "Anti-Tarnish Rhodium & Micron E-Coat"),
      "Stone Setting": override.specs?.["Stone Setting"] || "AAA+ Austrian Solitaire Crystals",
      "Hallmark Verification": override.specs?.["Hallmark Verification"] || (isGold ? "Certified 18K / 925 Stamp on Clasp" : "Certified 925 Stamp on Clasp/Band"),
      "Warranty Coverage": "6 Months Free Replating Assurance",
      "Packaging": "Luxury Suede Box with Authenticity Card",
      "Shipping": "Free Insured Express Delivery Across India",
      ...(override.specs || {})
    },
    inStock: true
  });
});

// Add universal-embrace alias as explicitly referenced in styling combos
if (!products.some(p => p.id === 'universal-embrace')) {
  const unity = products.find(p => p.id === 'unity-circle') || products[0];
  products.push({
    ...unity,
    id: 'universal-embrace',
    name: 'Universal Solitaire Drop Necklace',
    shortName: 'Universal Solitaire Necklace',
    sku: 'AUR-UNIV-EMBRACE',
    category: 'necklaces',
    categoryName: 'Necklaces & Lariats',
    price: 2799,
    mrp: 3999,
    discount: '30% OFF',
    badge: 'Bestseller'
  });
}

// Add crowned-solitaire-ring alias as explicitly referenced in customer reviews
if (!products.some(p => p.id === 'crowned-solitaire-ring')) {
  const halo = products.find(p => p.id === 'prism-halo-ring') || products[0];
  products.push({
    ...halo,
    id: 'crowned-solitaire-ring',
    name: 'Crowned Solitaire Band Ring',
    shortName: 'Crowned Solitaire Ring',
    sku: 'AUR-CROWN-SOL',
    category: 'rings',
    categoryName: 'Crowned Solitaires & Bands',
    price: 2999,
    mrp: 4299,
    discount: '30% OFF',
    badge: 'Bestseller'
  });
}

const categories = Object.keys(categoryMeta).map(key => ({
  id: key,
  name: categoryMeta[key].name,
  tagline: categoryMeta[key].tagline,
  image: categoryMeta[key].bannerImg,
  count: categoryCounts[key] || 0
}));

const customerReviews = [
  {
    id: 1,
    author: "Ananya Deshmukh",
    city: "Mumbai, Maharashtra",
    rating: 5,
    date: "2 days ago",
    verified: true,
    title: "Mesmerizing luster & pure luxury feel",
    comment: "I was blown away by the packaging first - the emerald suede box felt like high jewelry. The silver hallmark is clearly engraved, and the Austrian crystals reflect light like real diamonds. Wore it to an evening gala and received endless compliments!",
    productName: "Amethyst Bloom Necklace Set"
  },
  {
    id: 2,
    author: "Rohan & Priyadarshini Mehta",
    city: "Bengaluru, Karnataka",
    rating: 5,
    date: "1 week ago",
    verified: true,
    title: "The ring sizing was flawless",
    comment: "Ordered the Crowned Solitaire Ring in Rose Gold finish. The anti-tarnish coating is legit - my wife has been wearing it daily for two weeks, through hand washes, and not a single hint of oxidation. Top notch craftsmanship.",
    productName: "Crowned Solitaire Ring"
  },
  {
    id: 3,
    author: "Sunita Kulkarni",
    city: "Delhi NCR",
    rating: 5,
    date: "3 weeks ago",
    verified: true,
    title: "Authentic 925 silver with certificate",
    comment: "Finding genuine 925 silver with proper government BIS hallmark online is rare. The certificate card and the velvet pouch give complete peace of mind. Truly a Cartier-level experience at affordable pricing.",
    productName: "Azure Daisy Tennis Bracelet"
  }
];

const trustPillars = [
  {
    id: 'hallmark',
    title: 'BIS Certified 925 Silver',
    description: 'Every piece carries the official government 925 hallmark stamp of purity.',
    icon: 'ShieldCheck',
    badgeImg: 'solystra_assets/features/feat_hallmark.png'
  },
  {
    id: 'warranty',
    title: '6-Month Replating Warranty',
    description: 'Complimentary replating assurance to keep your jewels gleaming forever.',
    icon: 'Sparkles',
    badgeImg: 'solystra_assets/features/feat_warranty.png'
  },
  {
    id: 'shipping',
    title: 'Insured Express Delivery',
    description: 'Tamper-evident transit protection and express door delivery across India.',
    icon: 'Truck',
    badgeImg: 'solystra_assets/features/feat_shipping.png'
  },
  {
    id: 'returns',
    title: '15-Day Easy Exchange',
    description: 'Zero questions asked exchange guarantee for ultimate peace of mind.',
    icon: 'RotateCcw',
    badgeImg: 'solystra_assets/features/feat_returns.png'
  }
];

const promoCodes = {
  'AUR10': { discountPercent: 10, label: 'VIP Welcome 10% Off' },
  'GOLD500': { discountAmount: 500, label: 'Festive Atelier ₹500 Flat Off' },
  'SOULYSTRA': { discountPercent: 15, label: 'Collector Exclusive 15% Off' },
  'SILVER10': { discountPercent: 10, label: 'Silver Privileges 10% Off' },
  'SILVER15': { discountPercent: 15, label: 'Silver Tier 15% Off' },
  'SILVER20': { discountPercent: 20, label: 'Atelier Vault 20% Off' },
  'SOLYSTRA25': { discountPercent: 25, label: 'Signature VIP 25% Off' },
  'BOGOFREE': { discountPercent: 30, label: 'Buy 1 Get 1 Privilege' },
  'ROYAL15': { discountPercent: 15, label: 'Royal Festive 15% Off' },
  'B2G1': { discountPercent: 33, label: 'Buy 2 Get 1 Free Stack' }
};

const outputDir = path.join(rootDir, 'src/data');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const fileContent = `// Auto-generated Master Catalog for Solystra Jewels Luxury App
export const PRODUCTS = ${JSON.stringify(products, null, 2)};

export const CATEGORIES = ${JSON.stringify(categories, null, 2)};

export const CUSTOMER_REVIEWS = ${JSON.stringify(customerReviews, null, 2)};

export const TRUST_PILLARS = ${JSON.stringify(trustPillars, null, 2)};

export const PROMO_CODES = ${JSON.stringify(promoCodes, null, 2)};
`;

fs.writeFileSync(path.join(outputDir, 'catalog.js'), fileContent, 'utf8');
console.log('Successfully generated src/data/catalog.js with', products.length, 'products and', categories.length, 'categories.');
