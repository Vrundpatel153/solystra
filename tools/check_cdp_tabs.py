import urllib.request
import json

try:
    with urllib.request.urlopen('http://127.0.0.1:9222/json') as resp:
        tabs = json.loads(resp.read().decode('utf-8'))
        print(f"Connected! Found {len(tabs)} tabs:")
        for t in tabs:
            print(f" - {t.get('type')}: {t.get('title')} | {t.get('url')} (id: {t.get('id')})")
except Exception as e:
    print("Error connecting to CDP:", e)

