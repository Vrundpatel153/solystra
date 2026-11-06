import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in ['jewellery-design-html/css/styles.css', 'jewellery-design-html-dist/css/styles.css', r'c:\Users\vrund\OneDrive\Desktop\solystra-html\css\styles.css', 'src/index.css']:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        target = 'top: calc(74px + 1.25rem) !important; /* 94px: stays fixed with elegant breathing room below 74px header */'
        repl = 'top: calc(74px + 1.5rem) !important; /* 98px: stays fixed with generous breathing room below 74px header */'
        if target in c:
            c = c.replace(target, repl)
            with open(p, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated {p}")
        else:
            print(f"Target not found in {p}")
    except Exception as e:
        print(f"Error {p}: {e}")

