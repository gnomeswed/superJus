# -*- coding: utf-8 -*-
"""Adiciona mimo-v2.5 e muse-spark aos grupos do Hermes via config.yaml (path seguro)."""
import sys, json
sys.path.insert(0, r"C:\Users\Administrator\AppData\Local\hermes\hermes-agent")
from hermes_cli.config import load_config, save_config

cfg = load_config()
providers = cfg.get("providers", {})

# 1. Adicionar mimo-v2.5 e mimo-v2.5-pro ao CommandCode (já funcionam via cmc/)
cmc = providers.get("commandcode_router", {})
cmc_models = cmc.get("models", {})
cmc_models["cmc/xiaomi/mimo-v2.5"] = {}
cmc_models["cmc/xiaomi/mimo-v2.5-pro"] = {}
cmc["models"] = cmc_models
providers["commandcode_router"] = cmc
print("CommandCode models:", list(cmc_models.keys()))

# 2. Adicionar muse-spark ao grupo NVIDIA (que já aponta para o 9router... na real direto)
#    O grupo nvidia_router aponta direto para a NVIDIA (404 no muse-spark).
#    O muse-spark SÓ funciona via Meta (prefixo meta/ no 9router).
#    Vamos criar um grupo meta_router apontando para o 9router.
gateway_key = "sk-2c91384fe37bbeae-vcroo4-fb5f571c"
meta_router = {
    "name": "Meta",
    "base_url": "http://127.0.0.1:20128/v1",
    "api_key": gateway_key,
    "discover_models": False,
    "extra_headers": {"X-9router-Origin": "meta"},
    "models": {
        "meta/muse-spark-1.2": {},
        "meta/muse-spark-1.1": {},
        "meta/muse-glimmer-30b": {},
    },
}
providers["meta_router"] = meta_router
print("Meta router criado:", list(meta_router["models"].keys()))

cfg["providers"] = providers
save_config(cfg, strip_defaults=False)
print("CONFIG SALVA COM SUCESSO")
