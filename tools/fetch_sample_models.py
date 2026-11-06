import os
import urllib.request
import time

os.makedirs('scratch/model_check', exist_ok=True)

test_files = {
    'DSC02686.JPG': '1ds7VZF3Qemu1MblZLEiNnVy9Ni_mYKZv',
    'DSC02700.JPG': '15GLaWJg8E1TQUKrqoGg1j8K-e8UsEzHH',
    'DSC02715.JPG': '10omNDc-CU_PWMj25pGKu-xA7yf6QX9zO',
    'DSC02725.JPG': '1X-UWFYWOsN5ijW3Qvo4ZVahItkShXylI',
}

for name, fid in test_files.items():
    dest = os.path.join('scratch/model_check', name)
    if os.path.exists(dest):
        continue
    url = f"https://drive.google.com/thumbnail?id={fid}&sz=w800"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            with open(dest, 'wb') as f:
                f.write(data)
            print(f"Downloaded {name} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {name}: {e}")
    time.sleep(0.3)

print("Sample check complete!")

