from PIL import Image, ImageDraw

def render_preview(orig_path, w, h, obj_pos_x, obj_pos_y, pins, out_path):
    im = Image.open(orig_path).convert('RGB')
    orig_w, orig_h = im.size
    scale = max(w / orig_w, h / orig_h)
    sc_w, sc_h = int(orig_w * scale), int(orig_h * scale)
    scaled = im.resize((sc_w, sc_h), Image.Resampling.LANCZOS)
    
    crop_x = int((sc_w - w) * (obj_pos_x / 100.0))
    crop_y = int((sc_h - h) * (obj_pos_y / 100.0))
    
    cropped = scaled.crop((crop_x, crop_y, crop_x + w, crop_y + h))
    draw = ImageDraw.Draw(cropped)
    
    for p in pins:
        px = int(w * p['x'] / 100.0)
        py = int(h * p['y'] / 100.0)
        # draw pin
        r = 12
        draw.ellipse([(px - r, py - r), (px + r, py + r)], fill=(97, 83, 46, 180), outline=(212, 175, 55), width=2)
        draw.ellipse([(px - 3, py - 3), (px + 3, py + 3)], fill=(255, 255, 255))
        draw.text((px + 14, py - 6), p['label'], fill=(255, 215, 0))
        
    cropped.save(out_path, quality=95)
    print(f"Saved {out_path}")

# Desktop: 480 x 600
render_preview('scratch/curated_raw/second_combo.png', 480, 600, 50, 40, [
    {'x': 65.4, 'y': 37.0, 'label': 'Earring'},
    {'x': 43.4, 'y': 79.5, 'label': 'Necklace'}
], 'scratch/preview_c2_desktop.jpg')

render_preview('scratch/curated_raw/golden_meadow_set_combo.png', 480, 600, 50, 40, [
    {'x': 43.0, 'y': 80.0, 'label': 'Golden Meadow Suite'}
], 'scratch/preview_gm_desktop.jpg')

# Mobile: 358 x 460
render_preview('scratch/curated_raw/second_combo.png', 358, 460, 50, 40, [
    {'x': 65.4, 'y': 37.0, 'label': 'Earring'},
    {'x': 43.4, 'y': 79.6, 'label': 'Necklace'}
], 'scratch/preview_c2_mobile.jpg')

render_preview('scratch/curated_raw/golden_meadow_set_combo.png', 358, 460, 50, 40, [
    {'x': 43.0, 'y': 79.9, 'label': 'Golden Meadow Suite'}
], 'scratch/preview_gm_mobile.jpg')

