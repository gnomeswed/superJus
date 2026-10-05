# -*- coding: utf-8 -*-
"""
SUPERJUS — TESTE DE DISPARO DE ALERTA DE NOVIDADES NO TELEGRAM (JÚLIO PEREIRA MARCOS)
Simula a detecção de movimentações em tempo real no STJ e na 1ª Vara de Búzios.
"""

import sys, json, ssl, urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

BOT_TOKEN = "8831011573:AAFl2yA2C-fpczLIdMi3iQhRLQUBxCsBnIw"
CHAT_ID = "-5578464034"

agora_str = datetime.now().strftime("%d/%m/%Y às %H:%M")

msg = f"""🚨 *SUPERJUS — NOVIDADES NO PROCESSO DE JÚLIO PEREIRA MARCOS*
📅 _Varredura das 10h realizada em: {agora_str}_

🏛️ *STJ — 6ª Turma (Brasília)*
📂 *Processo:* `HC 1.116.750/RJ (2026/0311210-7)`
⚡ *Nova Movimentação:* `Conclusão ao Gabinete do Relator Min. Og Fernandes`
📝 *Detalhe:* Parecer do Ministério Público Federal (MPF) protocolado e concluso para decisão monocrática de mérito.

───────────────────────

🏛️ *1ª Vara da Comarca de Armação dos Búzios*
📂 *Processo:* `0023013-51.2021.8.19.0078`
⚡ *Nova Movimentação:* `Juntada de Carta Precatória / Despacho Cartorário`
📝 *Detalhe:* Autos encaminhados para cumprimento de diligência e preparação de pauta de Audiência de Instrução e Julgamento (AIJ).

───────────────────────

🎯 *Próxima Ação Estratégica da Defesa:*
• Protocolo e despacho dos *Memoriais Executivos de 2 Páginas* com a assessoria do Min. Og Fernandes focando no Art. 580 do CPP (Isonomia com Matheus) e Excesso de Prazo da Prisão.

⚖️ _SuperJus Intelligence • Monitor Diário Automatizado_"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = json.dumps({
    "chat_id": CHAT_ID,
    "text": msg,
    "parse_mode": "Markdown",
    "disable_web_page_preview": True
}).encode("utf-8")

req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
ctx = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("ok"):
            print("✅ TESTE ENVIADO COM SUCESSO AO TELEGRAM!")
            print(f"Chat ID: {CHAT_ID}")
            print(f"Message ID: {res['result']['message_id']}")
        else:
            print(f"Erro Telegram: {res}")
except Exception as e:
    print(f"Erro ao disparar: {e}")
