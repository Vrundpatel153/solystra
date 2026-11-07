import ctypes
from ctypes import wintypes
import urllib.request
import json
import time
import os
import sys

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEV_PROFILE_DIR = r"C:\Users\vrund\chrome-debug-profile"
DEBUG_PORT = 9222

class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('lpReserved', wintypes.LPWSTR),
        ('lpDesktop', wintypes.LPWSTR),
        ('lpTitle', wintypes.LPWSTR),
        ('dwX', wintypes.DWORD),
        ('dwY', wintypes.DWORD),
        ('dwXSize', wintypes.DWORD),
        ('dwYSize', wintypes.DWORD),
        ('dwXCountChars', wintypes.DWORD),
        ('dwYCountChars', wintypes.DWORD),
        ('dwFillAttribute', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('wShowWindow', wintypes.WORD),
        ('cbReserved2', wintypes.WORD),
        ('lpReserved2', ctypes.POINTER(ctypes.c_byte)),
        ('hStdInput', wintypes.HANDLE),
        ('hStdOutput', wintypes.HANDLE),
        ('hStdError', wintypes.HANDLE),
    ]

class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ('hProcess', wintypes.HANDLE),
        ('hThread', wintypes.HANDLE),
        ('dwProcessId', wintypes.DWORD),
        ('dwThreadId', wintypes.DWORD),
    ]

def is_cdp_ready():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=1) as resp:
            data = json.loads(resp.read().decode())
            return True
    except Exception:
        return False

def ensure_visible_chrome(urls=None):
    if urls is None:
        urls = ["http://127.0.0.1:8095/index.html"]

    urls_str = " ".join(f'"{u}"' for u in urls)

    if is_cdp_ready():
        print(f"Visible Chrome CDP is already active on port {DEBUG_PORT}.", flush=True)
        return True

    cmd_line = f'"{CHROME_PATH}" --remote-debugging-port={DEBUG_PORT} --user-data-dir="{DEV_PROFILE_DIR}" --no-first-run --no-default-browser-check --new-window {urls_str}'
    
    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    si.lpDesktop = r"WinSta0\Default"
    
    pi = PROCESS_INFORMATION()
    
    success = ctypes.windll.kernel32.CreateProcessW(
        None,
        cmd_line,
        None,
        None,
        False,
        0,
        None,
        None,
        ctypes.byref(si),
        ctypes.byref(pi)
    )
    if not success:
        print(f"Failed to launch Chrome on WinSta0\\Default: error {ctypes.GetLastError()}", flush=True)
        return False

    ctypes.windll.kernel32.CloseHandle(pi.hProcess)
    ctypes.windll.kernel32.CloseHandle(pi.hThread)

    for _ in range(20):
        time.sleep(0.5)
        if is_cdp_ready():
            print(f"Visible Chrome launched successfully on your screen with CDP port {DEBUG_PORT}!", flush=True)
            return True

    print("Chrome launched but CDP port took too long to respond.", flush=True)
    return False

if __name__ == '__main__':
    target_urls = sys.argv[1:] if len(sys.argv) > 1 else ["http://127.0.0.1:8095/index.html"]
    ensure_visible_chrome(target_urls)
