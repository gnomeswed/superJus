@echo off
title Super Analista Juridico - Inicializador
color 0A

echo ====================================================
echo    Iniciando o Motor do Super Analista Juridico...
echo ====================================================
echo.
echo Por favor, aguarde enquanto os sistemas de IA sao carregados.
echo O seu navegador abrira automaticamente em alguns segundos.
echo.

:: Ativa o ambiente virtual e inicia o painel
call .\.venv\Scripts\activate.bat
python -m streamlit run app.py

:: Caso dê algum erro, a tela não fecha sozinha
pause
