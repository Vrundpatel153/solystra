with open('src/pages/HomePage.jsx', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('const TOP_COLLECTIONS = [')
if idx != -1:
    idx2 = c.find('];', idx)
    print(c[idx:idx2+2])

