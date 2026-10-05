@echo off
title Super Analista Juridico - Inicializador
color 0A
echo ====================================================
echo    Iniciando o Motor do Super Analista Juridico...
echo ====================================================
echo.
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "ROOT=%%~fI"
if not exist "%ROOT%\.venv\Scripts\activate.bat" (
  echo [ERRO] .venv nao encontrado em %ROOT%\.venv
  echo        Crie com: py -3.11 -m venv .venv  na raiz e instale requirements.
  pause & exit /b 1
)
where python >nul 2>&1 || set "PATH=%ROOT%\.venv\Scripts;%PATH%"
call "%ROOT%\.venv\Scripts\activate.bat"
python -m streamlit --version >nul 2>&1 || (echo [ERRO] streamlit ausente. Rode: pip install -r requirements.txt & pause & exit /b 1)
echo [OK] raiz=%ROOT%
python -m streamlit run "%ROOT%\core\app.py"
if errorlevel 1 (
  echo [ERRO] Streamlit encerrou com codigo %errorlevel%.
)
pause
