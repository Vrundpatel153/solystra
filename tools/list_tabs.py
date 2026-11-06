import urllib.request
import json

req = urllib.request.urlopen('http://127.0.0.1:9222/json')
tabs = json.loads(req.read().decode())
for t in tabs:
    if t.get('type') == 'page':
        print(f"{t.get('id')} | {t.get('title')} | {t.get('url')}")

