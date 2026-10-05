# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
import urllib.request, json

TOKEN = "8831011573:AAFl2yA2C-fpczLIdMi3iQhRLQUBxCsBnIw"
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
try:
    req = urllib.request.Request(url)
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
    print("BOT:", json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print("getMe erro:", e)

url2 = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
try:
    req = urllib.request.Request(url2)
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
    print("\nUPDATES:", json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    for u in data.get("result", [])[-5:]:
        chat = u.get("message", {}).get("chat", {}) or u.get("channel_post", {}).get("chat", {}) or u.get("my_chat_member", {}).get("chat", {})
        print(f"  chat id={chat.get('id')} type={chat.get('type')} title={chat.get('title')} username={chat.get('username')}")
except Exception as e:
    print("getUpdates erro:", e)
