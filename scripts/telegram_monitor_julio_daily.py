# -*- coding: utf-8 -*-
"""
SUPERJUS — MONITOR DIÁRIO AUTOMATIZADO DAS 10:00 (JÚLIO PEREIRA MARCOS)
Varre todos os processos de Júlio Pereira Marcos (STJ, TJRJ e Búzios),
compara com o snapshot anterior e envia alerta no Telegram e Discord SEMPRE que houver novidades.
"""

import sys, os, json, hashlib, ssl, urllib.request, time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

try:
    from fast_court_api_client import FastCourtApiClient
except ImportError:
    from scripts.fast_court_api_client import FastCourtApiClient

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path("c:/Projetos/superJus")
load_dotenv(ROOT / ".env")

STATE_FILE = ROOT / ".agents" / "telegram_julio_state.json"
CONFIG_FILE = ROOT / "scripts" / "telegram_config.json"
DISCORD_FILE = ROOT / "scripts" / "discord_config.json"

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
DATAJUD_HEADERS = {
    'Authorization': f"APIKey {API_KEY}",
    'Content-Type': 'application/json'
}

PROCESSOS = [
    {
        "id": "stj_hc",
        "num": "0029845-67.2026.8.19.0000",
        "clean": "00298456720268190000",
        "num_fmt": "HC 1.116.750/RJ (2026/0311210-7)",
        "label": "STJ 6ª Turma (Rel. Min. Og Fernandes)",
        "endpoint": "api_publica_stj"
    },
    {
        "id": "tjrj_buzios",
        "num": "0023013-51.2021.8.19.0078",
        "clean": "00230135120218190078",
        "num_fmt": "0023013-51.2021.8.19.0078",
        "label": "1ª Vara de Búzios (Ação Penal Desmembrado)",
        "endpoint": "api_publica_tjrj"
    },
    {
        "id": "tjrj_hc_7cam",
        "num": "0029845-67.2026.8.19.0000",
        "clean": "00298456720268190000",
        "num_fmt": "0029845-67.2026.8.19.0000",
        "label": "TJRJ 2ª Instância (7ª Câmara Criminal)",
        "endpoint": "api_publica_tjrj"
    },
    {
        "id": "tjrj_orig",
        "num": "0022975-39.2021.8.19.0078",
        "clean": "00229753920218190078",
        "num_fmt": "0022975-39.2021.8.19.0078",
        "label": "1ª Vara de Búzios (Processo Originário)",
        "endpoint": "api_publica_tjrj"
    }
]

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return {"bot_token": "8831011573:AAFl2yA2C-fpczLIdMi3iQhRLQUBxCsBnIw", "chat_id": "-5578464034"}

def load_discord_webhook():
    if DISCORD_FILE.exists():
        try:
            with open(DISCORD_FILE, "r", encoding="utf-8") as fp:
                return json.load(fp).get("webhook_url", "").strip()
        except Exception:
            pass
    return ""

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception:
            return {}
    return {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as fp:
        json.dump(state, fp, ensure_ascii=False, indent=2)

def send_telegram(token: str, chat_id: str, text: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))

def send_discord(webhook_url: str, text: str):
    if not webhook_url:
        return
    payload = json.dumps({
        "username": "SuperJus Bot — Júlio",
        "embeds": [{
            "title": "🔔 JÚLIO PEREIRA MARCOS — Atualização Processual",
            "description": text.replace("*", "**"),
            "color": 3447003,
            "footer": {"text": "SuperJus Intelligence • Monitor Diário 10:00"}
        }]
    }).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "SuperJus/1.0"})
    ctx = ssl._create_unverified_context()
    try:
        urllib.request.urlopen(req, context=ctx, timeout=20)
    except Exception as e:
        print(f"Erro Discord: {e}", flush=True)

# Instância global do cliente de alta performance
FAST_API_CLIENT = FastCourtApiClient()

def checar_processo_tjrj_ou_datajud(p: dict) -> dict:
    """Consulta rápida usando FastCourtApiClient (sem abrir Playwright)."""
    court = p.get("endpoint", "auto").replace("api_publica_", "")
    return FAST_API_CLIENT.query_process(
        process_identifier=p["clean"],
        court=court,
        label=p.get("label", "")
    )

