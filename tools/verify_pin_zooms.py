from PIL import Image

# Let's inspect the crops around the pin centers:
im_c2 = Image.open('scratch/preview_c2_desktop.jpg')
# Earring pin at x=65.4% (314px), y=37.0% (222px)
ear_crop = im_c2.crop((314 - 40, 222 - 40, 314 + 40, 222 + 40))
ear_crop.save('scratch/pin_ear_c2_zoom.jpg')

# Necklace pin at x=43.4% (208px), y=79.5% (477px)
neck_crop = im_c2.crop((208 - 40, 477 - 40, 208 + 40, 477 + 40))
neck_crop.save('scratch/pin_neck_c2_zoom.jpg')

im_gm = Image.open('scratch/preview_gm_desktop.jpg')
# Choker pin at x=43.0% (206px), y=80.0% (480px)
chok_crop = im_gm.crop((206 - 40, 480 - 40, 206 + 40, 480 + 40))
chok_crop.save('scratch/pin_chok_gm_zoom.jpg')

print("Saved pin zoom crops!")

