import subprocess

out = subprocess.check_output(['git', 'show', 'cdd8d62:jewellery-design-html/index.html'], encoding='utf-8')
pos_hero = out.find('<section class="relative w-full overflow-hidden bg-stone-900')
pos_hero_end = out.find('</section>', pos_hero) + len('</section>')

print("Length of cdd8d62 hero section:", pos_hero_end - pos_hero)
with open('scratch_cdd8d62_hero.html', 'w', encoding='utf-8') as f:
    f.write(out[pos_hero:pos_hero_end])
print("Saved scratch_cdd8d62_hero.html")

