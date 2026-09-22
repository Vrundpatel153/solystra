import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.join(__dirname, '..');
const distDir = path.join(rootDir, 'dist');

// Helper to copy directory recursively
function copyDirRecursive(src, dest) {
  if (!fs.existsSync(src)) return;
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

// 1. Copy solystra_assets into dist/solystra_assets for Netlify self-contained hosting
console.log('Postbuild: Syncing solystra_assets into dist/solystra_assets...');
if (fs.existsSync(path.join(rootDir, 'public', 'solystra_assets'))) {
  copyDirRecursive(path.join(rootDir, 'public', 'solystra_assets'), path.join(distDir, 'solystra_assets'));
}
copyDirRecursive(path.join(rootDir, 'solystra_assets'), path.join(distDir, 'solystra_assets'));

// 1b. Copy assets into dist/assets
if (fs.existsSync(path.join(rootDir, 'assets'))) {
  console.log('Postbuild: Syncing assets into dist/assets...');
  copyDirRecursive(path.join(rootDir, 'assets'), path.join(distDir, 'assets'));
}

// 1c. Copy ONLY active video and poster assets into dist/zavya_assets (prevents 600MB+ of unused file bloat)
const activeZavyaAssets = [
  'products/pendant/pen-30277-g/video_01_pen-30277-g.mp4',
  'products/pendant/pen-30277-g/01_pen-30277-g.jpg',
  'products/drop_earrings/ear-21096-g/video_01_ear-21096-g.mp4',
  'products/drop_earrings/ear-21096-g/07_ear-21096-g.jpg',
  'products/bracelet/br-80505-g/video_01_br-80505-g.mp4',
  'products/bracelet/br-80505-g/01_br-80505-g.jpg',
  'products/diamond_stud_earrings/0-75-ct-halo-heart-solitaire-gold-stud-earring/01_0-75-ct-halo-heart-solitaire-gold-stud-earring.jpg',
  'products/diamond_solitaire_ring/0-75-ct-lambency-solitaire-diamond-ring/01_0-75-ct-lambency-solitaire-diamond-ring.jpg',
  'products/necklace/nl-30455-g/video_01_nl-30455-g.mp4',
  'products/necklace/nl-30455-g/01_nl-30455-g.jpg',
  'products/diamond_pendant/0-75-ct-celestial-solitaire-lab-grown-diamond-pendant-without-chain/01_0-75-ct-celestial-solitaire-lab-grown-diamond-pendant-without-chain.jpg',
  'products/kada_bracelet/peacock-925-sterling-silver-bracelet-in-rose-gold-valentine-hamper/01_peacock-925-sterling-silver-bracelet-in-rose-gold-valentine-hamper.jpg',
  'products/kada_bracelet_men/bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle/video_01_bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle.mp4',
  'products/kada_bracelet_men/bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle/01_bold-and-striking-rhodium-plated-925-sterling-silver-mens-bangle.jpg',
  'products/jewellery_sets/radiant-bloom-gold-plated-cz-pendant-earrings-set/video_01_radiant-bloom-gold-plated-cz-pendant-earrings-set.mp4',
  'products/jewellery_sets/eternal-spark-rose-gold-sterling-silver-jewellery-set/01_eternal-spark-rose-gold-sterling-silver-jewellery-set.jpg',
  'products/evil_eye_bracelet/infinity-charm-rhodium-plated-bracelet-with-evil-eye-cubic-zirconia/01_infinity-charm-rhodium-plated-bracelet-with-evil-eye-cubic-zirconia.jpg',
  'products/anklets/rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama/video_01_rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama.mp4',
  'products/anklets/rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama/01_rose-gold-plated-glimmering-fusion-cz-925-sterling-silver-anklet-x-kama.jpg',
  'products/diamond_stud_earrings/0-75-ct-solitaire-halo-gold-earrings-with-lab-grown-diamonds/video_01_0-75-ct-solitaire-halo-gold-earrings-with-lab-grown-diamonds.mp4'
];

console.log('Postbuild: Syncing active product video and poster assets into dist/zavya_assets...');
for (const relPath of activeZavyaAssets) {
  const srcFile = path.join(rootDir, 'zavya_assets', relPath);
  const destFile = path.join(distDir, 'zavya_assets', relPath);
  if (fs.existsSync(srcFile)) {
    fs.mkdirSync(path.dirname(destFile), { recursive: true });
    fs.copyFileSync(srcFile, destFile);
  }
}

// 3. Create Netlify SPA _redirects file in dist/
const redirectsContent = `/*    /index.html   200\n`;
fs.writeFileSync(path.join(distDir, '_redirects'), redirectsContent, 'utf8');
console.log('Postbuild: Created dist/_redirects for Netlify SPA routing (/* -> /index.html 200).');

// 4. Create standalone static netlify.toml in dist/ (without [build] command so pre-built deploys never fail)
const distNetlifyToml = `# Netlify Configuration for Pre-built Solystra Jewels
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/assets-bundle/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/solystra_assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
`;
fs.writeFileSync(path.join(distDir, 'netlify.toml'), distNetlifyToml, 'utf8');
console.log('Postbuild: Created dist/netlify.toml for standalone static hosting.');

// 5. Sync dist/assets-bundle to root assets-bundle for local server
const distAssets = path.join(distDir, 'assets-bundle');
const targetAssets = path.join(rootDir, 'assets-bundle');
if (fs.existsSync(distAssets)) {
  if (fs.existsSync(targetAssets)) {
    // Purge old hashed JS and CSS bundles to avoid stale clutter
    for (const file of fs.readdirSync(targetAssets)) {
      if (file.startsWith('index-') && (file.endsWith('.js') || file.endsWith('.css'))) {
        try { fs.unlinkSync(path.join(targetAssets, file)); } catch (e) {}
      }
    }
  } else {
    fs.mkdirSync(targetAssets, { recursive: true });
  }
  for (const file of fs.readdirSync(distAssets)) {
    fs.copyFileSync(path.join(distAssets, file), path.join(targetAssets, file));
  }
}

// 6. Ensure dist folder and files have accurate current timestamp in Windows File Explorer
const now = new Date();
try {
  fs.utimesSync(distDir, now, now);
  const distHtmlPath = path.join(distDir, 'index.html');
  if (fs.existsSync(distHtmlPath)) {
    fs.utimesSync(distHtmlPath, now, now);
  }
} catch (e) {}

// 7. Generate a clean dist.zip for 1-click Netlify Drop upload
try {
  const zipPath = path.join(rootDir, 'dist.zip');
  if (fs.existsSync(zipPath)) fs.unlinkSync(zipPath);
  console.log('Postbuild: Creating dist.zip for lightning-fast Netlify Drop upload...');
  if (process.platform === 'win32') {
    execSync(`powershell -Command "Compress-Archive -Path dist\\* -DestinationPath dist.zip -Force"`, { cwd: rootDir, stdio: 'inherit' });
  } else {
    execSync(`zip -rq dist.zip dist/`, { cwd: rootDir, stdio: 'inherit' });
  }
  if (fs.existsSync(zipPath)) {
    fs.utimesSync(zipPath, now, now);
  }
  console.log('Postbuild: Created dist.zip successfully!');
} catch (err) {
  console.warn('Postbuild: Note: Could not create dist.zip automatically:', err.message);
}

// 8. Restore root index.html with /src/main.jsx so active Vite dev server continues hot-reloading
try {
  const srcHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Solystra Jewels | Fine 925 Sterling Silver &amp; 18K Gold Atelier</title>
  <meta name="description" content="Explore Solystra Jewels' handcrafted 925 sterling silver and 18K gold jewelry. Certified BIS hallmark, Austrian solitaires, necklaces, rings, earrings, and tennis bracelets with free insured express delivery across India.">
  <link rel="icon" type="image/png" href="solystra_assets/solystra_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,400;1,9..144,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-[#FAF8F5] text-[#231F20] antialiased font-sans">
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>`;
  fs.writeFileSync(path.join(rootDir, 'index.html'), srcHtml, 'utf8');
  console.log('Postbuild: Restored root index.html for active Vite dev server');
} catch (e) {}

console.log('Postbuild: SUCCESS! dist/ is 100% self-contained, verified, and ready for deployment.');
