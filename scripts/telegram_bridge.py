# -*- coding: utf-8 -*-
"""
Ponte Telegram → Command Code (bridge bot).
Fica escutando o Telegram via long polling e, para cada comando em /help,/check,/status,/djen,/ocr,/run,
executa a ação correspondente e responde no mesmo chat.

Uso:
  python scripts/telegram_bridge.py                     # roda em foreground
  python scripts/telegram_bridge.py --once              # processa pendentes e sai
  python scripts/telegram_bridge.py --set-commands      # registra menu de comandos no Telegram

Comandos no Telegram (grupo Swd hermes / privado):
  /help                         - lista comandos
  /check                        - checa TJRJ/DataJud agora (os 4 do Júlio) e responde o espelho
  /status                       - mostra última checagem, cron, memória
  /djen                         - consulta DJEN (STJ HC 1.116.750) quando a rota BR estiver OK
  /ocr <anexo ou DJERJ_*.pdf>   - roda OCR nos PDFs do DJERJ (precisa enviar arquivo ou nome)
  /run <texto livre>            - encaminha <texto> como prompt para o Command Code (via memu/shell)
  /exec <comando shell>         - executa comando shell restrito (whitelist) e devolve saída

Segurança: só responde para chat_id configurado em telegram_config.json (allowed).
Telegram entrega vai para o cron já existente (telegram_monitor_julio.py) — este bridge é para COMANDOS sob demanda.
"""
import sys
import os
import json
import re
import ssl
import time
import hashlib
import urllib.request
import urllib.parse
import subprocess
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "..", ".agents", "telegram_last_state.json")
SSL_CTX = ssl._create_unverified_context()

ALLOWED_CMDS = {"help", "check", "status", "djen", "ocr", "run", "exec"}
CC_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
CC_SYSTEM = (
    "Você é o Analista Jurídico Criminal de Alta Performance do SuperJus (Command Code), "
    "especialista em Direito Penal/Processual Penal, operando no grupo Telegram Swd hermes. "
    "Responda de forma CONCISA, formatada para Telegram mobile (Markdown simples, sem blocos gigantes). "
    "Processos do Júlio Pereira Marcos: 0023013-51.2021.8.19.0078 (Búzios 2ª Vara), "
    "HC TJRJ 0029845-67.2026.8.19.0000, STJ HC 1.116.750/RJ. Use memória memU quando útil."
)


def _external_key():
    # Não use valores default hardcoded — venha do .env quando houver integração suportada.
    return os.environ.get("OPENROUTER_API_KEY", "").strip()


