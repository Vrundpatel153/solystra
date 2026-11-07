from PIL import Image

im = Image.open('scratch/preview_gm_desktop.jpg')
w, h = im.size
print("Preview GM size:", w, h)

# Center of necklace is at x=48-50%, y=76-80%
for px, py in [(43.0, 80.0), (48.0, 76.0), (32.0, 70.0)]:
    x = int(w * px / 100)
    y = int(h * py / 100)
    cr = im.crop((x - 30, y - 30, x + 30, y + 30))
    cr.save(f"scratch/gm_point_{px}_{py}.jpg")
    print(f"Point {px}%, {py}%: rgb={im.getpixel((x, y))}")

