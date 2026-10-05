# -*- coding: utf-8 -*-
"""Adiciona o grupo OpenRouter ao config do Hermes."""
import sys
sys.path.insert(0, r"C:\Users\Administrator\AppData\Local\hermes\hermes-agent")
from hermes_cli.config import load_config, save_config

cfg = load_config()
providers = cfg.get("providers", {})

gateway_key = "sk-2c91384fe37bbeae-vcroo4-fb5f571c"
or_router = {
    "name": "OpenRouter",
    "base_url": "http://127.0.0.1:20128/v1",
    "api_key": gateway_key,
    "discover_models": False,
    "extra_headers": {"X-9router-Origin": "or"},
    "models": {
        "or/liquid/lfm-2.5-2.6b:free": {},
        "or/nvidia/nemotron-3.5-lightning:free": {},
        "or/poolside/laguna-s-2.1:free": {},
        "or/poolside/laguna-xs-2.1:free": {},
        "or/cohere/north-mini-code:free": {},
        "or/nvidia/nemotron-3.5-content-safety:free": {},
        "or/nvidia/nemotron-3-ultra-550b-a55b:free": {},
        "or/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": {},
        "or/google/gemma-4-26b-a4b-it:free": {},
        "or/google/gemma-4-31b-it:free": {},
        "or/nvidia/nemotron-3-super-120b-a12b:free": {},
        "or/nvidia/nemotron-3-nano-30b-a3b:free": {},
        "or/nvidia/nemotron-nano-12b-v2-vl:free": {},
        "or/nvidia/nemotron-nano-9b-v2:free": {},
        "or/openai/gpt-oss-20b:free": {},
    },
}
providers["openrouter_router"] = or_router
cfg["providers"] = providers
save_config(cfg, strip_defaults=False)
print("OpenRouter group adicionado com", len(or_router["models"]), "modelos")
