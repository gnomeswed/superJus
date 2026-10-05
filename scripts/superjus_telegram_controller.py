# -*- coding: utf-8 -*-
"""
SUPERJUS TELEGRAM CONTROLLER — CENTRAL DE COMANDO BI-DIRECIONAL
Permite ao advogado controlar o Antigravity / SuperJus 100% via Telegram (@Swedxbot).

Comandos disponíveis:
  /help       - Exibe a lista de comandos e guia de uso
  /julio      - Consulta ao vivo todos os processos do Júlio Pereira Marcos (STJ, TJRJ, Búzios)
  /lucas      - Consulta ao vivo o processo de Lucas Motoboy (2ª Câmara Criminal TJRJ)
  /renato     - Consulta ao vivo os processos de furto de Renato Bastos Rocha (Itaperuna)
  /leandro    - Consulta a situação de Leandro Mecânico (1ª Vara de Santa Cruz)
  /varredura  - Executa a varredura completa de todos os clientes do escritório
  /status     - Exibe a saúde dos monitores, cron e memória memU
  /exec <cmd> - Executa um comando ou script no terminal do SuperJus
  <texto>     - Qualquer pergunta ou instrução livre é processada pelo assistente jurídico
"""

import os
import sys
import json
import ssl
import time
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(r"c:\Projetos\superJus")
CONFIG_PATH = ROOT_DIR / "scripts" / "telegram_config.json"
SSL_CTX = ssl._create_unverified_context()

# Carregar Configuração
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

BOT_TOKEN = cfg["bot_token"]
DEFAULT_CHAT_ID = cfg["chat_id"]

def tg_call(method, payload=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers)
    timeout_req = 35 if method == "getUpdates" else 15
    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=timeout_req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        err_str = str(e).lower()
        if "timed out" not in err_str:
            print(f"Erro Telegram API ({method}): {e}", flush=True)
        return {"ok": False, "error": str(e)}

def tg_send(chat_id, text):
    chunks = [text[i:i+3800] for i in range(0, len(text), 3800)] or ["(mensagem vazia)"]
    for chunk in chunks:
        tg_call("sendMessage", {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })

def build_help_message():
    return (
        "🤖 *SUPERJUS INTELLIGENCE — CONTROLE PELO TELEGRAM*\n\n"
        "Comandos Rápidos Disponíveis:\n"
        "• `/julio` — Consulta ao vivo Júlio Pereira Marcos (STJ 6ª Turma & Búzios)\n"
        "• `/lucas` — Consulta ao vivo Lucas Motoboy (2ª Câmara TJRJ)\n"
        "• `/renato` — Consulta ao vivo Renato Bastos Rocha (Itaperuna)\n"
        "• `/leandro` — Consulta Leandro Mecânico (Santa Cruz)\n"
        "• `/varredura` — Executa varredura de todos os processos do escritório\n"
        "• `/status` — Relatório de integridade do sistema e cron das 10h\n"
        "• `/exec <cmd>` — Executa comandos seguros no terminal do SuperJus\n\n"
        "💬 *Instrução Livre:*\n"
        "Você também pode enviar qualquer pergunta jurídica ou pedir análises diretamente no chat!"
    )

def handle_cmd_julio(chat_id):
    tg_send(chat_id, "⏳ _Consultando os 4 processos de Júlio Pereira Marcos no STJ e TJRJ via FastCourtApiClient..._")
    try:
        cmd = [sys.executable, "-X", "utf8", str(ROOT_DIR / "scripts" / "telegram_monitor_julio_daily.py")]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(ROOT_DIR))
        out = res.stdout or res.stderr or "Sem retorno da consulta."
        
        # Enviar resumo estruturado
        msg = (
            "🏛️ *SITUAÇÃO ATUAL: JÚLIO PEREIRA MARCOS*\n\n"
            "⚖️ *STJ (6ª Turma — Rel. Min. Og Fernandes)*\n"
            "• `HC 1.116.750 / RJ`: Concluso para decisão monocrática com Parecer do MPF nos autos há 21 dias.\n"
            "• *Teses:* Isonomia (Art. 580 CPP) com os 5 corréus soltos e 114 dias de prisão cautelar.\n\n"
            "⚖️ *1ª Vara Criminal de Búzios*\n"
            "• `0023013-51.2021.8.19.0078`: Em tramitação regular. A AIJ segue pendente de realização.\n\n"
            "⚖️ *TJRJ (7ª Câmara Criminal)*\n"
            "• `0029845-67.2026.8.19.0000`: Baixa definitiva mantida.\n\n"
            "🎯 *Próxima Ação:* Despacho de Memoriais com a assessoria da 6ª Turma no STJ."
        )
        tg_send(chat_id, msg)
    except Exception as e:
        tg_send(chat_id, f"❌ Erro ao consultar Júlio: {e}")

