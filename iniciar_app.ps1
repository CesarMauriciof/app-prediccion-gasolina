# Script PowerShell para iniciar la aplicación web
Set-Location -Path $PSScriptRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Iniciando Aplicación Web: Predicción de Gasolina" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$streamlitVenv = Join-Path $PSScriptRoot ".venv\Scripts\streamlit.exe"

if (Test-Path $streamlitVenv) {
    Write-Host "Ejecutando con el entorno virtual .venv..." -ForegroundColor Green
    & $streamlitVenv run app.py
} else {
    Write-Host "Ejecutando con Streamlit global..." -ForegroundColor Yellow
    streamlit run app.py
}
