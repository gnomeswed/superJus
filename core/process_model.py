# -*- coding: utf-8 -*-
from __future__ import annotations
import hashlib
import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

TZ = "America/Sao_Paulo"

@dataclass
class ConsultaResult:
    processo: str
    fonte: str  # tjrj_playwright|datajud|stj|fallback|indeterminada
    status: str  # ok|partial|blocked|error
    hash_norm: str
    resumo: str
    warnings: list
    texto_bruto: str = ""

    def to_dict(self): return asdict(self)

RX_MOV = re.compile(r"(Tipo do Movimento|Última Movimentação|Data da juntada|Recebimento|Conclusão ao Juiz)[^\n]{0,160}", re.I)
RX_DATA = re.compile(r"(\d{2}/\d{2}/\d{4})")
RX_TIPO = re.compile(r"Tipo do Movimento\s*:?\s*([^\n]+)", re.I)

def normalize_movimentacoes(texto: str) -> str:
    linhas = []
    for l in texto.splitlines():
        t = l.strip()
        if not t: continue
        if "Tipo do Movimento" in t or "Data da juntada" in t or "Data da conclusão" in t or "Localização" in t:
            linhas.append(re.sub(r"\s+", " ", t)[:180])
    # fallback: tenta extrair padrão simples
    if not linhas:
        for m in RX_MOV.findall(texto):
            linhas.append(re.sub(r"\s+", " ", m.strip())[:180])
    return "\n".join(linhas[:10]) or texto[:400].replace("\n"," ")

def hash_norm(norm: str) -> str:
    return hashlib.sha256(norm.encode("utf-8", "replace")).hexdigest()[:14]

def esc_md(s: str) -> str:
    return s.replace("*","\\*").replace("_","\\_").replace("[","\\[")

def state_path() -> Path:
    root = Path(__file__).resolve().parents[1]
    p = Path(os.getenv("TELEGRAM_STATE_PATH") or str(root / ".agents" / "telegram_last_state.json"))
    return p

def fmt_telegram(mudancas):
    agora = datetime.now().strftime("%d/%m %H:%M")
    linhas=[f"🔔 Júlio — {esc_md(agora)}"]
    for proc, res, ja_existia in mudancas:
        emoji = "🟢" if ja_existia else "📌"
        linhas.append(f"\n{emoji} {esc_md(proc['label'])}")
        linhas.append(f"  {esc_md(proc['num'])} → {esc_md(res.resumo[:160])}")
    return "\n".join(linhas)[:3600]
