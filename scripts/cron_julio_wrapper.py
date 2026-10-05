#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wrapper executado pelo cron: roda scraping + diff. Só imprime relatório se mudou."""
import subprocess, sys, os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PY = Path("C:/Users/Administrator/AppData/Local/Programs/Python/Python312/python.exe")
BASE = Path("C:/Projetos/superJus")
SCRAPER = BASE / "scripts" / "check_all_julio_live_now.py"
DIFF = BASE / "scripts" / "monitor_julio_diff.py"

def run_scraper():
    # Timeout generoso: scraping Playwright pode levar ~30s
    r = subprocess.run([str(PY), str(SCRAPER)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    if r.returncode != 0:
        print("[scraper] exit={} err:\n{}".format(r.returncode, (r.stderr or r.stdout)[-2000:]))
        return False
    return True

def run_diff():
    r = subprocess.run([str(PY), str(DIFF)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    sys.stdout.write(r.stdout)
    if r.stderr:
        sys.stderr.write(r.stderr)
    # Sinaliza pro scheduler se houve mudança (examinado pelo llm-skip logic abaixo)
    return "[STATUS] CHANGED" in r.stdout

if __name__ == "__main__":
    ok = run_scraper()
    if not ok:
        print("[CRON] scraping falhou — diff será tentado com snapshot anterior.")
    changed = run_diff()
    if not changed:
        # Sem mudança: imprime linha curta; o llm receberá vazio e não gerará entrega (silence on no-change)
        pass
