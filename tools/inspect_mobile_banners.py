from PIL import Image

for name in ['banner_mob_1.webp', 'banner_mob_2.webp', 'banner_floral_portrait_mob.webp', 'banner_profile_floral_mob.webp']:
    p = f'jewellery-design-html/solystra_assets/banners/{name}'
    im = Image.open(p)
    print(name, im.size)

