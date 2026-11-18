#!/usr/bin/env python3
"""
BẤM NÚT RUN (▶) TRÊN FILE NÀY TRONG VS CODE ĐỂ MỞ WEB GAME CHẠY LUÔN!
=====================================================================
- Tự động cài đặt thư viện (npm install) nếu chạy lần đầu.
- Tự động khởi động máy chủ web tại http://localhost:3000.
- Tự động mở trình duyệt mặc định của bạn vào thẳng game Fleet Battle.
"""

import os
import shutil
import subprocess
import sys
import time
import urllib.request
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
URL = "http://localhost:3000"


def is_server_ready() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:3000", timeout=0.6) as resp:
            return resp.status < 500
    except Exception:
        return False


def main() -> None:
    print("=" * 54)
    print("  FLEET BATTLE — KHOI CHAY WEB GAME TU VS CODE")
    print("=" * 54)

    if is_server_ready():
        print(f"Game đang chạy sẵn tại {URL} — Đang mở trình duyệt...")
        webbrowser.open(URL)
        return

    npm_cmd = shutil.which("npm")
    if not npm_cmd:
        print("\n[LỖI] Máy bạn chưa cài Node.js / npm.")
        print("Vui lòng cài Node.js LTS tại https://nodejs.org để chạy bản Web,")
        print("HOẶC mở file python_ai/fleet_battle_ai.py và bấm Run để chơi bản Python Terminal!")
        sys.exit(1)

    use_shell = os.name == "nt"

    if not (ROOT_DIR / "node_modules").exists():
        print("\nLần đầu chạy: đang tự động cài đặt gói thư viện (npm install)...")
        res = subprocess.run(["npm", "install"], cwd=ROOT_DIR, shell=use_shell)
        if res.returncode != 0:
            print("[LỖI] Không thể chạy npm install.")
            sys.exit(res.returncode)
        print("Cài đặt hoàn tất!\n")

    print(f"Đang khởi động máy chủ game tại {URL} ...")
    proc = subprocess.Popen(["npm", "run", "dev"], cwd=ROOT_DIR, shell=use_shell)

    opened = False
    try:
        for _ in range(80):
            if proc.poll() is not None:
                break
            if is_server_ready():
                print(f"\n>>> Đang mở trình duyệt web: {URL} <<<")
                print("(Giữ cửa sổ Terminal này mở trong lúc chơi. Nhấn Ctrl+C để tắt.)\n")
                webbrowser.open(URL)
                opened = True
                break
            time.sleep(0.4)

        if not opened and proc.poll() is None:
            webbrowser.open(URL)

        proc.wait()
    except KeyboardInterrupt:
        print("\nĐang dừng máy chủ game...")
        proc.terminate()


if __name__ == "__main__":
    main()
