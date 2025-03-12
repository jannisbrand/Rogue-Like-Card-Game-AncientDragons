@echo off
set "BASE_DIR=%~dp0Ancient-Dragons"
set "TARGET_DIR=%BASE_DIR%\.venv"
set "REQ_FILE=%BASE_DIR%\requirements.txt"
set "MAIN_SCRIPT=main.py"

if exist "%TARGET_DIR%" (
    echo Der Ordner .venv existiert.
) else (
    echo Der Ordner .venv existiert nicht.
    echo Erstelle virtuelle Umgebung...
    python -m venv "%TARGET_DIR%"
    echo Aktiviere virtuelle Umgebung...
    call "%TARGET_DIR%\Scripts\activate"
    if exist "%REQ_FILE%" (
        echo Installiere Abhaengigkeiten aus requirements.txt...
        pip install -r "%REQ_FILE%"
    ) else (
        echo Keine requirements.txt gefunden. Beende das Skript.
        exit /b
    )
)

echo Aktiviere virtuelle Umgebung...
call "%TARGET_DIR%\Scripts\activate"

cd /d "%BASE_DIR%"
echo Starte main.py...
python "%MAIN_SCRIPT%"

exit /b
