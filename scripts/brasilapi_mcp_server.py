# -*- coding: utf-8 -*-
"""
SUPERJUS — BRASIL DADOS ABERTOS & OSINT MCP SERVER
Servidor MCP para consulta de dados públicos brasileiros via BrasilAPI e bases públicas.
Suporta:
- CNPJ (Razão Social, Situação, QSA - Quadro Societário, CNAE, Endereço)
- CEP (Logradouro, Bairro, Cidade, Estado, Coordenadas)
- Feriados Nacionais e Forenses (para cômputo de prazos do CPP/CPC)
- Bancos e Instituições Financeiras
"""

import json
import sys
import urllib.request
import urllib.parse
from fastmcp import FastMCP

sys.stdout.reconfigure(encoding="utf-8")

mcp = FastMCP(
    name="SuperJus Brasil Dados Abertos (OSINT & Due Diligence)",
    instructions=(
        "Servidor MCP para consulta e investigação de dados públicos brasileiros. "
        "Permite consultar empresas (CNPJ), sócios e administradores (QSA), "
        "endereços (CEP), feriados oficiais para cômputo de prazos processuais "
        "e instituições financeiras."
    )
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

def _get_json(url: str, timeout: int = 10) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))

@mcp.tool()
def consultar_cnpj(cnpj: str) -> str:
    """Consulta dados cadastrais completos de pessoa jurídica brasileira pelo CNPJ.
    
    Args:
        cnpj: Número do CNPJ (com ou sem pontuação).
        
    Returns:
        Relatório detalhado contendo Razão Social, Nome Fantasia, Situação Cadastral,
        CNAE principal/secundários, Endereço completo, Capital Social e Quadro Societário (QSA).
    """
    clean_cnpj = "".join(filter(str.isdigit, cnpj))
    if len(clean_cnpj) != 14:
        return f"Erro: CNPJ '{cnpj}' inválido. Deve conter exatamente 14 dígitos."
        
    url = f"https://brasilapi.com.br/api/cnpj/v1/{clean_cnpj}"
    try:
        data = _get_json(url)
        qsa = data.get("qsa", [])
        socios_str = ""
        if qsa:
            socios_str = "\n### Quadro de Sócios e Administradores (QSA):\n"
            for s in qsa:
                nome = s.get("nome_socio", "N/I")
                qualif = s.get("qualificacao_socio", "N/I")
                faixa_etaria = s.get("faixa_etaria", "")
                socios_str += f"- **{nome}** — Qualificação: {qualif} ({faixa_etaria})\n"
        
        cnaes_sec = data.get("cnaes_secundarios", [])
        cnaes_str = ""
        if cnaes_sec:
            cnaes_str = "\n### Atividades Secundárias (CNAEs):\n"
            for c in cnaes_sec[:8]:
                cnaes_str += f"- {c.get('codigo')}: {c.get('descricao')}\n"

        relatorio = (
            f"# Consulta Empresarial — CNPJ {data.get('cnpj')}\n\n"
            f"* **Razão Social:** {data.get('razao_social')}\n"
            f"* **Nome Fantasia:** {data.get('nome_fantasia') or 'Não informado'}\n"
            f"* **Situação Cadastral:** {data.get('descricao_situacao_cadastral')} (desde {data.get('data_situacao_cadastral')})\n"
            f"* **Natureza Jurídica:** {data.get('natureza_juridica')}\n"
            f"* **Data de Abertura:** {data.get('data_inicio_atividade')}\n"
            f"* **Capital Social:** R$ {data.get('capital_social', 0):,.2f}\n"
            f"* **CNAE Principal:** {data.get('cnae_fiscal')} — {data.get('cnae_fiscal_descricao')}\n"
            f"* **Endereço:** {data.get('descricao_tipo_de_logradouro', '')} {data.get('logradouro')}, nº {data.get('numero')}, "
            f"{data.get('complemento', '')} - {data.get('bairro')}, {data.get('municipio')}/{data.get('uf')}, CEP {data.get('cep')}\n"
            f"* **Telefone / Contato:** ({data.get('ddd_telefone_1', '')}) {data.get('telefone_1', '')}\n"
            f"{socios_str}"
            f"{cnaes_str}"
        )
        return relatorio
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"CNPJ {clean_cnpj} não encontrado na base pública."
        return f"Erro ao consultar CNPJ ({e.code}): {e.reason}"
    except Exception as e:
        return f"Falha na consulta do CNPJ: {str(e)}"

@mcp.tool()
def consultar_cep(cep: str) -> str:
    """Consulta endereço oficial brasileiro a partir do código postal (CEP).
    
    Args:
        cep: Código de Endereçamento Postal (8 dígitos, com ou sem traço).
        
    Returns:
        Logradouro, Bairro, Cidade, Estado e Coordenadas geográficas.
    """
    clean_cep = "".join(filter(str.isdigit, cep))
    if len(clean_cep) != 8:
        return f"Erro: CEP '{cep}' inválido. Deve conter 8 dígitos."
        
    url = f"https://brasilapi.com.br/api/cep/v2/{clean_cep}"
    try:
        data = _get_json(url)
        coords = data.get("location", {}).get("coordinates", {})
        coord_str = ""
        if coords and coords.get("latitude"):
            coord_str = f"\n* **Geolocalização:** Lat: {coords.get('latitude')}, Long: {coords.get('longitude')}"
            
        return (
            f"📍 **Endereço Localizado (CEP {clean_cep}):**\n"
            f"* **Logradouro:** {data.get('street', 'N/I')}\n"
            f"* **Bairro:** {data.get('neighborhood', 'N/I')}\n"
            f"* **Cidade / UF:** {data.get('city', 'N/I')} - {data.get('state', 'N/I')}\n"
            f"* **Serviço Responsável:** {data.get('service', 'BrasilAPI')}"
            f"{coord_str}"
        )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"CEP {clean_cep} não encontrado na base de dados dos Correios/BrasilAPI."
        return f"Erro na consulta do CEP ({e.code}): {e.reason}"
    except Exception as e:
        return f"Falha na consulta do CEP: {str(e)}"

@mcp.tool()
def consultar_feriados_nacionais(ano: int) -> str:
    """Consulta os feriados nacionais oficiais de um determinado ano para contagem de prazos processuais (CPC/CPP).
    
    Args:
        ano: Ano para levantamento dos feriados (ex: 2026).
        
    Returns:
        Lista de feriados com datas, nomes e tipos.
    """
    url = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
    try:
        data = _get_json(url)
        if not data:
            return f"Nenhum feriado localizado para o ano {ano}."
            
        res = f"📅 **Feriados Nacionais Oficiais ({ano}):**\n\n"
        for f in data:
            dt = f.get("date", "")
            partes = dt.split("-")
            dt_fmt = f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else dt
            res += f"• **{dt_fmt}** — {f.get('name')} ({f.get('type')})\n"
        return res
    except Exception as e:
        return f"Falha na consulta de feriados: {str(e)}"

if __name__ == "__main__":
    mcp.run()
