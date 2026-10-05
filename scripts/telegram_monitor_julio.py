# -*- coding: utf-8 -*-
"""
Monitor automático dos 4 processos do Júlio Pereira Marcos.
Consulta TJRJ (1ª e 2ª instância) + DataJud e envia alerta no Telegram e Discord
quando detectar movimentação NOVA. Para uso via Command Code / Antigravity / Cron.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import os
import re
import json
import ssl
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime
from core.process_model import normalize_movimentacoes, hash_norm, ConsultaResult, fmt_telegram

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")
DISCORD_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "discord_config.json")
try:
    from core.config import STATE_FILE as _STATE_FILE  # type: ignore
    STATE_PATH = str(_STATE_FILE)
except Exception:
    STATE_PATH = os.path.join(os.path.dirname(__file__), "..", ".agents", "telegram_last_state.json")

PROCESSOS = [
    {"num": "0023013-51.2021.8.19.0078", "label": "Ação Penal - Búzios (2ª Vara)", "inst": "1"},
    {"num": "0029845-67.2026.8.19.0000", "label": "HC 7ª Câmara - TJRJ (HC 1.116.750/STJ)", "inst": "2"},
    {"num": "0001140-87.2024.8.19.0078", "label": "Execução/Medida - Búzios", "inst": "1"},
    {"num": "0022975-39.2021.8.19.0078", "label": "Processo Principal - Búzios (originário)", "inst": "1"},
]

SSL_CTX = ssl._create_unverified_context()

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_discord_webhook():
    if not os.path.exists(DISCORD_CONFIG_PATH):
        return ""
    try:
        with open(DISCORD_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("webhook_url", "").strip()
    except Exception:
        return ""

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

def telegram_send(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
        return json.loads(resp.read().decode())

def discord_send(webhook_url, text):
    if not webhook_url:
        return
    agora = datetime.utcnow().isoformat() + "Z"
    embed = {
        "title": "🔔 JÚLIO PEREIRA MARCOS — Atualização de Processo",
        "description": text.replace("*", "**"),
        "color": 3447003,
        "footer": {"text": "SuperJus • Acompanhamento Processual"},
        "timestamp": agora
    }
    payload = json.dumps({
        "username": "SuperJus Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "embeds": [embed]
    }).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "SuperJus-DiscordBot/1.0"})
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
            return resp.status
    except Exception as e:
        print(f"Erro ao enviar para Discord Webhook: {e}")

def telegram_discover(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=SSL_CTX, timeout=15) as resp:
        data = json.loads(resp.read().decode())
    results = data.get("result", [])
    chats = []
    for u in results:
        for key in ("message", "channel_post", "my_chat_member", "edited_message"):
            chat = u.get(key, {}).get("chat")
            if chat:
                chats.append(chat)
    dedup = {c["id"]: c for c in chats}
    return list(dedup.values())

def consulta_tjrj(num, inst="1"):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"erro": "playwright não instalado (use Python 3.12)"}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            ctx = browser.new_context(viewport={"width": 1280, "height": 900})
            page = ctx.new_page()
            page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", timeout=30000)
            page.wait_for_timeout(3000)
            frame = page.frame_locator("iframe#mainframe")
            frame.locator("input[name='numeroProcesso']").fill(num)
            page.wait_for_timeout(500)
            frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first.click()
            page.wait_for_timeout(6000)
            real_frame = page.query_selector("iframe#mainframe").content_frame()
            txt = real_frame.inner_text("body")[:8000]
            try:
                btn = real_frame.query_selector("text=Todos Os Movimentos")
                if btn:
                    btn.click()
                    page.wait_for_timeout(4000)
                    txt = real_frame.inner_text("body")[:12000]
            except Exception:
                pass
            browser.close()
            norm = normalize_movimentacoes(txt)
            h = hash_norm(norm)
            resumo = norm.splitlines()[0][:180] if norm else txt[:300].replace("\n"," ")
            cr = ConsultaResult(processo=num, fonte="tjrj_playwright", status="ok", hash_norm=h, resumo=resumo, texto_bruto=txt[:6000], warnings=[])
            return {"texto": txt, "hash": h, "resumo": resumo, "norm": norm, "result": cr}
    except Exception as e:
        msg = str(e).lower()
        status = "blocked" if any(k in msg for k in ["timeout","blocked","403","403","bot","captcha","cloudflare"]) else "error"
        cr = ConsultaResult(processo=num, fonte="tjrj_playwright", status=status, hash_norm="", resumo=str(e)[:200], texto_bruto=str(e), warnings=[str(e)[:260]])
        return {"erro": str(e)[:300], "status": status, "_result": cr}

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--discover", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    token = cfg.get("bot_token", "").strip()
    chat_id = cfg.get("chat_id", "")
    discord_url = load_discord_webhook()

    if not token:
        print("ERRO: bot_token não configurado em telegram_config.json")
        sys.exit(1)

    if args.discover:
        chats = telegram_discover(token)
        if not chats:
            print("Nenhum chat encontrado. Adicione @Swedxbot ao grupo/canal e envie uma mensagem, depois rode --discover novamente.")
        else:
            for c in chats:
                print(f"  id={c.get('id')} type={c.get('type')} title={c.get('title')} username=@{c.get('username')}")
        return

    if not chat_id:
        print("ERRO: chat_id não configurado.")
        sys.exit(1)

    state = load_state()
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mudancas = []

    erros=[]
    for proc in PROCESSOS:
        print(f"Checando {proc['num']} ({proc['label']}) ...")
        last_err=None
        res=None
        for attempt in range(3):
            res = consulta_tjrj(proc["num"])
            if "erro" not in res: break
            last_err=res.get("erro")
            print(f"  tentativa {attempt+1} falhou: {last_err[:120]}")
        if res is None or "erro" in res:
            status=res.get("status","error") if res else "error"
            print(f"  ERRO {status}: {last_err}")
            erros.append((proc, status, last_err))
            continue
        key = proc["num"]
        prev = state.get(key, {})
        # deduplica por hash da movimentacao normalizada
        if prev.get("hash_norm") != res["hash"]:
            mudancas.append((proc, res, prev.get("hash_norm") is not None))
            state[key] = {"hash_norm": res["hash"], "hash": res["hash"], "resumo": res["resumo"], "norm": res.get("norm","")[:600], "visto_em": agora}
            print(f"  NOVIDADE: {res['resumo'][:100]}")
        else:
            print(f"  sem novidade")

    def fmt_msg(mudancas):
        # usa formatador com md escape
        from core.process_model import esc_md
        # converte res dict para objeto simples com .resumo
        class R: pass
        lst=[]
        for proc,res,ja in mudancas:
            r=R(); r.resumo=res["resumo"]
            lst.append((proc,r,ja))
        return fmt_telegram(lst)

    if erros:
        # não mascarar erro como sem novidade
        for proc,status,msg in erros:
            print(f"  !! {proc['num']} = {status}: {msg[:160]}")
        # notifica quando o portal puder estar bloqueado/timeout
        if any(s in ("blocked","error") for _,s,_ in erros):
            warn = "⚠️ Verificação parcial — portal TJRJ com bloqueio/timeout em alguns processos. Nenhum alerta de 'sem novidade' enviado como sucesso."
            print(warn)

    if mudancas:
        save_state(state)
        msg = fmt_msg(mudancas)
        telegram_send(token, chat_id, msg)
        print(f"Enviado Telegram para {chat_id}: {len(mudancas)} novidade(s)")
        if discord_url:
            discord_send(discord_url, msg)
            print("Enviado Discord Webhook OK")
        # registra no memU sem segredos
        try:
            import subprocess as _sp
            _sp.run([sys.executable,"scripts/memu_store.py","--name",f"andamento_julio_{datetime.now().strftime('%d_%m_%Y')}.md","--track","memory","--description","Alerta Júlio (monitor 4h)","--content",msg[:2500]], cwd=str(ROOT), timeout=20)
        except Exception: pass
    elif args.force:
        if erros:
            txt = f"⚠️ Júlio — verificação parcial ({agora}). {len(erros)} processo(s) com bloqueio. Cheque logs."
        else:
            txt = f"✅ Júlio — sem novidade ({agora}). {len(PROCESSOS)} processos checados."
        telegram_send(token, chat_id, txt)
        print("Envio Telegram forçado OK")
        if discord_url:
            discord_send(discord_url, txt)
            print("Envio Discord Webhook forçado OK")
    else:
        print("Sem novidades — nada enviado (use --force para testar)")

    state["_ultima_checagem"] = agora
    if erros:
        state["_ultimo_erro"] = "; ".join(f"{p['num']}:{s}" for p,s,_ in erros)[:400]
    save_state(state)

if __name__ == "__main__":
    main()
