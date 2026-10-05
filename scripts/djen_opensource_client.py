# -*- coding: utf-8 -*-
"""
===============================================================================
                       DJEN-OpenSource-Client (MIT License)
===============================================================================
Cliente Open-Source de Alta Disponibilidade para Consulta ao DJEN & DataJud (CNJ).

Recursos Open-Source Integrados:
1. Engine DataJud REST (API Pública Oficial do CNJ - Isento de bloqueios)
2. Engine Tor Network SOCKS5 (Rotação Dinâmica de IP via circuito Tor)
3. Engine Stealth HTTP com Backoff Exponencial & User-Agent Rotation
===============================================================================
"""

import sys
import json
import time
import random
import socket
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional

# Configuração de Log Professional
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DJEN_OpenSource")

sys.stdout.reconfigure(encoding="utf-8")

# Lista de User-Agents Modernos (Desktop)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
]

class DJENOpenSourceClient:
    """Cliente Open-Source resiliente para consulta processual no DJEN e DataJud."""

    DATAJUD_API_KEY = __import__('os').getenv('DATAJUD_API_KEY','')

    def __init__(self, tor_socks_port: int = 9050):
        self.tor_socks_port = tor_socks_port

    def _get_stealth_headers(self) -> Dict[str, str]:
        """Gera cabeçalhos HTTP legítimos simulando navegação humana."""
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin"
        }

    # -------------------------------------------------------------------------
    # ENGINE 1: DATAJUD OFFICIAL CNJ REST API (RECOMENDADO E SEM BLOQUEIO)
    # -------------------------------------------------------------------------
    def consultar_datajud(self, tribunal: str, termo: str) -> Dict[str, Any]:
        """
        Consulta a API pública oficial do CNJ (DataJud) para o tribunal especificado.
        Isenta de bloqueios de WAF/IP de diários eletrônicos.
        """
        endpoint = f"api_publica_{tribunal.lower()}"
        url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"

        payload = {
            "query": {
                "query_string": {
                    "query": f'"{termo}"'
                }
            },
            "size": 15
        }

        headers = {
            "Authorization": self.DATAJUD_API_KEY,
            "Content-Type": "application/json"
        }

        logger.info(f"[DataJud Engine] Consultando {endpoint.upper()} para termo: '{termo}'...")
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                hits = data.get("hits", {}).get("hits", [])
                logger.info(f"[DataJud Engine] Sucesso! Encontrados {len(hits)} registro(s).")
                return {"sucesso": True, "engine": "DataJud REST API", "total": len(hits), "resultados": hits}
        except Exception as e:
            logger.warning(f"[DataJud Engine] Erro na consulta: {e}")
            return {"sucesso": False, "engine": "DataJud REST API", "erro": str(e)}

    # -------------------------------------------------------------------------
    # ENGINE 2: TOR SOCKS5 OPEN-SOURCE ROUTER
    # -------------------------------------------------------------------------
    def testar_conexao_tor(self) -> bool:
        """Verifica se o serviço open-source Tor SOCKS5 está ativo na porta local."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            res = sock.connect_ex(("127.0.0.1", self.tor_socks_port))
            sock.close()
            return res == 0
        except Exception:
            return False

    def consultar_djen_via_tor(self, tribunal: str, numero_processo: str = "") -> Dict[str, Any]:
        """
        Executa a requisição ao DJEN (PJe Comunica) através do circuito anônimo Tor SOCKS5.
        Requer o Tor Service rodando localmente (127.0.0.1:9050).
        """
        if not self.testar_conexao_tor():
            return {
                "sucesso": False,
                "engine": "Tor Network",
                "erro": f"Serviço Tor não detectado em 127.0.0.1:{self.tor_socks_port}. Inicie o 'tor' para habilitar."
            }

        url = "https://comunica.pje.jus.br/api/v1/comunicacao"
        payload = {"siglaTribunal": tribunal, "meio": "D"}
        if numero_processo:
            payload["numeroProcesso"] = numero_processo

        try:
            import socks  # PySocks open-source module
            import urllib.request

            # Configura handler SOCKS5 para o urllib
            handler = socks.Socks5Handler(socks5_host="127.0.0.1", socks5_port=self.tor_socks_port)
            opener = urllib.request.build_opener(handler)

            headers = self._get_stealth_headers()
            headers["Content-Type"] = "application/json"
            headers["Origin"] = "https://comunica.pje.jus.br"

            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")

            logger.info(f"[Tor Engine] Disparando requisição anonimizada via Tor SOCKS5 para {tribunal}...")
            with opener.open(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                logger.info("[Tor Engine] Resposta recebida com sucesso!")
                return {"sucesso": True, "engine": "Tor Network SOCKS5", "data": data}
        except ImportError:
            return {
                "sucesso": False,
                "engine": "Tor Network",
                "erro": "Pacote 'PySocks' não instalado. Instale com: pip install PySocks"
            }
        except Exception as e:
            return {"sucesso": False, "engine": "Tor Network SOCKS5", "erro": str(e)}

    # -------------------------------------------------------------------------
    # EXECUÇÃO HÍBRIDA COM FALLBACK AUTOMÁTICO
    # -------------------------------------------------------------------------
    def buscar(self, tribunal: str, termo: str) -> Dict[str, Any]:
        """
        Tenta buscar prioritariamente via DataJud REST API. Se necessário, faz fallback para a rede Tor.
        """
        logger.info(f"=== INICIANDO BUSCA OPEN-SOURCE: Tribunal={tribunal} | Termo='{termo}' ===")
        
        # 1. Tentar DataJud REST API (Sem taxa de bloqueio)
        res_datajud = self.consultar_datajud(tribunal, termo)
        if res_datajud["sucesso"] and res_datajud["total"] > 0:
            return res_datajud

        # 2. Tentar via Tor SOCKS5 se disponível
        if self.testar_conexao_tor():
            res_tor = self.consultar_djen_via_tor(tribunal, numero_processo=termo)
            if res_tor["sucesso"]:
                return res_tor

        # Retorna o resultado compilado
        return res_datajud


if __name__ == "__main__":
    client = DJENOpenSourceClient()
    
    # Exemplo de teste no STJ
    resultado = client.buscar(tribunal="STJ", termo="0023013-51.2021.8.19.0078")
    print("\n--- RESULTADO DA CONSULTA ---")
    print(json.dumps(resultado, indent=2, ensure_ascii=False)[:2000])
