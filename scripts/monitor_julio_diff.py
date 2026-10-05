#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor Julio Pereira Marcos — diff-aware wrapper.
Rodado pelo cron 3x/dia. Salva snapshot atual, compara com anterior,
e imprime relatório AMIGÁVEL para Telegram (sem tabelas | nem blocos ``` gigantes).
"""
import re, hashlib
from pathlib import Path
from datetime import datetime

BASE = Path("C:/Projetos/superJus")
SNAP_DIR = BASE / "tmp_julio_snaps"
SNAP_DIR.mkdir(parents=True, exist_ok=True)

LIVE_TXT = BASE / "julio_verificacao_14h_06_08_2026.txt"
LATEST_SNAP = SNAP_DIR / "latest.txt"
SNAP_HASH_FILE = SNAP_DIR / "latest.hash"

FIELDS = {
    "localizacao": re.compile(r"Localiza[cç][aã]o na Serventia\s*(.+?)\s*Dados dos Personagens", re.I | re.S),
    "ult_mov_tipo": re.compile(r"Tipo do Movimento:\s*(.+)", re.I),
    "ult_mov_data": re.compile(r"Data da juntada:\s*(.+)", re.I),
    "advogados": re.compile(r"Advogado\(s\)\s*(.+?)\s*Última Movimenta", re.I | re.S),
}

def read_current_snapshot():
    if not LIVE_TXT.exists():
        return None, "Arquivo de verificação INEXISTENTE: {}".format(LIVE_TXT)
    txt = LIVE_TXT.read_text(encoding="utf-8", errors="replace")
    return txt, None

def normalize_for_hash(txt):
    t = re.sub(r"TJ/RJ\s*-\s*\d{2}/\d{2}/\d{4}\s*-\s*\d{2}:\d{2}:\d{2}", "TJ/RJ - <ts>", txt)
    t = re.sub(r"\d{2}:\d{2}:\d\ds", "<t>", t)
    return t.strip()

def clean_loc(raw):
    if not raw or raw == "—":
        return "—"
    # pega só primeira linha, limpa
    s = re.sub(r"\s+", " ", raw.strip())
    # corta em "Dados" etc já tratado pelo regex, mas garante curto
    return s[:60].strip()

def clean_field(raw):
    if not raw or raw == "—":
        return "—"
    s = re.sub(r"\s+", " ", raw.strip())
    return s[:80].strip()

def extract_fields(txt):
    out = {}
    for k, rx in FIELDS.items():
        m = rx.search(txt)
        val = m.group(1).strip()[:500] if m else "—"
        # limpa quebras
        val = re.sub(r"\s+", " ", val).strip()
        out[k] = val
    norm = normalize_for_hash(txt)
    out["full_hash"] = hashlib.sha256(norm.encode("utf-8", errors="replace")).hexdigest()[:12]
    return out

def previous_hash():
    if SNAP_HASH_FILE.exists():
        return SNAP_HASH_FILE.read_text(encoding="utf-8").strip()
    return None

def previous_text():
    if LATEST_SNAP.exists():
        return LATEST_SNAP.read_text(encoding="utf-8", errors="replace")
    return None

def build_report(current_txt, changed, cur_fields, prev_fields):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    dia_sem = ["segunda","terça","quarta","quinta","sexta","sábado","domingo"][datetime.now().weekday()]
    lines = []
    lines.append("🔔 **Júlio Pereira Marcos — Monitor de Processos**")
    lines.append(f"🕐 {now} ({dia_sem})")
    lines.append("")

    cur_loc = clean_loc(cur_fields.get("localizacao","—"))
    cur_mov = clean_field(cur_fields.get("ult_mov_tipo","—"))
    cur_data = clean_field(cur_fields.get("ult_mov_data","—"))
    cur_adv = clean_field(cur_fields.get("advogados","—"))

    prev_loc = clean_loc(prev_fields.get("localizacao","—")) if prev_fields else "—"
    prev_mov = clean_field(prev_fields.get("ult_mov_tipo","—")) if prev_fields else "—"
    prev_data = clean_field(prev_fields.get("ult_mov_data","—")) if prev_fields else "—"

    if changed:
        lines.append("⚠️ **Houve mudança nos campos monitorados**")
    else:
        lines.append("✅ **Sem mudança nos campos monitorados**")
    lines.append("")

    # Localização com destaque se mudou
    if changed and prev_loc != cur_loc and prev_loc != "—":
        lines.append(f"📍 **Localização:** {cur_loc}  ⚠️ _mudou_")
        lines.append(f"   _antes: {prev_loc}_")
    else:
        lines.append(f"📍 **Localização:** {cur_loc}")

    # Movimento
    if changed and prev_mov != cur_mov and prev_mov != "—":
        lines.append(f"📄 **Último movimento:** {cur_mov}  ⚠️ _mudou_")
        lines.append(f"   _antes: {prev_mov}_")
    else:
        lines.append(f"📄 **Último movimento:** {cur_mov}")

    # Data
    if changed and prev_data != cur_data and prev_data != "—":
        lines.append(f"📅 **Data da juntada:** {cur_data}  ⚠️ _mudou_")
        lines.append(f"   _antes: {prev_data}_")
    else:
        lines.append(f"📅 **Data da juntada:** {cur_data}")

    lines.append("")
    lines.append("⚖️ **Processos acompanhados:**")
    lines.append("• `0023013-51.2021.8.19.0078` — Búzios 2ª Vara Criminal (Ação Penal Art.33)")
    lines.append("• `0029845-67.2026.8.19.0000` — TJRJ 7ª Câmara Criminal (HC / ROC)")
    lines.append("")

    # Advogados resumido
    if cur_adv != "—":
        # pega só OABs
        adv_curto = cur_adv[:120]
        if len(cur_adv) > 120:
            adv_curto += "..."
        lines.append(f"👥 **Advogados:** {adv_curto}")
        lines.append("")

    # Interpretação curta e amigável
    lines.append("💡 **O que significa agora:**")
    if cur_loc == "Processamento":
        lines.append("Autos no cartório em fase de expediente — cumprindo determinação pós-decisão. Próximo passo esperado: publicação/intimação ou novo despacho. Não é nova decisão ainda.")
    elif "Retorno da Conclus" in cur_loc or "Retorno" in cur_loc:
        lines.append("Autos retornaram do gabinete do juiz para o cartório. Juiz já analisou e devolveu — cartório vai publicar/cumprir.")
    elif "Conclus" in cur_loc:
        lines.append("Autos conclusos ao juiz — aguardando decisão/despacho.")
    else:
        lines.append(f"Situação atual: {cur_loc}. Acompanhando próxima movimentação.")

    if "Juntada" in cur_mov and cur_data != "—":
        lines.append(f"Última juntada mantida em {cur_data} — sem nova movimentação desde então.")

    lines.append("")
    lines.append(f"_Atualizado em {now} • hash {cur_fields.get('full_hash','')} • fonte: TJRJ Portal_")
    return "\n".join(lines)

def main():
    cur_txt, err = read_current_snapshot()
    if err:
        print("[ERRO] " + err)
        print("[STATUS] NO_CHANGE")
        return

    cur_fields = extract_fields(cur_txt)
    prev_hash = previous_hash()
    prev_txt = previous_text()
    prev_fields = extract_fields(prev_txt) if prev_txt else None

    changed = (prev_hash is None) or (cur_fields["full_hash"] != prev_hash)
    if prev_txt is not None:
        field_changed = any(cur_fields[k] != prev_fields.get(k, "") for k in ["localizacao", "ult_mov_tipo", "ult_mov_data"])
        changed = field_changed

    first_run = prev_hash is None
    LATEST_SNAP.write_text(cur_txt, encoding="utf-8")
    SNAP_HASH_FILE.write_text(cur_fields["full_hash"], encoding="utf-8")

    if first_run:
        print("[STATUS] NO_CHANGE — baseline inicializado.")
        print("[HASH] {} | localizacao={} mov={} data={}".format(cur_fields["full_hash"], clean_loc(cur_fields["localizacao"])[:60], clean_field(cur_fields["ult_mov_tipo"])[:60], clean_field(cur_fields["ult_mov_data"])[:40]))
        return

    if changed:
        report = build_report(cur_txt, True, cur_fields, prev_fields)
        print(report)
        print("\n[STATUS] CHANGED")
        print("[HASH] {} -> {}".format(prev_hash, cur_fields["full_hash"]))
    else:
        # Para cron sem mudança, imprime versão curta mas ainda amigável (o LLM vai suprimir entrega)
        print("[STATUS] NO_CHANGE")
        print("[HASH] {} (sem alteração)".format(cur_fields["full_hash"]))
        print("[FIELDS] localizacao={} | mov={} | data={}".format(clean_loc(cur_fields["localizacao"])[:60], clean_field(cur_fields["ult_mov_tipo"])[:60], clean_field(cur_fields["ult_mov_data"])[:40]))
        # Também gera preview amigável para debug mas não é entregue
        # print(build_report(cur_txt, False, cur_fields, prev_fields))

if __name__ == "__main__":
    main()
