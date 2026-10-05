# -*- coding: utf-8 -*-
"""
Ponte Discord -> Command Code (bridge bot, via REST, sem discord.py).
Escuta mensagens do canal de um servidor Discord (gateway REST via polling)
e executa comandos /check, /status, /run, /exec, /djen, respondendo no canal.

Config (scripts/discord_config.json):
  {
    "bot_token": "<TOKEN_BOT_DISCORD>",
    "channel_id": "<ID_CANAL_TEXTO>"
  }

Uso:
  python scripts/discord_bridge.py --once     # processa pendentes e sai
  python scripts/discord_bridge.py            # loop de polling
"""
import sys, os, json, time, ssl, urllib.request, urllib.parse, subprocess, pathlib
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "discord_config.json")
STATE_PATH = os.path.join(ROOT, ".agents", "discord_last_state.json")
SSL_CTX = ssl._create_unverified_context()

ALLOWED_CMDS = {"help", "check", "status", "djen", "run", "exec"}
API = "https://discord.com/api/v10"
PY = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def discord_api(token, method, path, payload=None):
    url = f"{API}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
        return json.loads(resp.read().decode() or "{}")


def discord_send(token, channel_id, text):
    text = text[:1900]
    discord_api(token, "POST", f"/channels/{channel_id}/messages", {"content": text})


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def build_help():
    return (
        "📱 **Comandos do SuperJus no Discord**\n"
        "`/check` → consulta TJRJ/DataJud agora (4 processos do Júlio)\n"
        "`/status` → última checagem e estado\n"
        "`/djen` → consulta DJEN STJ (HC 1.116.750)\n"
        "`/run <texto>` → envia instrução ao Command Code (modo IA)\n"
        "`/exec <cmd>` → executa comando shell (whitelist)\n"
    )


def do_check():
    mon = os.path.join(os.path.dirname(__file__), "telegram_monitor_julio.py")
    try:
        res = subprocess.run([PY, "-X", "utf8", mon, "--force"], capture_output=True, text=True, timeout=180)
        out = (res.stdout or "") + (res.stderr or "")
        return out[-3500:] or "(sem saída)"
    except subprocess.TimeoutExpired:
        return "Timeout após 180s (TJRJ lento)."
    except Exception as e:
        return f"Erro: {e}"


def do_status():
    st = load_state()
    t = datetime.now().strftime("%d/%m %H:%M")
    linhas = [f"📊 **JÚLIO — status** · {t}"]
    if not st:
        linhas.append("_Sem checagens ainda._")
    else:
        linhas.append(f"Última: `{st.get('_ultima_checagem','?')}`")
        for k, v in st.items():
            if k.startswith("_"):
                continue
            curto = k.replace("-51.2021.8.19.0078","").replace("-67.2026.8.19.0000","")
            linhas.append(f"• `{curto}` → _{v.get('resumo','')[:80]}_")
    return "\n".join(linhas)


def whitelist_exec(cmd):
    allowed = ("git ", "dir ", "ls ", "cat ", "type ", "python -X utf8 scripts/", "python scripts/", "cmd /c dir")
    blocked = ("rm ", "del ", "shutdown", "reboot", "curl ", "wget ", "nc ", "ncat", "powershell -enc", "Invoke-")
    low = cmd.lower().strip()
    if any(b in low for b in blocked):
        return None, "Comando bloqueado por política."
    if not any(low.startswith(p) for p in allowed) and low not in ("help", "pwd"):
        return None, f"Prefixo não permitido. Permitidos: {', '.join(allowed)}"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=str(ROOT))
        return res.returncode, (res.stdout or "") + (res.stderr or "")[-3000:]
    except subprocess.TimeoutExpired:
        return None, "Timeout 60s."
    except Exception as e:
        return None, str(e)


def handle_message(token, channel_id, text):
    raw = (text or "").strip()
    if not raw:
        return
    parts = raw.split(maxsplit=1)
    cmd = parts[0].lstrip("/").split("@")[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd not in ALLOWED_CMDS:
        discord_send(token, channel_id, f"Desconhecido `/{cmd}` → use /help")
        return
    if cmd == "help":
        discord_send(token, channel_id, build_help())
    elif cmd == "status":
        discord_send(token, channel_id, do_status())
    elif cmd == "check":
        discord_send(token, channel_id, "⏳ _checando TJRJ..._")
        out = do_check()
        discord_send(token, channel_id, out[:1900] or "(sem saída)")
    elif cmd == "djen":
        discord_send(token, channel_id, "_Tentando DJEN (STJ HC 1.116.750)..._")
        try:
            p = os.path.join(os.path.dirname(__file__), "djen_consulta_hc_stj.py")
            res = subprocess.run([PY, "-X", "utf8", p], capture_output=True, text=True, timeout=90)
            discord_send(token, channel_id, (res.stdout or res.stderr or "")[:1900])
        except Exception as e:
            discord_send(token, channel_id, f"Erro DJEN: {e}")
    elif cmd == "run":
        if not arg:
            discord_send(token, channel_id, "Uso: `/run <sua instrução>`")
            return
        discord_send(token, channel_id, "⏳ _processando..._")
        # Sem integração oficial do Command Code: retorna instrução clara
        discord_send(token, channel_id, "(modo IA do Discord desativado — use /check, /status, /djen, /exec)")
    elif cmd == "exec":
        if not arg:
            discord_send(token, channel_id, "Uso: `/exec <comando>` (whitelist)")
            return
        code, out = whitelist_exec(arg)
        discord_send(token, channel_id, f"*exit {code}*\n```\n{out[:1500]}\n```")


def fetch_new_messages(token, channel_id, after_id):
    """Busca mensagens do canal via REST (sem gateway). Retorna lista de msgs novas."""
    params = urllib.parse.urlencode({"limit": 10})
    url = f"{API}/channels/{channel_id}/messages?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bot {token}"})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
        msgs = json.loads(resp.read().decode())
    # msgs vêm em ordem desc (mais recente primeiro) — invertemos
    msgs = list(reversed(msgs))
    out = []
    for m in msgs:
        if m.get("author", {}).get("bot"):
            continue
        if after_id and m["id"] <= after_id:
            continue
        out.append(m)
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    token = cfg.get("bot_token", "").strip()
    channel_id = cfg.get("channel_id", "").strip()
    if not token or not channel_id:
        print("ERRO: configure bot_token e channel_id em scripts/discord_config.json")
        sys.exit(1)

    st = load_state()
    last = st.get("_last_msg_id", "")

    if args.once:
        try:
            for m in fetch_new_messages(token, channel_id, last):
                handle_message(token, channel_id, m.get("content", ""))
                last = m["id"]
            st["_last_msg_id"] = last
            save_state(st)
            print(f"OK: {last}")
        except Exception as e:
            print(f"ERRO: {e}")
        return

    # loop
    while True:
        try:
            for m in fetch_new_messages(token, channel_id, last):
                handle_message(token, channel_id, m.get("content", ""))
                last = m["id"]
            st["_last_msg_id"] = last
            save_state(st)
        except Exception as e:
            print(f"[loop] {e}", flush=True)
        time.sleep(5)


if __name__ == "__main__":
    main()
