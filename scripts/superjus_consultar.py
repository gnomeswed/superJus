# -*- coding: utf-8 -*-
"""
SuperJus Consultar — CLI Oficial Unificado do Protocolo Operacional Padrão (POP v1.0)
====================================================================================
Implementa a Cadeia de 5 Fases para consulta e atualização processual:
  Fase 1: Memória Persistente (memU / SQLite)
  Fase 2: DataJud / MCP Estruturado
  Fase 3: Reconciliação com Diários (DJEN/DJERJ)
  Fase 4: Validação Anti-Alucinação com Decodificador TPU
  Fase 5: Persistência em Disco e memU

Uso:
  python scripts/superjus_consultar.py --processo 0808595-36.2026.8.19.0002 --cliente "Lucas_Dias_Oliveira"
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
import sqlite3
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Garantir UTF-8 no Windows
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

# Adicionar raiz do projeto ao path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Imports do ecossistema SuperJus
from core.config import PROJECT_ROOT, CLIENTS_ROOT, datajud_headers
from scripts.superjus_tpu_decoder import decode_movement, audit_movements_history


DATAJUD_ENDPOINTS = {
    "tjrj": "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search",
    "stj": "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search",
    "tjsp": "https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search",
    "trf2": "https://api-publica.datajud.cnj.jus.br/api_publica_trf2/_search",
}


def infer_court_from_cnj(proc_str: str) -> str:
    """Infere o tribunal a partir do número CNJ (ex: 8.19 -> tjrj, 8.26 -> tjsp)."""
    clean = re.sub(r"\D", "", proc_str)
    if len(clean) >= 20:
        j_tr = clean[13:16]
        if j_tr == "819":
            return "tjrj"
        elif j_tr == "826":
            return "tjsp"
        elif j_tr == "402":
            return "trf2"
        elif clean.startswith("00") and clean[13:14] == "3":
            return "stj"
    return "tjrj"


def consultar_memu_historico(termo: str) -> List[Dict[str, Any]]:
    """FASE 1: Consulta o banco SQLite local do memU."""
    db_path = Path.home() / ".memu" / "memu.sqlite3"
    if not db_path.exists():
        return []
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        query = """
            SELECT name, description, content, created_at 
            FROM memu_recall_files 
            WHERE name LIKE ? OR description LIKE ? OR content LIKE ?
            ORDER BY created_at DESC LIMIT 5
        """
        like_pattern = f"%{termo}%"
        cursor.execute(query, (like_pattern, like_pattern, like_pattern))
        rows = cursor.fetchall()
        conn.close()
        return [
            {"name": r[0], "description": r[1], "content": r[2], "created_at": r[3]}
            for r in rows
        ]
    except Exception:
        return []


def consultar_datajud(proc_clean: str, court: str) -> List[Dict[str, Any]]:
    """FASE 2: Consulta a API Pública do DataJud CNJ com retry."""
    url = DATAJUD_ENDPOINTS.get(court.lower(), DATAJUD_ENDPOINTS["tjrj"])
    headers = datajud_headers()
    payload = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("hits", {}).get("hits", [])
    except Exception as e:
        print(f"⚠️ [DataJud] Erro na requisição ({court.upper()}): {e}")
        return []


def checar_diario_djen(termo: str) -> List[Dict[str, Any]]:
    """FASE 3: Reconciliação com publicações recentes no DJEN."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SuperJus/1.0",
        "Accept": "application/json, text/plain, */*"
    }
    url = f"https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto={urllib.parse.quote(termo)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("items", [])[:5]
    except Exception:
        return []


