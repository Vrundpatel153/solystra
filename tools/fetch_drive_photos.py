import os
import urllib.request
import time

files = {
  "DSC02659.JPG": "1_eO4lROd3SY2IO54ry_llCM7kGZmr2Uw",
  "DSC02660.JPG": "1BNN0W34euH7NIA8vI2yhwqtJvI52owNb",
  "DSC02661.JPG": "1xw_gQlOfq_2GIIhXattZLz0K97fQvH_x",
  "DSC02662.JPG": "18QZrr9lKsUY7Psl2UNGXN8a1uDGt4nr5",
  "DSC02663.JPG": "1B-p-FQ2KoZwBA6PRyHLJoYpCLfjU2dPr",
  "DSC02664.JPG": "14UX_V0Tej5FD-6Rus6o3dGFnqngajpRn",
  "DSC02665.JPG": "1g81FfGai7z25Tr8cAZrzktRGaUkezdpH",
  "DSC02666.JPG": "1kl609v8tMpBBXKmGVSbSq-1zN1klK8tP",
  "DSC02667.JPG": "1IUR7FmK1FJpXjOW0_QEq0xC_ZOQ5WNEX",
  "DSC02668.JPG": "1EyMgoEWqt9grrF05tl5ImXkLiqrOROAk",
  "DSC02669.JPG": "1cClA6fTIZb2nut225cQZu946YhjWyLZ0",
  "DSC02671.JPG": "1YzMAVMV---zra1xj8uPN50K8QHLCyppV",
  "DSC02672.JPG": "1vh_nLulTMiGZLnaMRsESFibCSiqX9azF",
  "DSC02673.JPG": "1NeJvgPnmHOBsGQlBdnjquDbDW6OkFKbI",
  "DSC02674.JPG": "1IEnYepH-veeOo5a_gikRAg8In82O9ugv",
  "DSC02675.JPG": "1HYRGaqEYyzVnvMF4Afz1JZaxuPMBJk9r",
  "DSC02676.JPG": "1f8PZTwXRt4yTjgg0iWFjKC5NKFROGvvI",
  "DSC02677.JPG": "1TCxcCxx9-lR5A95gYXeX6fQ4NTTIWna",
  "DSC02678.JPG": "1rn95XuaqEiOlomxDYK_0BgNe_F9oYTOr"
}

out_dir = 'scratch/drive_photos'
os.makedirs(out_dir, exist_ok=True)

for name, fid in files.items():
    dest = os.path.join(out_dir, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"Already downloaded: {name}")
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

print("Download complete!")

