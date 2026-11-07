import asyncio
import json
import urllib.request
import websockets
import re

async def main():
    req = urllib.request.urlopen("http://127.0.0.1:9222/json")
    tabs = json.loads(req.read().decode())
    
    tab = None
    for t in tabs:
        if t.get('type') == 'page' and 'drive.google.com' in t.get('url', ''):
            tab = t
            break
            
    if not tab:
        print("Drive tab not found")
        return

    ws_url = tab['webSocketDebuggerUrl']
    async with websockets.connect(ws_url, max_size=50*1024*1024) as ws:
        msg_id = 1
        async def send(method, params=None):
            nonlocal msg_id
            m = {"id": msg_id, "method": method, "params": params or {}}
            msg_id += 1
            await ws.send(json.dumps(m))
            while True:
                res = json.loads(await ws.recv())
                if res.get("id") == m["id"]:
                    return res.get("result", {})

        # Extract html of the script tag with ds:3 or all script contents
        scripts_data = await send("Runtime.evaluate", {
            "expression": """(() => {
                const scripts = Array.from(document.querySelectorAll('script'));
                for (const s of scripts) {
                    if (s.innerText.includes('hero-banner') || s.innerText.includes('WIZ_global_data') || s.className.includes('ds:')) {
                        return s.innerText;
                    }
                }
                return document.body.innerHTML;
            })()""",
            "returnByValue": True
        })
        text = scripts_data.get('result', {}).get('value', '')
        print("Script text length:", len(text))

        # Search for all folder and file names and IDs
        # Pattern in Drive data: [[null, "FILE_OR_FOLDER_ID"], ... , "NAME", ...]
        # Or look for matches: [null,"([a-zA-Z0-9_-]{20,})"].*?"([^"]+)"
        matches = re.findall(r'\[(?:null,)?\"([a-zA-Z0-9_-]{25,40})\"\][^\"]{0,500}?\"([^\"]{3,80})\"', text)
        print(f"Found {len(matches)} regex matches:")
        seen = set()
        for fid, name in matches:
            if fid not in seen and not name.startswith('application/'):
                seen.add(fid)
                print(f"ID: {fid} -> Name: {name}")

        with open("scratch/drive_root_script.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Saved raw script to scratch/drive_root_script.txt")

if __name__ == '__main__':
    asyncio.run(main())