def call_cc(prompt: str, timeout: int = 60) -> str:
    # Modo IA do Telegram desativado até haver integração oficial do Command Code.
    # Retorna mensagem legível em vez de falhar silenciosamente ou expor segredos.
    key = _external_key()
    if not key:
        return "(modo IA do Telegram desativado — use /check, /status, /djen, /exec; configure integração oficial para /run)"
    payload = json.dumps({
        "model": CC_MODEL,
        "messages": [
            {"role": "system", "content": CC_SYSTEM},
            {"role": "user", "content": prompt[:8000]},
        ],
        "max_tokens": 1800,
        "temperature": 0.4,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "HTTP-Referer": "https://superjus.local", "X-Title": "superJus-telegram"},
    )
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout) as resp:
        data = json.loads(resp.read().decode())
    choices = data.get("choices") or []
    if choices:
        return (choices[0].get("message", {}).get("content") or "").strip() or "(sem resposta)"
    return json.dumps(data, ensure_ascii=False)[:1500]


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def telegram_api(token, method, payload=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as resp:
        return json.loads(resp.read().decode())


def tg_send(token, chat_id, text):
    # Telegram limita 4096 chars; corta
    for chunk in [text[i:i+3800] for i in range(0, len(text), 3800)] or ["(vazio)"]:
        telegram_api(token, "sendMessage", {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown", "disable_web_page_preview": True})


def set_commands(token):
    cmds = [
        {"command": "help", "description": "Lista comandos disponíveis"},
        {"command": "check", "description": "Checa TJRJ/DataJud agora (4 processos Júlio)"},
        {"command": "status", "description": "Última checagem, cron e memória"},
        {"command": "djen", "description": "Consulta DJEN STJ (HC 1.116.750)"},
        {"command": "run", "description": "Roda prompt livre no Command Code"},
        {"command": "exec", "description": "Executa comando shell (whitelist)"},
    ]
    return telegram_api(token, "setMyCommands", {"commands": cmds})


def build_help():
    return (
        "📱 *Swed — atalhos*\n"
        "`/check` → consulta TJRJ agora\n"
        "`/status` → última checagem\n"
        "`/djen` → DJEN STJ (HC 1.116.750)\n"
        "`/run <texto>` → manda pro Command Code\n"
        "`/exec <cmd>` → shell (whitelist)\n"
        "_Dica: toque e segure o comando acima p/ enviar_"
    )


def do_status():
    state = {}
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception as e:
            return f"Erro lendo estado: {e}"
    t = datetime.now().strftime("%d/%m %H:%M")
    linhas = [f"📊 *JÚLIO — status* · {t}"]
    if not state or all(k.startswith("_") for k in state):
        linhas.append("_Sem checagens ainda. Use /check_")
    else:
        linhas.append(f"Última: `{state.get('_ultima_checagem','?')}`")
        for k, v in state.items():
            if k.startswith("_"):
                continue
            curto = k.replace("-51.2021.8.19.0078","").replace("-67.2026.8.19.0000","").replace("-87.2024.8.19.0078","").replace("-39.2021.8.19.0078","")
            linhas.append(f"• `{curto}` → _{v.get('resumo','')[:70]}_")
    linhas.append("\n`cron 30min` · `bridge on`")
    return "\n".join(linhas)


def do_check():
    """Roda o monitor em modo --force mas só devolve resumo (não duplica envio cron). Usa subprocess."""
    py = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
    mon = os.path.join(os.path.dirname(__file__), "telegram_monitor_julio.py")
    try:
        res = subprocess.run([py, "-X", "utf8", mon, "--force"], capture_output=True, text=True, timeout=180)
        out = (res.stdout or "") + (res.stderr or "")
        return out[-3500:] or "(sem saída)"
    except subprocess.TimeoutExpired:
        return "Timeout após 180s (TJRJ lento). O cron tenta de novo em 30 min."
    except Exception as e:
        return f"Erro: {e}"


def whitelist_exec(cmd):
    allowed_prefixes = (
        "git ", "dir ", "ls ", "cat ", "type ",
        "python -X utf8 scripts/", "python scripts/",
        "hermes ", "cmd /c dir",
    )
    blocked = ("rm ", "del ", "shutdown", "reboot", "curl ", "wget ", "nc ", "ncat", "powershell -enc", "Invoke-")
    low = cmd.lower().strip()
    if any(b in low for b in blocked):
        return None, "Comando bloqueado por política."
    if not any(low.startswith(p) for p in allowed_prefixes) and low not in ("help", "pwd"):
        return None, f"Prefixo não permitido. Permitidos: {', '.join(allowed_prefixes)}"
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, cwd=r"C:\Projetos\superJus")
        out = (res.stdout or "") + (res.stderr or "")
        return res.returncode, out[-3500:]
    except subprocess.TimeoutExpired:
        return None, "Timeout 60s."
    except Exception as e:
        return None, str(e)


def handle_message(token, chat_id, text, from_user):
    # também aceita fallback CC: mensagem sem "/" no grupo permitido vira pergunta à IA
    raw = (text or "").strip()
    if not raw:
        return
    if not raw.startswith("/"):
        # conversa livre → responde com a IA do Command Code
        try:
            tg_send(token, chat_id, f"🤖 _{call_cc(raw)[:3500]}_")
        except Exception as e:
            tg_send(token, chat_id, f"Erro IA: {e}")
        return
    parts = raw.split(maxsplit=1)
    cmd = parts[0].lstrip("/").split("@")[0].lower()
    arg = parts[1] if len(parts) > 1 else ""
    text = raw
    if cmd not in ALLOWED_CMDS:
        tg_send(token, chat_id, f"Desconhecido `/{cmd}` → /help")
        return
    if cmd == "help":
        tg_send(token, chat_id, build_help())
    elif cmd == "status":
        tg_send(token, chat_id, do_status())
    elif cmd == "check":
        tg_send(token, chat_id, "⏳ _checando TJRJ..._")
        raw = do_check()
        # compacta se veio o dump verboso do monitor
        if "Checando" in raw and "NOVIDADE" in raw:
            raw = raw.replace("Checando", "•").replace("NOVIDADE:", "→")
        tg_send(token, chat_id, raw[:3500] or "(sem saída)")
    elif cmd == "djen":
        tg_send(token, chat_id, "_Tentando DJEN (STJ HC 1.116.750) — depende da rota BR..._")
        try:
            py = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"
            p = os.path.join(os.path.dirname(__file__), "djen_consulta_hc_stj.py")
            res = subprocess.run([py, "-X", "utf8", p], capture_output=True, text=True, timeout=90)
            out = (res.stdout or res.stderr or "")[-3500:]
            tg_send(token, chat_id, out or "(sem saída)")
        except Exception as e:
            tg_send(token, chat_id, f"Erro DJEN: {e}")
    elif cmd == "run":
        if not arg:
            tg_send(token, chat_id, "Uso: `/run <sua instrução>`")
            return
        tg_send(token, chat_id, "⏳ _processando..._")
        try:
            tg_send(token, chat_id, call_cc(arg)[:3800])
        except Exception as e:
            tg_send(token, chat_id, f"Erro: {e}")
    elif cmd == "exec":
        if not arg:
            tg_send(token, chat_id, "Uso: `/exec <comando>` (whitelist)")
            return
        code, out = whitelist_exec(arg)
        tg_send(token, chat_id, f"*exit {code}*\n```\n{out[:3500]}\n```")
    elif cmd == "ocr":
        tg_send(token, chat_id, "Envie o PDF como documento junto de `/ocr` ou use o fluxo DJERJ já configurado.")


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="processa pendentes e sai")
    ap.add_argument("--set-commands", action="store_true")
    ap.add_argument("--offset", type=int, default=None)
    args = ap.parse_args()

    cfg = load_config()
    token = cfg.get("bot_token", "").strip()
    allowed = str(cfg.get("chat_id", "")).strip()
    if not token:
        print("bot_token faltando em telegram_config.json")
        sys.exit(1)

    if args.set_commands:
        print(json.dumps(set_commands(token), ensure_ascii=False, indent=2))
        return

    # long polling
    offset = args.offset
    # tenta retomar offset salvo
    off_file = os.path.join(os.path.dirname(__file__), "..", ".agents", "telegram_bridge_offset.txt")
    if offset is None and os.path.exists(off_file):
        try:
            offset = int(open(off_file, "r", encoding="utf-8").read().strip())
        except Exception:
            offset = None

    print(f"Bridge Telegram → Command Code | bot=@Swedxbot chat={allowed} offset={offset}")
    if args.once:
        data = telegram_api(token, "getUpdates", {"offset": offset, "timeout": 5})
        for upd in data.get("result", []):
            msg = upd.get("message") or upd.get("channel_post") or {}
            chat = msg.get("chat", {})
            if str(chat.get("id")) != allowed:
                continue
            handle_message(token, allowed, msg.get("text", ""), msg.get("from", {}))
            offset = upd["update_id"] + 1
        if offset is not None:
            open(off_file, "w", encoding="utf-8").write(str(offset))
        return

    # loop
    while True:
        try:
            data = telegram_api(token, "getUpdates", {"offset": offset, "timeout": 25})
            for upd in data.get("result", []):
                msg = upd.get("message") or upd.get("channel_post") or {}
                chat = msg.get("chat", {})
                # em grupo, só processa se vier do chat permitido
                if str(chat.get("id")) != allowed:
                    offset = upd["update_id"] + 1
                    continue
                text = msg.get("text", "")
                if text and text.startswith("/"):
                    handle_message(token, allowed, text, msg.get("from", {}))
                offset = upd["update_id"] + 1
                open(off_file, "w", encoding="utf-8").write(str(offset))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[loop] {e}", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()
