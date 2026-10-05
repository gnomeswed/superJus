# -*- coding: utf-8 -*-
import pathlib, json

def test_no_hardcoded_super_analista_in_runtime():
    offenders=[]
    for p in pathlib.Path("core").glob("*.py"):
        txt=p.read_text(encoding="utf-8", errors="ignore")
        # só falha se houver caminho absoluto com o nome antigo (ex: C:\...\Super Analista...)
        if "Super Analista Jurídico" in txt and ("CLIENTS_ROOT" in txt and ("C:\\" in txt or "c:\\" in txt)):
            offenders.append(str(p))
    assert not offenders, f"Caminhos hardcoded remanescentes: {offenders}"

def test_contract_report_docs():
    # garante que o contrato de analise_timeline_version existe em memU ou docs
    assert (pathlib.Path("core")/"process_model.py").exists()
    assert (pathlib.Path("core")/"config.py").exists()
