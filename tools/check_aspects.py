from PIL import Image

for i in [3, 4]:
    for mode in ['pc', 'mob']:
        path = f'jewellery-design-html/solystra_assets/banners/banner_{mode}_{i}.webp'
        im = Image.open(path)
        print(f"Banner {i} {mode}: size={im.size}, aspect={im.width/im.height:.2f}")

