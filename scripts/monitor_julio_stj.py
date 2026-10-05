#!/usr/bin/env python3
"""Monitor STJ HC 1.116.750/RJ for new decisions."""
import subprocess
import json
import os
import re
from datetime import datetime

PROCESSO = "202603112107"
CHECK_FILE = "C:/Projetos/superJus/Clientes/Julio_Pereira_Marcos/Caso_Principal/documentos_processo/last_phase_julio.txt"

def get_last_phase():
    """Get the last known phase from the check file."""
    if os.path.exists(CHECK_FILE):
        with open(CHECK_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ""

def normalize_phase(s):
    return re.sub(r'\s+', ' ', s).strip()

def save_last_phase(phase):
    """Save the current phase to the check file."""
    with open(CHECK_FILE, 'w', encoding='utf-8') as f:
        f.write(normalize_phase(phase))

def check_stj():
    """Check STJ for new phases."""
    import urllib.request
    import re
    
    url = f"https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo={PROCESSO}&totalRegistrosPorPagina=40&aplicacao=processos.ea"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Extract phases
        phases = re.findall(r'classSpanFaseData">(\d{2}/\d{2}/\d{4})</span><span class="classSpanFaseHora">(\d{2}:\d{2})</span>.*?classSpanFaseTexto[^>]*>(.*?)</span', html, re.DOTALL)
        
        if phases:
            latest = phases[0]
            date, time, text = latest
            text = re.sub(r'<[^>]+>', '', text).strip()
            return f"{date} {time} - {text}"
        
        return None
    except Exception as e:
        return f"Erro: {e}"

# Main
last_phase = normalize_phase(get_last_phase())
current_phase_raw = check_stj()
current_phase = normalize_phase(current_phase_raw) if current_phase_raw and not str(current_phase_raw).startswith("Erro") else None

if current_phase and not current_phase.startswith("Erro") and current_phase != last_phase:
    save_last_phase(current_phase)
    print(f"🔔 NOVA ATUALIZAÇÃO NO HC 1.116.750/RJ!")
    print(f"📅 {current_phase}")
    print(f"👤 Paciente: JULIO PEREIRA MARCOS")
    print(f"⚖️ Relator: Min. OG FERNANDES")
else:
    print(f"✅ Sem alterações. Última fase: {last_phase}")
