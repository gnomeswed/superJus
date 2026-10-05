# -*- coding: utf-8 -*-
import urllib.request, json, ssl, sys

sys.stdout.reconfigure(encoding="utf-8")

token = "8831011573:AAFl2yA2C-fpczLIdMi3iQhRLQUBxCsBnIw"
ctx = ssl._create_unverified_context()

try:
    url_me = f"https://api.telegram.org/bot{token}/getMe"
    req = urllib.request.Request(url_me)
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        me = json.loads(resp.read().decode("utf-8"))
        print("BOT INFO:", json.dumps(me, indent=2, ensure_ascii=False))
except Exception as e:
    print("Erro getMe:", e)

try:
    url_up = f"https://api.telegram.org/bot{token}/getUpdates?limit=5"
    req2 = urllib.request.Request(url_up)
    with urllib.request.urlopen(req2, context=ctx, timeout=10) as resp:
        up = json.loads(resp.read().decode("utf-8"))
        print("\nUPDATES RECENTES:")
        for res in up.get("result", [])[-5:]:
            msg = res.get("message") or res.get("channel_post") or {}
            chat = msg.get("chat", {})
            sender = msg.get("from", {})
            text = msg.get("text", "")
            print(f"Chat ID: {chat.get('id')} ({chat.get('title') or chat.get('first_name')}) | From: {sender.get('first_name')} | Msg: {text}")
except Exception as e:
    print("Erro getUpdates:", e)