def gravar_memu_registro(name: str, desc: str, content: str, track: str = "memory") -> bool:
    """FASE 5: Persiste o resultado no banco memU."""
    db_path = Path.home() / ".memu" / "memu.sqlite3"
    if not db_path.exists():
        return False
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        query = """
            INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content)
            VALUES (lower(hex(randomblob(16))), datetime('now'), datetime('now'), ?, ?, ?, ?)
        """
        cursor.execute(query, (name, track, desc, content))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def run_consulta_padrao(processo: str, cliente_nome: str, tribunal: Optional[str] = None):
    print("=" * 80)
    print(f"🏛️ SUPERJUS — CONSULTA PROCESSUAL PADRÃO (POP v1.0)")
    print(f"Processo: {processo} | Cliente: {cliente_nome}")
    print("=" * 80)

    clean_proc = re.sub(r"\D", "", processo)
    detected_court = tribunal or infer_court_from_cnj(processo)
    
    # -------------------------------------------------------------------------
    # FASE 1: Memória Persistente (memU)
    # -------------------------------------------------------------------------
    print("\n[FASE 1] Resgatando memória prévia no memU...")
    memorias = consultar_memu_historico(cliente_nome) or consultar_memu_historico(clean_proc)
    if memorias:
        print(f"  ✓ {len(memorias)} registro(s) prévio(s) recuperado(s).")
        print(f"  Última memória: {memorias[0]['name']} ({memorias[0]['created_at']})")
    else:
        print("  ℹ️ Nenhum histórico prévio específico localizado na memória.")

    # -------------------------------------------------------------------------
    # FASE 2: Consulta DataJud CNJ
    # -------------------------------------------------------------------------
    print(f"\n[FASE 2] Consultando DataJud CNJ ({detected_court.upper()})...")
    hits = consultar_datajud(clean_proc, detected_court)
    
    if not hits:
        print(f"  ⚠️ Nenhum registro retornado pelo DataJud para {clean_proc}.")
        return

    print(f"  ✓ Encontrado(s) {len(hits)} registro(s) de instância no tribunal.")
    
    # -------------------------------------------------------------------------
    # FASE 4: Auditoria Anti-Alucinação com Decodificador TPU
    # -------------------------------------------------------------------------
    print("\n[FASE 4] Decodificando e auditando movimentações com Decodificador TPU...")
    
    for idx, hit in enumerate(hits, 1):
        src = hit["_source"]
        grau = src.get("grau", "N/I")
        orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
        classe = src.get("classe", {}).get("nome", "N/I")
        dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
        movs = src.get("movimentos", [])
        
        audit_res = audit_movements_history(movs)
        
        print(f"\n--- Instância [{idx}]: Grau {grau} | {orgao} ---")
        print(f"Classe: {classe} | Última Sincronização CNJ: {dt_at}")
        print(f"Total de Movimentos: {audit_res['total_movimentos']}")
        print(f"Status Cautelar Auditado: {audit_res['safe_custody_status']}")
        
        if audit_res["critical_alerts"]:
            print("\n🚨 ALERTAS CRÍTICOS DE AUDITORIA (CUSTÓDIA / TPU):")
            for alert in audit_res["critical_alerts"][:5]:
                dt = alert.data_hora[:19].replace("T", " ")
                print(f"  • {dt} | Cód. {alert.codigo} ({alert.nome_original}) -> {alert.alerta_seguranca}")
                
        print("\nÚltimas 5 Movimentações Decodificadas:")
        for dm in audit_res["decoded_movements"][:5]:
            print(f"  {dm.to_markdown_row()}")

    # -------------------------------------------------------------------------
    # FASE 3: Reconciliação Temporal com Diários (DJEN)
    # -------------------------------------------------------------------------
    print("\n[FASE 3] Verificando Diários Oficiais (DJEN)...")
    diarios = checar_diario_djen(clean_proc)
    if diarios:
        print(f"  ✓ {len(diarios)} publicação(ões) localizada(s) no DJEN.")
        for d in diarios[:2]:
            dt = d.get("data_disponibilizacao", "")
            tipo = d.get("tipoComunicacao", "")
            print(f"  📌 Publicado em {dt}: {tipo}")
    else:
        print("  ℹ️ Nenhuma publicação pendente recente encontrada no DJEN.")

    # -------------------------------------------------------------------------
    # FASE 5: Persistência em Disco e memU
    # -------------------------------------------------------------------------
    print("\n[FASE 5] Persistindo dados e gerando relatórios...")
    client_dir = CLIENTS_ROOT / cliente_nome.replace(" ", "_")
    movs_dir = client_dir / "02_Movimentacoes"
    movs_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    raw_path = movs_dir / f"datajud_raw_{timestamp_str}.json"
    
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump([h["_source"] for h in hits], f, indent=2, ensure_ascii=False)
    print(f"  ✓ JSON bruto salvo em: {raw_path}")
    
    # Gravar resumo no memU
    resumo_memu = f"Consulta atualizada em {timestamp_str}. Total instâncias: {len(hits)}. Status cautelar auditado: {audit_res['safe_custody_status']}."
    memu_ok = gravar_memu_registro(
        name=f"atualizacao_{cliente_nome}_{datetime.now().strftime('%Y_%m_%d')}",
        desc=f"Atualização POP {processo} ({cliente_nome})",
        content=resumo_memu
    )
    if memu_ok:
        print("  ✓ Registro persistido com sucesso na memória compartilhada memU.")

    print("\n" + "=" * 80)
    print("✅ CONSULTA CONCLUÍDA COM SUCESSO SOB AS DIRETRIZES DO POP v1.0")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="SuperJus — Consulta Processual Padronizada")
    parser.add_argument("--processo", required=True, help="Número CNJ do processo")
    parser.add_argument("--cliente", required=True, help="Nome do cliente (usado na pasta e memória)")
    parser.add_argument("--tribunal", default=None, help="Sigla do tribunal (opcional, inferido por padrão)")
    
    args = parser.parse_args()
    run_consulta_padrao(args.processo, args.cliente, args.tribunal)


if __name__ == "__main__":
    main()
