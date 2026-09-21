import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.join(__dirname, '..');

const files = fs.readdirSync(rootDir).filter(f => 
  f.endsWith('.html') && 
  f !== 'index.html' && 
  f !== 'index_legacy.html' && 
  f !== 'solystra_index.html'
);

let patched = 0;
for (const f of files) {
  const id = f.replace('.html', '');
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=index.html#/product/${id}">
  <title>Redirecting to ${id}...</title>
  <script>window.location.replace("index.html#/product/${id}");</script>
</head>
<body>
  <p>Redirecting to <a href="index.html#/product/${id}">Product Page</a>...</p>
</body>
</html>`;
  fs.writeFileSync(path.join(rootDir, f), html, 'utf8');
  patched++;
}

console.log(`Successfully patched ${patched} legacy HTML files with auto-redirect to React PDP!`);
