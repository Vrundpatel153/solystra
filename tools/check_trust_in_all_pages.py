import glob

for f in sorted(glob.glob('jewellery-design-html/*.html')):
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    if '7-Day Exchanges' in content:
        count = content.count('7-Day Exchanges')
        print(f"{f}: {count} occurrences of '7-Day Exchanges'")

