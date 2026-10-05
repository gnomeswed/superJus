# -*- coding: utf-8 -*-
from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

CLIENTS_ROOT: Path = PROJECT_ROOT / "Clientes"
AGENTS_ROOT: Path = PROJECT_ROOT / ".agents"
STATE_FILE: Path = AGENTS_ROOT / "telegram_last_state.json"
DOCS_ROOT: Path = PROJECT_ROOT / "docs"


def get_client_path(client_folder: str) -> Path:
    return CLIENTS_ROOT / client_folder


def get_case_path(client_folder: str, case_name: str) -> Path:
    return CLIENTS_ROOT / client_folder / case_name


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(
            f"Variável de ambiente obrigatória ausente: {name}. "
            f"Configure no .env ou no ambiente."
        )
    return value


def require_datajud_key() -> str:
    return require_env("DATAJUD_API_KEY")


def datajud_headers() -> dict:
    key = require_datajud_key().strip()
    auth = key if key.lower().startswith("apikey ") else f"APIKey {key}"
    return {"Authorization": auth, "Content-Type": "application/json"}
