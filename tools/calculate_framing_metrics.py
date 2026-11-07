from PIL import Image

# Let's inspect the position of the necklace in each generated test:
# In C2:
# Pendant is at Y in original: ~1000.
# Earring is at Y in original: ~460.
# Top of head is at Y in original: ~120.

for h in [460, 480, 500, 520]:
    for p in [45, 55, 65]:
        scale = 592 / 1024
        sc_h = 1536 * scale
        max_crop = sc_h - h
        crop_y = max_crop * (p / 100.0)
        
        orig_top_y = crop_y / scale
        orig_bottom_y = (crop_y + h) / scale
        
        # Check if head (120), earring (460), and necklace (1000) are inside
        head_in = orig_top_y <= 200
        earring_in = orig_top_y <= 450 and orig_bottom_y >= 500
        neck_in = orig_bottom_y >= 1080 # at least 80px below pendant
        
        print(f"Desktop h={h}, pos={p}% -> visible orig Y: {orig_top_y:.0f} to {orig_bottom_y:.0f} | head:{head_in} ear:{earring_in} neck:{neck_in}")

print("\n--- Mobile Tests ---")
for h in [400, 440, 480]:
    for p in [45, 55, 65]:
        scale = max(358 / 1024, h / 1536) # on mobile, if h=480, scale is 480/1536 or 358/1024
        # if 358/1024=0.3496, then 1536*0.3496=537.
        sc_h = 1536 * (358 / 1024)
        max_crop = sc_h - h
        crop_y = max_crop * (p / 100.0)
        orig_top_y = crop_y / (358 / 1024)
        orig_bottom_y = (crop_y + h) / (358 / 1024)
        head_in = orig_top_y <= 200
        earring_in = orig_top_y <= 450 and orig_bottom_y >= 500
        neck_in = orig_bottom_y >= 1080
        print(f"Mobile h={h}, pos={p}% -> visible orig Y: {orig_top_y:.0f} to {orig_bottom_y:.0f} | head:{head_in} ear:{earring_in} neck:{neck_in}")

