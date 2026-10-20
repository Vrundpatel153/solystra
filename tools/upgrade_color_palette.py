import os
import re

# Precise color replacements according to user specifications:
# Primary dark: #61532E (buttons, gradients, dark highlights, white text)
# Secondary: #CEBDA7 (warm sandstone / linen taupe for borders, secondary buttons, tags)
# Golden: #C5A059 / #9E7B35 (for contrast: stars, ratings, hallmark, luxury shimmer)
# White: #FFFFFF (crisp contrast on dark buttons & cards)

REPLACEMENTS = [
    # 1. Old emerald mint tints -> Secondary soft sandstone tint
    ('#F0F7F6', '#F6F3EE'),
    ('#f0f7f6', '#f6f3ee'),
    ('#E1EFEB', '#EFEAE3'),
    ('#e1efeb', '#efeae3'),

    # 2. Old ruby/maroon borders and dark shades
    ('#EAD5DA', '#CEBDA7'),
    ('#ead5da', '#cebda7'),
    ('#4A0A19', '#3D341B'),
    ('#4a0a19', '#3d341b'),
    ('#8E1B38', '#61532E'),
    ('#8e1b38', '#61532e'),
    ('#2A1520', '#3D341B'),
    ('#2a1520', '#3d341b'),

    # 3. Old neutral/gray borders -> Secondary #CEBDA7
    ('#EAE4DC', '#CEBDA7'),
    ('#eae4dc', '#cebda7'),
    ('#EAE5DB', '#CEBDA7'),
    ('#eae5db', '#cebda7'),

    # 4. Any remaining emerald green codes
    ('#145C59', '#61532E'),
    ('#145c59', '#61532e'),
    ('#0D3F3D', '#3D341B'),
    ('#0d3f3d', '#3d341b'),
    ('#0F4745', '#4D4224'),
    ('#0f4745', '#4d4224'),
    ('#1A6E6B', '#7A693A'),
    ('#1a6e6b', '#7a693a'),
    ('#228B87', '#938048'),
    ('#228b87', '#938048'),
    ('#082827', '#252010'),
    ('#082827', '#252010'),
]

TARGET_DIRS = [
    'src',
    'jewellery-design-html',
    'jewellery-design-html-dist',
]

def upgrade_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    modified_count = 0

    for d in TARGET_DIRS:
        target_dir = os.path.join(root, d)
        if not os.path.exists(target_dir):
            continue
        for dirpath, _, filenames in os.walk(target_dir):
            for fn in filenames:
                if fn.endswith(('.jsx', '.js', '.css', '.html')):
                    fpath = os.path.join(dirpath, fn)
                    if upgrade_file(fpath):
                        modified_count += 1

    print(f"Successfully upgraded palette in {modified_count} files.")

if __name__ == '__main__':
    main()
