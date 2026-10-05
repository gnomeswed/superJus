# -*- coding: utf-8 -*-
"""
SUPERJUS — SQLITE MCP SERVER NATIVO
Conecta-se ao banco de dados memU (C:/Users/Administrator/.memu/memu.sqlite3) ou bancos locais do escritório.
Sem dependências frágeis, sem erros de 'list_resources', 100% compatível com FastMCP.
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from fastmcp import FastMCP

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

DEFAULT_DB = Path(r"C:\Users\Administrator\.memu\memu.sqlite3")

mcp = FastMCP(
    name="SuperJus SQLite Intelligence",
    instructions=(
        "Servidor MCP para consultas e operações seguras no banco de dados SQLite do SuperJus / memU. "
        "Permite inspecionar tabelas, schemas e executar consultas analíticas nos dados relacionais e memórias."
    )
)

def get_connection(db_path: str = "") -> sqlite3.Connection:
    target = Path(db_path) if db_path else DEFAULT_DB
    if not target.exists():
        raise FileNotFoundError(f"Banco de dados '{target}' não encontrado.")
    con = sqlite3.connect(str(target))
    con.row_factory = sqlite3.Row
    return con

@mcp.tool()
def list_tables(db_path: str = "") -> str:
    """Lista todas as tabelas presentes no banco de dados SQLite.
    
    Args:
        db_path: (Opcional) Caminho do banco SQLite. Se omitido, usa memu.sqlite3 padrão.
    """
    try:
        with get_connection(db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            rows = [r[0] for r in cur.fetchall()]
            return json.dumps({"tables": rows}, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao listar tabelas: {str(e)}"

@mcp.tool()
def describe_table(table_name: str, db_path: str = "") -> str:
    """Descreve as colunas e tipos de uma tabela específica.
    
    Args:
        table_name: Nome da tabela a ser descrita.
        db_path: (Opcional) Caminho do banco SQLite.
    """
    try:
        with get_connection(db_path) as con:
            cur = con.cursor()
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = [
                {
                    "cid": r["cid"],
                    "name": r["name"],
                    "type": r["type"],
                    "notnull": bool(r["notnull"]),
                    "dflt_value": r["dflt_value"],
                    "pk": bool(r["pk"])
                }
                for r in cur.fetchall()
            ]
            return json.dumps({"table": table_name, "columns": columns}, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Erro ao descrever tabela: {str(e)}"

@mcp.tool()
def read_query(query: str, db_path: str = "") -> str:
    """Executa uma consulta SQL (SELECT) de leitura no banco de dados.
    
    Args:
        query: Instrução SQL de consulta (deve ser SELECT ou PRAGMA).
        db_path: (Opcional) Caminho do banco SQLite.
    """
    clean_q = query.strip().upper()
    if not (clean_q.startswith("SELECT") or clean_q.startswith("PRAGMA") or clean_q.startswith("EXPLAIN")):
        return "Erro: read_query permite apenas consultas de leitura (SELECT / PRAGMA). Use write_query para modificações."
        
    try:
        with get_connection(db_path) as con:
            cur = con.cursor()
            cur.execute(query)
            rows = [dict(r) for r in cur.fetchall()]
            return json.dumps({"count": len(rows), "results": rows[:100]}, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Erro na execução da query: {str(e)}"

@mcp.tool()
def write_query(query: str, db_path: str = "") -> str:
    """Executa uma instrução SQL de modificação (INSERT, UPDATE, DELETE) no banco.
    
    Args:
        query: Instrução SQL de modificação.
        db_path: (Opcional) Caminho do banco SQLite.
    """
    try:
        with get_connection(db_path) as con:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            return f"Query executada com sucesso. Linhas afetadas: {cur.rowcount}"
    except Exception as e:
        return f"Erro na execução da instrução write: {str(e)}"

if __name__ == "__main__":
    mcp.run()
