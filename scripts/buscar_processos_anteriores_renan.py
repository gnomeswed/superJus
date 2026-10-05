# -*- coding: utf-8 -*-
import json, urllib.request, sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
from core.config import datajud_headers

sys.stdout.reconfigure(encoding="utf-8")

headers = datajud_headers()
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

nome = "Renan Rodrigues de Souza"
cpf_fmt = "198.249.487-59"
cpf_raw = "19824948759"

queries = [
    ("Nome Completo", {"query": {"query_string": {"query": f'"{nome}"'}}, "size": 15}),
    ("CPF Formatado", {"query": {"query_string": {"query": f'"{cpf_fmt}"'}}, "size": 15}),
    ("CPF Puro", {"query": {"query_string": {"query": f'"{cpf_raw}"'}}, "size": 15}),
    ("Nome em Polo Passivo", {"query": {"match_phrase": {"pessoas.nome": nome}}, "size": 15})
]

encontrados = {}

print("=== BUSCA DATAJUD TJRJ — PROCESSOS ANTERIORES E EXECUÇÃO PENAL (VEP) ===")

for rotulo, q in queries:
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.loads(r.read().decode("utf-8"))
            hits = res.get("hits", {}).get("hits", [])
            print(f"[{rotulo}] retornou {len(hits)} processo(s).")
            for h in hits:
                src = h["_source"]
                num = src.get("numeroProcesso")
                if num and num not in encontrados:
                    encontrados[num] = src
    except Exception as e:
        print(f"Erro em [{rotulo}]: {e}")

print(f"\nTotal de Processos Únicos Localizados: {len(encontrados)}\n")

for num, src in encontrados.items():
    grau = src.get("grau")
    classe = src.get("classe", {}).get("nome")
    orgao = src.get("orgaoJulgador", {}).get("nome")
    dt_aj = src.get("dataAjuizamento")
    dt_at = src.get("dataHoraUltimaAtualizacao")
    assuntos = [a.get("nome") for a in src.get("assuntos", [])]
    movs = src.get("movimentos", [])
    
    print("=" * 80)
    print(f"Processo: {num} (Grau: {grau})")
    print(f"Órgão: {orgao} | Classe: {classe}")
    print(f"Ajuizamento: {dt_aj} | Última Atualização: {dt_at}")
    print(f"Assuntos: {', '.join(assuntos)}")
    print(f"Total Movimentos: {len(movs)}")
    
    # Checar se há fuga, evasão, mandado de prisão ou execução penal
    movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
    print("Últimas 5 movimentações:")
    for m in movs_sorted[:5]:
        dt = m.get("dataHora", "")[:19].replace("T", " ")
        print(f"  • {dt} | {m.get('nome')} [Cód. {m.get('codigo')}] -> {m.get('complementosTabelados')}")
    
    evasao_movs = [m for m in movs if any(k in (m.get("nome","") + str(m.get("complementosTabelados"))).lower() for k in ["evas", "fuga", "mandado", "captura", "regress", "falta grave", "suspens"])]
    if evasao_movs:
        print("\n🚨 Movimentações de Evasão / Mandado / Regressão:")
        for em in evasao_movs[:5]:
            dt = em.get("dataHora", "")[:19].replace("T", " ")
            print(f"  ⚠️ {dt} | {em.get('nome')} [Cód. {em.get('codigo')}]")
