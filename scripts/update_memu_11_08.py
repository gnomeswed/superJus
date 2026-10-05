# -*- coding: utf-8 -*-
import subprocess
import json
import sys

content = {
    "data_verificacao": "11/08/2026",
    "acao_penal_buzios": {
        "processo": "0023013-51.2021.8.19.0078",
        "localizacao_serventia": "Processamento",
        "ultima_juntada": "04/08/2026 (registrada no sistema em 06/08/2026)",
        "despacho_juiz": "Despacho de mero expediente em 30/07/2026 (devolvido em 01/08/2026)",
        "total_movimentos": 55
    },
    "rhc_stj": {
        "processo": "HC 1.116.750 / RJ (2026/0311210-7)",
        "relator": "Min. Og Fernandes",
        "orgao": "6ª Turma",
        "status": "Aguardando parecer do MPF e inclusão em pauta / julgamento de mérito"
    }
}

cmd = [
    sys.executable,
    "scripts/memu_store.py",
    "--name", "andamento_julio_11_08_2026",
    "--track", "Julio_Pereira_Marcos_Caso_Principal",
    "--description", "Verificacao ao vivo em 11/08/2026 dos processos de Julio Pereira Marcos",
    "--content", json.dumps(content, ensure_ascii=False)
]

res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
