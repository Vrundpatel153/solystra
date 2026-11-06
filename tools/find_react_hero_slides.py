with open('src/pages/HomePage.jsx', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('banner_pc_2.webp')
if idx != -1:
    print(c[idx-300:idx+1200])

