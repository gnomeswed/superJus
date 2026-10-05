@echo off
title Comite Juridico Estrategico - SuperJus
cd /d "c:\Projetos\superJus"
echo ========================================================
echo        SUPERJUS — COMITE JURIDICO ESTRATEGICO
echo          (MESA REDONDA MULTIAGENTE DE CASOS)
echo ========================================================
echo.
set /p CLIENTE="Digite o nome da pasta do cliente (ex: Julio_Pereira_Marcos): "
if "%CLIENTE%"=="" set CLIENTE=Julio_Pereira_Marcos

python "c:\Projetos\superJus\.agents\skills\debate_juridico_multiagente\scripts\debate_juridico_cli.py" --cliente "%CLIENTE%"
echo.
pause
