from PIL import Image

top_im = Image.open("scratch/calib_v2_top.jpg")
bot_im = Image.open("scratch/calib_v2_bottom.jpg")

# Crop box-c2-mob and box-c2-pc from top_im
crop_c2_mob = top_im.crop((20, 150, 20 + 360, 150 + 422))
crop_c2_pc = top_im.crop((410, 150, 410 + 594, 150 + 492))
crop_c2_mob.save("scratch/v2_crop_c2_mob.jpg")
crop_c2_pc.save("scratch/v2_crop_c2_pc.jpg")

# Crop box-gm-mob and box-gm-pc from bot_im
crop_gm_mob = bot_im.crop((20, 150, 20 + 360, 150 + 422))
crop_gm_pc = bot_im.crop((410, 150, 410 + 594, 150 + 492))
crop_gm_mob.save("scratch/v2_crop_gm_mob.jpg")
crop_gm_pc.save("scratch/v2_crop_gm_pc.jpg")

print("Saved v2 crops!")

