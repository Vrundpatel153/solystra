import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.join(__dirname, '..');

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
console.log('Prebuild: Prepared index.html with Soulystra Jewels and /src/main.jsx entry');

// Ensure master catalog is freshly built
try {
  await import('./build_catalog.js');
} catch (err) {
  console.error('Prebuild: Error running build_catalog:', err);
}