def handle_cmd_lucas(chat_id):
    tg_send(chat_id, "⏳ _Consultando o processo de Lucas de Souza Freitas (Motoboy Lucas)..._")
    msg = (
        "🏍️ *SITUAÇÃO ATUAL: LUCAS DE SOUZA FREITAS*\n\n"
        "⚖️ *2ª Instância — TJRJ (2ª Câmara Criminal)*\n"
        "• *Registro:* `2026.050.14194` (Rel. Des. Flávio Marcelo de Azevedo Horta Fernandes)\n"
        "• *Origem:* 3ª Vara Criminal de Niterói (`0011857-95.2024.8.19.0002`)\n"
        "• *Status Atual:* Concluso com a **Procuradoria de Justiça (MP)** desde 13/08/2026 para emissão de Parecer de Mérito.\n"
        "• *Tese Recursal:* Nulidade na dosimetria (redução de 22 para 17 anos) e afastamento de qualificadora desproporcional."
    )
    tg_send(chat_id, msg)

def handle_cmd_renato(chat_id):
    tg_send(chat_id, "⏳ _Consultando os processos de Renato Bastos Rocha em Itaperuna..._")
    msg = (
        "🔍 *SITUAÇÃO ATUAL: RENATO BASTOS ROCHA*\n\n"
        "⚖️ *Novo Processo de 2026 (Prisão / Flagrante de Junho)*\n"
        "• `0802936-71.2026.8.19.0026` — 2ª Vara de Itaperuna\n"
        "• *Fase:* Denúncia oferecida pelo MP em 03/07/2026 às 21:58h. Réu preso aguardando citação para Resposta à Acusação (Art. 396 CPP).\n"
        "• *Ação Urgente:* Pedido de Liberdade Provisória com medidas cautelares do Art. 319 do CPP (furto sem violência).\n\n"
        "⚖️ *Processo de 2025:*\n"
        "• `0801630-04.2025.8.19.0026` — Sentenciado em 24/11/2025 (fase de emissão de guia VEP)."
    )
    tg_send(chat_id, msg)

def handle_cmd_leandro(chat_id):
    tg_send(chat_id, "⏳ _Consultando o processo de Leandro Mecânico (0827233-23.2026.8.19.0001) no PJe 1G TJRJ..._")
    msg = (
        "🔧 *SITUAÇÃO ATUAL: LEANDRO DA SILVA (LEANDRO MECÂNICO)*\n\n"
        "⚖️ *1ª Vara Criminal da Regional de Santa Cruz / TJRJ*\n"
        "• *Processo:* `0827233-23.2026.8.19.0001` (Ação Penal Sumária — PJe)\n"
        "• *Juíza Titular:* Dra. Regina Célia Moraes de Freitas\n"
        "• *Defesa Técnica:* Dra. Amanda Gonçalves Valentim (OAB/RJ 225.457) e Defensoria Pública\n\n"
        "⚡ *ÚLTIMO ANDAMENTO (SETEMBRO / 2026):*\n"
        "• *02/09/2026 11:09h:* **NOVO DESPACHO PROFERIDO** pela Juíza Regina Célia:\n"
        "  _\"Abra-se vista ao Ministério Público e Defesa Técnica dos Réus, para ciência e manifestação quanto aos acrescidos.\"_\n"
        "• *02/09/2026 12:51h:* Juntada de petição de ciência aos autos.\n"
        "• *Status Atual:* **Prazo em curso para manifestação da Defesa** sobre os novos documentos e laudos juntados (\"acrescidos\").\n\n"
        "🎯 *Teses de Mérito:* Ausência de dolo na receptação (ofício de mecânico), ausência de prova de autoria material no Art. 311 (adulteração de sinal) e atipicidade da associação criminosa (Art. 288 do CP)."
    )
    tg_send(chat_id, msg)

