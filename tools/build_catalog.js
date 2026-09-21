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
  'anklets': {
    name: 'Sterling Anklets & Sets',
    tagline: 'Dainty anklet chains with anti-tarnish micro-shield finish',
    bannerImg: 'solystra_assets/categories/cat_anklets.png'
  }
};

// Known price overrides & editorial metadata
const knownOverrides = {
  'amethyst-bloom-necklace-set-925-sterling-silver': {
    name: 'Amethyst Bloom Floral Necklace Set',
    shortName: 'Amethyst Bloom Necklace Set',
    price: 9585,
    mrp: 11981,
    badge: 'Atelier Gala',
    category: 'necklaces',
    metals: ['Rose Gold Plated', 'Pure 925 Silver', '18K Yellow Gold']
  },
  'flora-band-hoops': {
    name: 'Blossom Petal Flora Band Hoops',
    shortName: 'Flora Band Hoops',
    price: 2499,
    mrp: 3499,
    badge: 'Bestseller',
    category: 'earrings',
    metals: ['Rose Gold Plated', 'Pure 925 Silver']
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
  'golden-meadow-necklace-set-925-sterling-silver': {
    name: 'Golden Meadow Tennis Choker & Earrings Set',
    shortName: 'Golden Meadow Necklace Set',
    price: 5499,
    mrp: 7999,
    badge: 'Atelier Gala',
    category: 'necklaces',
    metals: ['18K Yellow Gold', 'Pure 925 Silver']
  },
  'greek-pattern-hoops': {
    name: 'Greek Geometric Pattern Imperial Hoops',
    shortName: 'Greek Pattern Hoops',
    price: 3499,
    mrp: 4999,
    badge: 'Bestseller',
    category: 'earrings',
    metals: ['Pure 925 Silver', '18K Yellow Gold']
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
  'blush-spark-tennis-bracelet-925-sterling-silver': {
    name: 'Blush Spark Tennis Bracelet 925 Silver',
    shortName: 'Blush Spark Tennis Bracelet',
    price: 3699,
    mrp: 4999,
    badge: 'Newly Launched',
    category: 'bracelets',
    metals: ['Rose Gold Plated', 'Pure 925 Silver']
  },
  'celeste-glow-925-sterling-silver-necklace': {
    name: 'Celeste Glow Solitaire Drop Necklace',
    shortName: 'Celeste Glow Necklace',
    price: 2799,
    mrp: 3999,
    badge: 'Bestseller',
    category: 'necklaces',
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

function formatTitle(id) {
  let clean = id
    .replace(/-925-sterling-silver/gi, '')
    .replace(/-925-silver/gi, '')
    .replace(/-sterling-silver/gi, '');
  return clean
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

function determineCategory(id) {
  if (id.includes('anklet')) return 'anklets';
  if (id.includes('set') && (id.includes('necklace') || id.includes('pendant') || id.includes('bloom') || id.includes('meadow') || id.includes('wreath') || id.includes('leaf') || id.includes('swan') || id.includes('halo-pendant') || id.includes('ceramic-pendant'))) return 'necklaces';
  if (id.includes('necklace') || id.includes('pendant') || id.includes('lariat') || id.includes('chain') || id.includes('bot') || id.includes('unity') || id.includes('love') || id.includes('glow') || id.includes('key-to-my-heart')) return 'necklaces';
  if (id.includes('bracelet') || id.includes('bangle') || id.includes('buckle')) return 'bracelets';
  if (id.includes('earring') || id.includes('stud') || id.includes('hoop')) return 'earrings';
  if (id.includes('ring') || id.includes('band')) return 'rings';
  return 'necklaces';
}

function getBasePrice(category, id, index) {
  if (id.includes('set')) return 4999 + ((index * 370) % 4000);
  if (category === 'rings') return 1999 + ((index * 230) % 1800);
  if (category === 'earrings') return 1899 + ((index * 210) % 1600);
  if (category === 'bracelets') return 2799 + ((index * 310) % 2400);
  if (category === 'anklets') return 1999 + ((index * 170) % 1000);
  return 2499 + ((index * 290) % 2200);
}

const products = [];
const categoryCounts = {};

const dirs = fs.readdirSync(productsDir)
  .filter(d => fs.statSync(path.join(productsDir, d)).isDirectory())
  .sort();

dirs.forEach((id, index) => {
  const dir = path.join(productsDir, id);
  const override = knownOverrides[id] || {};
  const catKey = override.category || determineCategory(id);
  categoryCounts[catKey] = (categoryCounts[catKey] || 0) + 1;

  // Collect and prioritize valid images (png, jpg, webp)
  let images = [];
  const files = fs.readdirSync(dir)
    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
    .sort((a, b) => {
      // Sort angle_1, angle_2, angle_3 first
      const getScore = (name) => {
        if (name.includes('angle_1')) return 1;
        if (name.includes('angle_2')) return 2;
        if (name.includes('angle_3')) return 3;
        return 10;
      };
      return getScore(a) - getScore(b);
    })
    .map(f => `solystra_assets/products/${id}/${f}`);

  images.push(...files);

  // Fallback supplementary craftsmanship macro shots if only 1 image
  if (images.length === 1) {
    images.push('assets/craftsmanship-atelier.jpg');
    images.push('assets/bento-craftsmanship-macro.jpg');
  }

  const shortName = override.shortName || formatTitle(id);
  const name = override.name || `${shortName} in Pure 925 Sterling Silver`;
  const price = override.price || getBasePrice(catKey, id, index);
  const mrp = override.mrp || Math.round(price * 1.38);
  const discountPercent = Math.round(((mrp - price) / mrp) * 100);

  const badges = ['Bestseller', 'Newly Launched', 'Trending', 'Atelier Pick', 'Popular Choice'];
  const badge = override.badge || (price > 7500 ? 'Atelier Gala' : badges[index % badges.length]);

  const metals = override.metals || [
    'Pure 925 Silver',
    'Rose Gold Plated',
    '18K Yellow Gold'
  ];

  products.push({
    id,
    name,
    shortName,
    sku: `AUR-${id.replace(/[^a-zA-Z0-9]/g, '').substring(0, 8).toUpperCase()}`,
    category: catKey,
    categoryName: categoryMeta[catKey]?.name || 'Fine Jewelry',
    price,
    mrp,
    discount: `${discountPercent}% OFF`,
    rating: Number((4.7 + ((index % 4) * 0.08)).toFixed(1)),
    reviewsCount: 24 + ((index * 7) % 65),
    badge,
    isNew: badge === 'Newly Launched',
    metals,
    desc: `Exquisitely handcrafted by master artisans at Solystra Atelier. Cast in solid, hypoallergenic 925 sterling silver with high-precision micro-prong setting and finished with protective anti-tarnish rhodium coating to maintain enduring showroom brilliance.`,
    images,
    specs: {
      "Metal Purity": "BIS Certified 925 Sterling Silver",
      "Plating Finish": "Anti-Tarnish Rhodium & Micron E-Coat",
      "Stone Setting": "AAA+ Austrian Solitaire Crystals",
      "Hallmark Verification": "Certified 925 Stamp on Clasp/Band",
      "Warranty Coverage": "6 Months Free Replating Assurance",
      "Packaging": "Luxury Suede Box with Authenticity Card",
      "Shipping": "Free Insured Express Delivery Across India"
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
