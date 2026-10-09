import os
import re

# Comprehensive color replacement dictionary
# Keys will be matched case-insensitively where appropriate
HEX_REPLACEMENTS = [
    # Full 8-digit hex with alpha
    ('#7a152ecc', '#145c59cc'),
    ('#7A152ECC', '#145C59CC'),
    ('#7a152e99', '#145c5999'),
    ('#7A152E99', '#145C5999'),
    ('#7a152e80', '#145c5980'),
    ('#7A152E80', '#145C5980'),
    ('#7a152e66', '#145c5966'),
    ('#7A152E66', '#145C5966'),
    ('#7a152e59', '#145c5959'),
    ('#7A152E59', '#145C5959'),
    ('#7a152e4d', '#145c594d'),
    ('#7A152E4D', '#145C594D'),
    ('#7a152e33', '#145c5933'),
    ('#7A152E33', '#145C5933'),
    ('#7a152e26', '#145c5926'),
    ('#7A152E26', '#145C5926'),
    ('#7a152e1a', '#145c591a'),
    ('#7A152E1A', '#145C591A'),
    ('#7a152e0d', '#145c590d'),
    ('#7A152E0D', '#145C590D'),
    ('#590d1ecc', '#0d3f3dcc'),
    ('#590D1ECC', '#0D3F3DCC'),
    
    # 6-digit hexes (Primary and shades)
    ('#7A152E', '#145C59'),
    ('#7a152e', '#145c59'),
    
    ('#590D1E', '#0D3F3D'),
    ('#590d1e', '#0d3f3d'),
    
    ('#5A0F22', '#0F4745'),
    ('#5a0f22', '#0f4745'),
    
    ('#8B1E3F', '#1A6E6B'),
    ('#8b1e3f', '#1a6e6b'),
    
    ('#A0284A', '#228B87'),
    ('#a0284a', '#228b87'),
    
    ('#4A0D1C', '#082827'),
    ('#4a0d1c', '#082827'),
    
    ('#3B0713', '#082827'),
    ('#3b0713', '#082827'),
    
    ('#3D0712', '#082827'),
    ('#3d0712', '#082827'),
    
    # Background soft & tint tints
    ('#FAF0F2', '#F0F7F6'),
    ('#faf0f2', '#f0f7f6'),
    
    ('#FBF2F4', '#F0F7F6'),
    ('#fbf2f4', '#f0f7f6'),
    
    ('#F3E2E6', '#E1EFEB'),
    ('#f3e2e6', '#e1efeb'),
    
    ('#F6E6E9', '#E1EFEB'),
    ('#f6e6e9', '#e1efeb'),
]

RGBA_REPLACEMENTS = [
    (r'rgba\(\s*122\s*,\s*21\s*,\s*46', 'rgba(20, 92, 89'),
    (r'rgba\(\s*89\s*,\s*13\s*,\s*30', 'rgba(13, 63, 61'),
]

TEXT_REPLACEMENTS = [
    ('deep-burgundy suede velvet keepsake box', 'bespoke deep-emerald suede velvet keepsake box'),
    ('Deep burgundy suede box', 'Deep emerald suede box'),
    ('brand burgundy & gold', 'brand emerald & gold'),
    ('brand burgundy', 'brand emerald'),
    ('bg-rose-50', 'bg-[#F0F7F6]'),
]

def retheme_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # 1. Hex replacements
    for old_hex, new_hex in HEX_REPLACEMENTS:
        content = content.replace(old_hex, new_hex)
        
    # 2. RGBA replacements
    for pat, rep in RGBA_REPLACEMENTS:
        content = re.sub(pat, rep, content)
        
    # 3. Specific text / tailwind replacements
    for old_txt, new_txt in TEXT_REPLACEMENTS:
        content = content.replace(old_txt, new_txt)
        
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
    
    specific_files = [
        os.path.join(root, 'tailwind.config.js'),
        os.path.join(root, 'index.html'),
        os.path.join(root, 'tools', 'build_catalog.js'),
    ]
    
    modified_files = []
    
    # Process target directories
    for d in target_dirs:
        for dirpath, _, filenames in os.walk(d):
            for fname in filenames:
                if fname.endswith(('.jsx', '.js', '.css', '.html', '.json')):
                    fpath = os.path.join(dirpath, fname)
                    if retheme_file(fpath):
                        modified_files.append(os.path.relpath(fpath, root))
                        
    # Process specific files
    for fpath in specific_files:
        if os.path.exists(fpath):
            if retheme_file(fpath):
                modified_files.append(os.path.relpath(fpath, root))
                
    print(f"Successfully re-themed {len(modified_files)} files across React and HTML projects:")
    for f in modified_files:
        print(f"  - {f}")

if __name__ == '__main__':
    main()