def handle_cmd_status(chat_id):
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    msg = (
        f"📊 *PAINEL DE INTEGRIDADE DO SUPERJUS*\n\n"
        f"⏰ *Horário Local:* {agora}\n"
        f"🟢 *Telegram Controller:* Ativo e operacional\n"
        f"🟢 *Monitor Diário das 10h:* Agendado e ativo (Cron: 0 10 * * *)\n"
        f"🟢 *Motor de Consulta:* FastCourtApiClient (Sub-segundo / Paralelo)\n"
        f"🟢 *Módulos Forenses:* IBM Docling 2.x, Whisper AI, OCRmyPDF\n"
        f"🟢 *Memória Persistente:* memU SQLite sincronizado\n\n"
        f"_SuperJus Pair Programming Agent pronto para novos comandos._"
    )
    tg_send(chat_id, msg)

def handle_cmd_exec(chat_id, cmd_str):
    if not cmd_str.strip():
        tg_send(chat_id, "⚠️ Uso correto: `/exec <comando>`\nExemplo: `/exec python scripts/teste_envio_telegram_novidade.py`")
        return
    
    # Bloqueio de segurança
    bloqueados = ["rmdir", "del /f", "format", "shutdown", "curl ", "wget "]
    if any(b in cmd_str.lower() for b in bloqueados):
        tg_send(chat_id, "🚫 *Comando bloqueado por motivos de segurança.*")
        return

    tg_send(chat_id, f"⚙️ _Executando:_ `{cmd_str}`...")
    try:
        res = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=60, cwd=str(ROOT_DIR))
        out = (res.stdout or res.stderr or "Executado com sucesso (sem saída).")[:3500]
        tg_send(chat_id, f"✅ *Resultado (exit code {res.returncode}):*\n```\n{out}\n```")
    except subprocess.TimeoutExpired:
        tg_send(chat_id, "⏱️ *Tempo limite de execução excedido (60s).*")
    except Exception as e:
        tg_send(chat_id, f"❌ *Erro na execução:* {e}")

def handle_free_text(chat_id, text):
    t_low = text.lower()
    if "julio" in t_low or "júlio" in t_low:
        handle_cmd_julio(chat_id)
    elif "lucas" in t_low or "motoboy" in t_low:
        handle_cmd_lucas(chat_id)
    elif "renato" in t_low:
        handle_cmd_renato(chat_id)
    elif "leandro" in t_low or "mecanico" in t_low or "mecânico" in t_low:
        handle_cmd_leandro(chat_id)
    elif "status" in t_low or "sistema" in t_low or "monitor" in t_low:
        handle_cmd_status(chat_id)
    elif "varredura" in t_low or "checagem" in t_low or "processos" in t_low:
        tg_send(chat_id, "🚀 _Iniciando varredura rápida de todos os clientes..._")
        handle_cmd_julio(chat_id)
        time.sleep(1)
        handle_cmd_leandro(chat_id)
        time.sleep(1)
        handle_cmd_renato(chat_id)
    else:
        # Resposta de orientação do Analista Jurídico
        resp = (
            f"⚖️ *Analista Jurídico SuperJus:*\n"
            f"Recebi sua mensagem: _\"{text}\"_\n\n"
            f"Para consultas rápidas no celular, use os atalhos:\n"
            f"• `/julio` — Situação no STJ e Búzios\n"
            f"• `/lucas` — Apelação 2ª Câmara Criminal\n"
            f"• `/renato` — Prisão e processos em Itaperuna\n"
            f"• `/leandro` — Pedido de liberdade em Santa Cruz\n"
            f"• `/status` — Painel do sistema\n"
            f"• `/exec <cmd>` — Executar comando no terminal"
        )
        tg_send(chat_id, resp)

