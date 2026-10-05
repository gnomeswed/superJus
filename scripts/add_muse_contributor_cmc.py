# -*- coding: utf-8 -*-
"""Adiciona meta/muse-spark-1.2-contributor ao grupo CommandCode do Hermes."""
import sys
sys.path.insert(0, r"C:\Users\Administrator\AppData\Local\hermes\hermes-agent")
from hermes_cli.config import load_config, save_config

cfg = load_config()
providers = cfg.get("providers", {})

# 1. Adicionar ao CommandCode
cmc = providers.get("commandcode_router", {})
cmc_models = cmc.get("models", {})
cmc_models["cmc/meta/muse-spark-1.2-contributor"] = {}
cmc["models"] = cmc_models
providers["commandcode_router"] = cmc
print("CommandCode agora:", len(cmc_models), "modelos")

# 2. Remover o grupo Meta criado anteriormente (muse-spark-1.2 sem sufixo não é o que o usuário quer)
#    O usuário quer usar via CommandCode. Vamos manter o grupo Meta só com muse-glimmer (que está no NVIDIA também),
#    ou remover o grupo inteiro para não poluir.
if "meta_router" in providers:
    del providers["meta_router"]
    print("Grupo Meta removido (muse-spark vai pelo CommandCode)")

cfg["providers"] = providers
save_config(cfg, strip_defaults=False)
print("CONFIG SALVA")
