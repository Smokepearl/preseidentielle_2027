@echo off
REM Lanceur de l'application - Presidentielle 2027 (LFI)
REM Double-cliquez sur ce fichier pour ouvrir la demo

cd /d "%~dp0"
echo ============================================
echo   Lancement de l'application LFI 2027...
echo   (laissez cette fenetre ouverte pendant la demo)
echo ============================================
echo.
python -m streamlit run app_lfi_2027.py

pause