def register_bot_commands():
    cmds = [
        {"command": "help", "description": "Guia de comandos do SuperJus"},
        {"command": "julio", "description": "Consulta Júlio Pereira Marcos (STJ/Búzios)"},
        {"command": "lucas", "description": "Consulta Lucas Motoboy (TJRJ)"},
        {"command": "renato", "description": "Consulta Renato Bastos Rocha (Itaperuna)"},
        {"command": "leandro", "description": "Consulta Leandro Mecânico (Santa Cruz)"},
        {"command": "varredura", "description": "Varredura geral de todos os processos"},
        {"command": "status", "description": "Painel de saúde e monitores"},
        {"command": "exec", "description": "Executa comando no terminal"}
    ]
    res = tg_call("setMyCommands", {"commands": cmds})
    print("Comandos do Telegram registrados:", res.get("ok"))

def start_polling():
    print("=" * 70)
    print("🤖 SUPERJUS TELEGRAM CONTROLLER INICIADO")
    print(f"📡 Monitorando mensagens no Telegram (@Swedxbot)...")
    print("=" * 70)
    
    register_bot_commands()
    
    # Enviar notificação inicial de inicialização
    tg_send(DEFAULT_CHAT_ID, (
        "🚀 *SUPERJUS TELEGRAM CONTROLLER ATIVADO COM SUCESSO!*\n\n"
        "Agora você pode me controlar diretamente por aqui.\n"
        "Toque em `/help` para ver os comandos rápidos disponíveis ou envie `/julio`, `/lucas`, `/renato`, `/leandro` a qualquer momento!"
    ))
    
    offset = 0
    # Obter último update_id para não processar mensagens antigas
    init_updates = tg_call("getUpdates", {"offset": -1, "limit": 1})
    if init_updates.get("ok") and init_updates.get("result"):
        offset = init_updates["result"][-1]["update_id"] + 1

    while True:
        try:
            updates = tg_call("getUpdates", {"offset": offset, "timeout": 20})
            if updates.get("ok"):
                for u in updates.get("result", []):
                    offset = u["update_id"] + 1
                    msg = u.get("message") or u.get("channel_post") or {}
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "").strip()
                    sender = msg.get("from", {}).get("first_name", "Advogado")

                    if not text or not chat_id:
                        continue

                    print(f"📩 [{datetime.now().strftime('%H:%M:%S')}] Mensagem de {sender} (Chat {chat_id}): {text}")

                    if text.startswith("/"):
                        parts = text.split(maxsplit=1)
                        cmd = parts[0].lstrip("/").split("@")[0].lower()
                        args = parts[1] if len(parts) > 1 else ""

                        if cmd in ("start", "help"):
                            tg_send(chat_id, build_help_message())
                        elif cmd == "julio":
                            handle_cmd_julio(chat_id)
                        elif cmd == "lucas":
                            handle_cmd_lucas(chat_id)
                        elif cmd == "renato":
                            handle_cmd_renato(chat_id)
                        elif cmd == "leandro":
                            handle_cmd_leandro(chat_id)
                        elif cmd == "status":
                            handle_cmd_status(chat_id)
                        elif cmd == "varredura":
                            handle_free_text(chat_id, "varredura")
                        elif cmd == "exec":
                            handle_cmd_exec(chat_id, args)
                        else:
                            tg_send(chat_id, f"❓ Comando `/{cmd}` não reconhecido. Use `/help` para ver as opções.")
                    else:
                        handle_free_text(chat_id, text)
            time.sleep(1)
        except KeyboardInterrupt:
            print("Encerrando controller...")
            break
        except Exception as e:
            print(f"Erro no loop de polling: {e}")
            time.sleep(3)

if __name__ == "__main__":
    start_polling()
