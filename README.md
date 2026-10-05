# superJus — Super Analista Jurídico

## Instalação (Windows limpo)
```powershell
cd C:\Projetos\superJus
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install chromium
copy .env.example .env  # preencha DATAJUD_API_KEY, TELEGRAM_BOT_TOKEN, etc.
```
## Uso
- App: `.\.venv\Scripts\python -m streamlit run core/app.py` ou `scripts\INICIAR_SISTEMA.bat`
- Pipeline: `python -m scripts.run_pipeline 0011857-95.2024.8.19.0002 --out Clientes/Processo_X --demo`
- Diagnóstico: `python scripts/doctor.py`
- Testes: `python -m pytest tests -m "not live" -q` e `python -m pytest --cov=core --cov=scripts --cov-report=term-missing`

## Monitor 4h + Telegram
- `scripts/telegram_monitor_julio.py` (Estado `.agents/telegram_last_state.json`, deduplica por movimentação normalizada).
- Cron do Command Code: `cron_list` / `cron_create` com `0 8,12,16,20 * * *` (sem --force) — veja `.agents/telegram_last_state.json` para auditoria.
- Persistente: criar no Task Scheduler do Windows a cada 4h chamando `python scripts/telegram_monitor_julio.py` (sem --force) com `PYTHONIOENCODING=utf-8` e `DATAJUD_API_KEY` no ambiente.

## memU
- `python scripts/memu_store.py --name X --track memory --description "Y" --content "..."` e `python scripts/memu_retrieve.py "consulta"`.
- Intervalo do provider pode ser curto — use `python ...` com venv quando possível.

## Segredos
- Não versione `.env`, `scripts/telegram_config.json`, `scripts/discord_config.json`. Rotacione chaves expostas antes de qualquer release.

## Troubleshooting
- Portal TJRJ geobloqueia IP estrangeiro — VPS fora do BR pode precisar VPN/proxy brasileiro.
- `requirements.txt` vem sem PyPDF2 (use pypdf). Whisper é opcional e pesado.
