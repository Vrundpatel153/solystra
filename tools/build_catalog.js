import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read existing catalog.js
const code = fs.readFileSync(path.join(__dirname, '../catalog.js'), 'utf8');
const catObj = {};
const evalFn = new Function('global', code.replace('const SOULYSTRA_CATALOG =', 'global.cat =') + '; return global.cat;');
const rawCatalog = evalFn(catObj);

const products = [];

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

const categoryCounts = {};

for (const [id, item] of Object.entries(rawCatalog)) {
  const dir = path.join(__dirname, '../solystra_assets/products', id);
  let images = [...item.images];

  if (fs.existsSync(dir)) {
    const validFiles = fs.readdirSync(dir)
      .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
      .map(f => `solystra_assets/products/${id}/${f}`);
    
    for (const f of validFiles) {
      if (!images.includes(f)) {
        images.push(f);
      }
    }
  }

  // Ensure at least 2 images for rich gallery experience
  if (images.length === 1) {
    images.push('assets/craftsmanship-atelier.jpg');
    images.push('assets/bento-craftsmanship-macro.jpg');
  }

  const catKey = item.category || 'necklaces';
  categoryCounts[catKey] = (categoryCounts[catKey] || 0) + 1;

  products.push({
    id: item.id,
    name: item.name,
    shortName: item.shortName || item.name,
    sku: item.sku || `AUR-${item.id.substring(0, 8).toUpperCase()}`,
    category: catKey,
    categoryName: categoryMeta[catKey]?.name || item.categoryName,
    price: item.price,
    mrp: item.mrp || Math.round(item.price * 1.25),
    discount: item.discount || '20% OFF',
    rating: item.rating || 4.9,
    reviewsCount: item.reviewsCount || Math.floor(Math.random() * 40 + 25),
    badge: item.badge || (item.price > 8000 ? 'Atelier Gala' : 'Bestseller'),
    metals: item.metals && item.metals.length ? item.metals : [
      'Pure 925 Silver',
      'Rose Gold Plated',
      '18K Yellow Gold'
    ],
    desc: item.desc,
    images: images,
    specs: item.specs || {
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

const outputDir = path.join(__dirname, '../src/data');
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const fileContent = `// Auto-generated Master Catalog for Aurélia & Co. / Soulystra Jewels Luxury App
export const PRODUCTS = ${JSON.stringify(products, null, 2)};

export const CATEGORIES = ${JSON.stringify(categories, null, 2)};

export const CUSTOMER_REVIEWS = ${JSON.stringify(customerReviews, null, 2)};

export const TRUST_PILLARS = [
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

export const PROMO_CODES = {
  'AUR10': { discountPercent: 10, label: 'VIP Welcome 10% Off' },
  'GOLD500': { discountAmount: 500, label: 'Festive Atelier ₹500 Flat Off' },
  'SOULYSTRA': { discountPercent: 15, label: 'Collector Exclusive 15% Off' }
};
`;

fs.writeFileSync(path.join(outputDir, 'catalog.js'), fileContent, 'utf8');
console.log('Successfully generated src/data/catalog.js with', products.length, 'products and', categories.length, 'categories.');
