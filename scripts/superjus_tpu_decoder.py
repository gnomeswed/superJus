# -*- coding: utf-8 -*-
"""
SuperJus TPU Decoder — Decodificador e Auditor Anti-Alucinação de Códigos TPU do CNJ
===================================================================================
Este módulo decodifica movimentações processuais do DataJud e PJe, com foco especial
em evitar armadilhas de classificação da Tabela Processual Unificada (TPU) do CNJ,
especialmente em códigos que afetam a liberdade e custódia do réu.

Casos clássicos de armadilha:
- Código 12146 ("Liberdade Provisória"): usado para apreciação (deferimento OU indeferimento).
- Código 12068 ("Prisão Preventiva"): usado para apreciação (decretação, manutenção OU revogação).
- Código 198 ("Decisão"): genérico, requer análise textual.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import re


# Códigos que NÃO indicam resultado e NÃO podem ser interpretados pelo nome literal
TPU_AMBIGUOUS_CODES = {
    12146: "Liberdade Provisória",
    12068: "Prisão Preventiva",
    198: "Decisão Interlocutória",
    581: "Documento Juntado",
    60: "Expedição de Documento",
    11383: "Ato Ordinatório",
    51: "Conclusão ao Juiz",
    85: "Petição",
    219: "Condenação",
    326: "Absolvição",
    385: "Extinção da Punibilidade",
    1051: "Decurso de Prazo",
}

# Palavras-chave positivas (deferimento / soltura)
KEYWORDS_DEFERIDO = [
    "concedid", "deferid", "revogad", "relaxad", "alvara", "soltura",
    "acolhid", "provid", "revogacao da prisao", "liberdade provisoria com medidas"
]

# Palavras-chave negativas (indeferimento / manutenção)
KEYWORDS_INDEFERIDO = [
    "indeferid", "negad", "denegad", "mantid", "rejeitad", "inacolhid",
    "desprovid", "nao provid", "manutencao da prisao", "convertida em preventiva"
]


@dataclass
class DecodedMovement:
    codigo: int
    nome_original: str
    data_hora: str
    is_ambiguous: bool
    status_interpretado: str  # "DEFERIDO", "INDEFERIDO", "AMBIGUO", "ROTINA"
    complementos_str: str
    alerta_seguranca: Optional[str] = None
    afeta_custodia: bool = False
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_markdown_row(self) -> str:
        dt_clean = self.data_hora[:19].replace("T", " ") if self.data_hora else "-"
        status_tag = ""
        if self.alerta_seguranca:
            status_tag = f" ⚠️ **{self.alerta_seguranca}**"
        elif self.status_interpretado in ("DEFERIDO", "INDEFERIDO"):
            status_tag = f" [{self.status_interpretado}]"
            
        comp_text = f" -> {self.complementos_str}" if self.complementos_str else ""
        return f"| {dt_clean} | {self.codigo} | {self.nome_original}{status_tag}{comp_text} |"


def parse_complementos(comps: List[Dict[str, Any]]) -> str:
    """Extrai representação textual legível de complementos tabelados."""
    if not comps:
        return ""
    parts = []
    for c in comps:
        nome = c.get("nome", "")
        desc = c.get("descricao", "")
        if nome and desc:
            parts.append(f"{nome}: {desc}")
        elif nome:
            parts.append(nome)
        elif desc:
            parts.append(desc)
    return " | ".join(parts)


def decode_movement(mov: Dict[str, Any], text_hint: str = "") -> DecodedMovement:
    """
    Decodifica uma movimentação individual do DataJud / PJe com auditoria anti-alucinação.
    """
    codigo = int(mov.get("codigo", 0) or 0)
    nome = mov.get("nome", "") or ""
    data_hora = mov.get("dataHora", "") or ""
    comps = mov.get("complementosTabelados", []) or []
    comp_str = parse_complementos(comps)
    
    combined_text = f"{nome} {comp_str} {text_hint}".lower()
    
    is_ambiguous = codigo in TPU_AMBIGUOUS_CODES
    afeta_custodia = codigo in (12146, 12068) or any(k in combined_text for k in ["prisao", "liberdade", "soltura", "custodia", "alvara"])
    
    status = "ROTINA"
    alerta = None
    
    # Análise de Liberdade Provisória (Cód. 12146) e Prisão Preventiva (Cód. 12068)
    if codigo == 12146 or "liberdade provisória" in nome.lower():
        afeta_custodia = True
        is_ambiguous = True
        
        # Verificar complementos e texto
        has_pos = any(k in combined_text for k in KEYWORDS_DEFERIDO)
        has_neg = any(k in combined_text for k in KEYWORDS_INDEFERIDO)
        
        if has_pos and not has_neg:
            status = "DEFERIDO"
        elif has_neg:
            status = "INDEFERIDO"
            alerta = "DECISÃO DE INDEFERIMENTO (MANTÉM PREVENTIVA)"
        else:
            status = "AMBIGUO"
            alerta = "APRECIAÇÃO SEM RESULTADO EXPLÍCITO NO BANCO — NÃO PRESUMIR SOLTURA"
            
    elif codigo == 12068 or "prisão preventiva" in nome.lower():
        afeta_custodia = True
        is_ambiguous = True
        if any(k in combined_text for k in ["revogad", "relaxad"]):
            status = "DEFERIDO"
            alerta = "REVOGAÇÃO DE PREVENTIVA INDICADA"
        elif any(k in combined_text for k in ["decretad", "mantid", "convertid"]):
            status = "INDEFERIDO"
            alerta = "DECRETAÇÃO/MANUTENÇÃO DE PRISÃO PREVENTIVA"
        else:
            status = "AMBIGUO"
            alerta = "APRECIAÇÃO DE PRISÃO SEM RESULTADO EXPLÍCITO"
            
    elif codigo == 198: # Decisão genérica
        if afeta_custodia:
            status = "AMBIGUO"
            alerta = "DECISÃO AFETANDO CUSTÓDIA — VERIFICAR TEOR"
        else:
            status = "ROTINA"
            
    return DecodedMovement(
        codigo=codigo,
        nome_original=nome,
        data_hora=data_hora,
        is_ambiguous=is_ambiguous,
        status_interpretado=status,
        complementos_str=comp_str,
        alerta_seguranca=alerta,
        afeta_custodia=afeta_custodia,
        raw=mov
    )


def audit_movements_history(movs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Varre a lista completa de movimentações, ordenando por data e detectando
    alertas de custódia e armadilhas da TPU.
    """
    sorted_movs = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
    decoded_list = [decode_movement(m) for m in sorted_movs]
    
    critical_alerts = [dm for dm in decoded_list if dm.alerta_seguranca]
    custody_events = [dm for dm in decoded_list if dm.afeta_custodia]
    
    # Determinar status cautelar inferível com segurança
    safe_custody_status = "INDETERMINADO"
    if custody_events:
        latest_custody = custody_events[0]
        if latest_custody.status_interpretado == "INDEFERIDO":
            safe_custody_status = "PRESO (Último pedido de liberdade INDEFERIDO / Mantida preventiva)"
        elif latest_custody.status_interpretado == "DEFERIDO":
            safe_custody_status = "LIBERDADE PROVISÓRIA / SOLTURA INDICADA"
        else:
            safe_custody_status = "INCERTO (Apreciação registrada sem resultado explícito — conferir autos)"
            
    return {
        "total_movimentos": len(decoded_list),
        "decoded_movements": decoded_list,
        "critical_alerts": critical_alerts,
        "custody_events": custody_events,
        "safe_custody_status": safe_custody_status,
        "has_unresolved_ambiguity": any(dm.status_interpretado == "AMBIGUO" for dm in custody_events[:3])
    }