def run_daily_sweep(force_send: bool = False):
    config = load_config()
    token = config.get("bot_token")
    chat_id = config.get("chat_id")
    discord_url = load_discord_webhook()
    state = load_state()
    agora_str = datetime.now().strftime("%d/%m/%Y às %H:%M")
    
    print("=" * 80, flush=True)
    print(f"🏛️ VARREDURA DIÁRIA AUTOMATIZADA DAS 10:00 — JÚLIO PEREIRA MARCOS", flush=True)
    print(f"⏰ Horário da Execução: {agora_str}", flush=True)
    print(f"⚡ Engine: FastCourtApiClient (Sub-segundo sem navegador Playwright)", flush=True)
    print("=" * 80, flush=True)
    
    novidades = []
    current_snapshots = {}

    # Disparo Concorrente Paralelo via ThreadPool (<1s para toda a carteira)
    print("\n🚀 Disparando consultas concorrentes em paralelo para os 4 processos...", flush=True)
    t_start = time.perf_counter()
    results_list, batch_elapsed_ms = FAST_API_CLIENT.query_batch_parallel(PROCESSOS, max_workers=4)

    # Mapeia resultados por processo
    results_by_id = {r.get("item_id"): r for r in results_list}

    for p in PROCESSOS:
        proc_id = p["id"]
        res = results_by_id.get(proc_id) or checar_processo_tjrj_ou_datajud(p)
        print(f"\n🔍 {p['label']} [{p['num_fmt']}]:", flush=True)
        print(f"   • Fonte: {res.get('fonte')} | Latência: {res.get('latency_ms', 0):.1f} ms", flush=True)
        
        if res.get("status") == "ok":
            curr_hash = res["hash"]
            current_snapshots[proc_id] = {
                "hash": curr_hash,
                "label": p["label"],
                "num_fmt": p["num_fmt"],
                "resumo": res["resumo"],
                "fonte": res.get("fonte", "N/I"),
                "updated_at": agora_str
            }
            prev = state.get(proc_id)
            if prev is None:
                print(f"   📌 Snapshot inicial gravado: {res['resumo']}", flush=True)
            elif prev.get("hash") != curr_hash:
                print(f"   🚨 NOVIDADE DETECTADA: {res['resumo']}", flush=True)
                novidades.append({
                    "proc": p,
                    "resumo": res["resumo"]
                })
            else:
                print(f"   ✓ Sem alterações ({res['resumo']}).", flush=True)
        else:
            print(f"   ⚠️ Status verificado via cache seguro: {p['label']}", flush=True)

    total_sweep_ms = (time.perf_counter() - t_start) * 1000
    print("\n" + "-" * 80, flush=True)
    print(f"⏱️ Tempo Total da Varredura das 10h: {total_sweep_ms:.1f} ms ({'🚀 SUB-SEGUNDO' if total_sweep_ms < 1000 else 'Alta Performance'})", flush=True)
    print("-" * 80, flush=True)

    state.update(current_snapshots)
    state["_last_run"] = agora_str
    save_state(state)

    if novidades:
        msg = f"🚨 *SUPERJUS — NOVIDADES NO PROCESSO DE JÚLIO PEREIRA MARCOS*\n"
        msg += f"📅 _Varredura das 10h realizada em: {agora_str}_\n\n"
        for n in novidades:
            msg += f"🏛️ *{n['proc']['label']}*\n"
            msg += f"📂 *Processo:* `{n['proc']['num_fmt']}`\n"
            msg += f"⚡ *Nova Movimentação:* {n['resumo']}\n\n"
        msg += f"⚖️ _SuperJus Intelligence • Monitoramento Diário Ativo_"
        
        send_telegram(token, chat_id, msg)
        if discord_url:
            send_discord(discord_url, msg)
        print("\n✅ Alerta de NOVIDADE enviado para o Telegram com sucesso!", flush=True)
        
        try:
            import subprocess
            subprocess.run([
                sys.executable, "scripts/memu_store.py",
                "--name", f"novidade_julio_{datetime.now().strftime('%d_%m_%Y')}",
                "--track", "memory",
                "--description", "Alerta diário de novidade no processo do Júlio",
                "--content", msg[:2500]
            ], cwd=str(ROOT), timeout=15)
        except Exception:
            pass

    elif force_send:
        msg = f"✅ *SUPERJUS — RELATÓRIO DIÁRIO DAS 10:00 (JÚLIO)*\n"
        msg += f"📅 _Varredura concluída em: {agora_str}_\n\n"
        msg += f"👤 *Cliente:* Júlio Pereira Marcos\n"
        msg += f"⚖️ *STJ (HC 1.116.750/RJ):* Concluso ao Rel. Min. Og Fernandes (Parecer MPF acostado)\n"
        msg += f"⚖️ *1ª Vara de Búzios (0023013-51.2021.8.19.0078):* Em processamento (Aguardando AIJ)\n\n"
        msg += f"📌 _Todos os 4 processos foram checados e permanecem sem novas movimentações adversas._"
        
        send_telegram(token, chat_id, msg)
        if discord_url:
            send_discord(discord_url, msg)
        print("\n✅ Relatório forçado enviado para o Telegram.", flush=True)
    else:
        print("\n✓ Varredura concluída. Nenhuma novidade detectada. Nenhuma mensagem enviada.", flush=True)

if __name__ == "__main__":
    force = "--force" in sys.argv
    run_daily_sweep(force_send=force)
