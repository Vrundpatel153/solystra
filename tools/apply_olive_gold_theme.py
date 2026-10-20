import os
import re

# Surgical replacement: ONLY replace the emerald green colors (#145C59 and dark hover shades)
# with #61532e and its deep tone.
# Backgrounds (#FAF8F5, #FFFFFF), champagne gold (#C5A059), soft tints (#F0F7F6, #E1EFEB),
# and neutral borders (#EAE4DC) remain 100% UNTOUCHED to avoid turning the site golden.

EXACT_REPLACEMENTS = [
    # 8-digit hexes with alpha (both case variants)
    ('#145c59cc', '#61532ecc'),
    ('#145C59CC', '#61532ECC'),
    ('#145c5999', '#61532e99'),
    ('#145C5999', '#61532E99'),
    ('#145c5980', '#61532e80'),
    ('#145C5980', '#61532E80'),
    ('#145c5966', '#61532e66'),
    ('#145C5966', '#61532E66'),
    ('#145c5959', '#61532e59'),
    ('#145C5959', '#61532E59'),
    ('#145c594d', '#61532e4d'),
    ('#145C594D', '#61532E4D'),
    ('#145c5933', '#61532e33'),
    ('#145C5933', '#61532E33'),
    ('#145c5926', '#61532e26'),
    ('#145C5926', '#61532E26'),
    ('#145c591a', '#61532e1a'),
    ('#145C591A', '#61532E1A'),
    ('#145c590d', '#61532e0d'),
    ('#145C590D', '#61532E0D'),
    ('#0d3f3dcc', '#3d341bcc'),
    ('#0D3F3DCC', '#3D341BCC'),

    # 6-digit hexes (Primary Green -> #61532e)
    ('#145C59', '#61532E'),
    ('#145c59', '#61532e'),

    # Darker hover / button border green
    ('#0D3F3D', '#3D341B'),
    ('#0d3f3d', '#3d341b'),

    ('#0F4745', '#4A3F22'),
    ('#0f4745', '#4a3f22'),

    # Dark gradient end
    ('#082827', '#252010'),
    ('#082827', '#252010'),

    # Rich accent
    ('#1A6E6B', '#7A693A'),
    ('#1a6e6b', '#7a693a'),

    # Light green accent
    ('#228B87', '#938048'),
    ('#228b87', '#938048'),
]

REGEX_REPLACEMENTS = [
    # RGBA values
    (r'rgba?\(\s*20\s*,\s*92\s*,\s*89', 'rgba(97, 83, 46'),
    (r'rgba?\(\s*13\s*,\s*63\s*,\s*61', 'rgba(61, 52, 27'),
    (r'rgba?\(\s*26\s*,\s*110\s*,\s*107', 'rgba(122, 105, 58'),
    (r'rgb\(\s*20\s+92\s+89', 'rgb(97 83 46'),
    (r'rgb\(\s*13\s+63\s+61', 'rgb(61 52 27'),
    (r'rgb\(\s*26\s+110\s+107', 'rgb(122 105 58'),
    (r'hover:bg-emerald-800', 'hover:bg-[#252010]'),
]

def retheme_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    original = content

    for old, new in EXACT_REPLACEMENTS:
        content = content.replace(old, new)

    for pat, rep in REGEX_REPLACEMENTS:
        content = re.sub(pat, rep, content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_dirs = [
        os.path.join(root, 'src'),
        os.path.join(root, 'jewellery-design-html'),
        os.path.join(root, 'jewellery-design-html-dist'),
    ]

    target_files = [
        os.path.join(root, 'tailwind.config.js'),
        os.path.join(root, 'index.html'),
    ]

    count = 0
    for d in target_dirs:
        if not os.path.exists(d):
            continue
        for dirpath, _, filenames in os.walk(d):
            for fname in filenames:
                if fname.endswith(('.jsx', '.js', '.css', '.html')):
                    fpath = os.path.join(dirpath, fname)
                    if retheme_file(fpath):
                        count += 1

    for fpath in target_files:
        if os.path.exists(fpath):
            if retheme_file(fpath):
                count += 1

    print(f"Applied surgical #61532e theme to {count} files.")

if __name__ == '__main__':
    main()
