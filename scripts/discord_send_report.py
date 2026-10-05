# -*- coding: utf-8 -*-
"""
Envia relatório formatado em Rich Embed para o Discord via Webhook.

Uso:
  python scripts/discord_send_report.py
  python scripts/discord_send_report.py --url "https://discord.com/api/webhooks/..."
"""
import sys
import os
import json
import ssl
import urllib.request
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "discord_config.json")
SSL_CTX = ssl._create_unverified_context()

def load_webhook_url():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("webhook_url", "").strip()
        except Exception:
            pass
    return ""

def send_discord_report(webhook_url=None):
    url = webhook_url or load_webhook_url()
    if not url:
        print("ERRO: Webhook URL do Discord não encontrado em scripts/discord_config.json")
        print("Forneça o URL via comando ou salve em scripts/discord_config.json")
        sys.exit(1)

    agora = datetime.utcnow().isoformat() + "Z"
    agora_br = datetime.now().strftime("%d/%m/%Y às %H:%M BRT")

    embed = {
        "title": "📢 RELATÓRIO ATUALIZADO — JÚLIO PEREIRA MARCOS",
        "description": f"Acompanhamento processual em tempo real • *{agora_br}*",
        "color": 3447003, # Azul elegante
        "fields": [
            {
                "name": "⚖️ 1ª Instância — 2ª Vara Criminal de Búzios",
                "value": (
                    "**Processo:** `0023013-51.2021.8.19.0078`\n"
                    "**Status/Localização:** `Processamento`\n"
                    "**Última Juntada:** 04/08/2026 (Juntada - Documento)\n"
                    "**Recebimento da Conclusão:** 01/08/2026\n"
                    "**Situação Prática:** Despacho proferido pelo Juiz Dr. Danilo Marques Borges. "
                    "Cartório elaborando expedientes (mandados/ofícios) para publicação no DJERJ (24h a 72h úteis)."
                ),
                "inline": False
            },
            {
                "name": "🏛️ 3ª Instância — Superior Tribunal de Justiça (STJ)",
                "value": (
                    "**Processo:** `HC 1.116.750 / RJ` (2026/0311210-7)\n"
                    "**Relator:** Min. Og Fernandes (6ª Turma)\n"
                    "**Situação:** Informações oficiais prestadas pelo TJRJ (31/07). Autos remetidos ao MPF.\n"
                    "**Parecer MPF:** Aguardado entre 10/08 e 14/08/2026.\n"
                    "**Julgamento de Mérito:** Previsto para a 2ª quinzena de agosto."
                ),
                "inline": False
            },
            {
                "name": "🛡️ Pilares Defensivos Ativos",
                "value": (
                    "1. **Isonomia (Art. 580 CPP):** 5 corréus respondem em liberdade desde ago/2022.\n"
                    "2. **Ausência de Materialidade:** Nenhuma droga apreendida com Júlio.\n"
                    "3. **Excesso de Prazo:** Preso cautelarmente sem AIJ realizada."
                ),
                "inline": False
            }
        ],
        "footer": {
            "text": "SuperJus • Analista Jurídico Criminal"
        },
        "timestamp": agora
    }

    payload = json.dumps({
        "username": "SuperJus Bot",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "embeds": [embed]
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SuperJus-DiscordBot/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=20) as resp:
            print("SUCESSO: Relatório enviado para o Discord com sucesso!")
            return True
    except Exception as e:
        print(f"ERRO ao enviar para o Discord: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Envia relatório do Júlio para o Discord")
    parser.add_argument("--url", help="URL do Webhook do Discord")
    args = parser.parse_args()

    send_discord_report(args.url)

if __name__ == "__main__":
    main()
