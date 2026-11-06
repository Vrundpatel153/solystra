import subprocess

commits = ['cdd8d62', '38b9195', 'de807ee', '13797d6', '07a92f2']

for c in commits:
    try:
        out = subprocess.check_output(['git', 'show', f'{c}:jewellery-design-html/index.html'], encoding='utf-8')
        pos_hero = out.find('id="hero-section"')
        if pos_hero == -1:
            pos_hero = out.find('solystra-hero-wrap')
        if pos_hero == -1:
            pos_hero = out.find('<section')
        # Find where hero section ends
        pos_hero_end = out.find('</section>', pos_hero) + len('</section>')
        print(f"=== COMMIT {c} HERO SECTION (length {pos_hero_end - pos_hero}) ===")
        print(out[pos_hero:pos_hero+1200])
        print("...\n")
    except Exception as e:
        print(f"Error checking commit {c}:", e)

