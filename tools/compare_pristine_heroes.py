import subprocess

out_cdd = subprocess.check_output(['git', 'show', 'cdd8d62:jewellery-design-html/index.html'], encoding='utf-8')
out_137 = subprocess.check_output(['git', 'show', '13797d6:jewellery-design-html/index.html'], encoding='utf-8')

p1 = out_cdd.find('<section class="relative w-full overflow-hidden bg-stone-900')
p1_end = out_cdd.find('</section>', p1) + len('</section>')

p2 = out_137.find('<section class="relative w-full overflow-hidden bg-stone-900')
p2_end = out_137.find('</section>', p2) + len('</section>')

print("cdd8d62 hero start:")
print(out_cdd[p1:p1+500])

print("\n13797d6 hero start:")
print(out_137[p2:p2+500])

with open('scratch_13797d6_hero.html', 'w', encoding='utf-8') as f:
    f.write(out_137[p2:p2_end])

