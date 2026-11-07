from PIL import Image

im = Image.open('scratch/c2_exact_earring_zoom.jpg')
w, h = im.size
print("Crop size:", w, h)
# Print min/max RGB in crop
colors = [im.getpixel((x, y)) for y in range(0, h, 5) for x in range(0, w, 5)]
# Sort by brightness
colors_sorted = sorted(colors, key=lambda c: sum(c), reverse=True)
print("Top 10 brightest pixels in earring crop:", colors_sorted[:10])

