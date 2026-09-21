import fs from 'fs';

try {
  const text = fs.readFileSync('solystra_index.html', 'utf8');
  const imgMatches = text.match(/<img[^>]+>/gi) || [];
  console.log('Total img tags in solystra_index.html:', imgMatches.length);
  const logoImgs = imgMatches.filter(tag => /logo|brand|soulystra|solystra/i.test(tag));
  console.log('Logo img tags:', logoImgs);

  const svgs = text.match(/<svg[^>]*>[\s\S]*?<\/svg>/gi) || [];
  console.log('Total svgs:', svgs.length);
  const logoSvgs = svgs.filter(s => /logo|brand|soulystra|solystra/i.test(s));
  console.log('Logo svgs:', logoSvgs.length);
} catch (e) {
  console.error(e);
}
