@echo off
title Prediccion Precio Gasolina - Streamlit Web App
cd /d "%~dp0"

echo ==========================================================
echo   Iniciando Aplicacion Web: Prediccion de Gasolina
echo ==========================================================
echo.

if exist ".venv\Scripts\streamlit.exe" (
    echo Iniciando entorno virtual y abriendo navegador...
    ".venv\Scripts\streamlit.exe" run app.py
) else (
    echo Entorno .venv no detectado directamente, buscando streamlit en el sistema...
    where streamlit >nul 2>nul
    if %errorlevel% equ 0 (
        streamlit run app.py
    ) else (
        echo [ERROR] No se encontro Streamlit instalado.
        echo Por favor instala las dependencias con: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

pause
