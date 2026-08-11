@echo off
rem ============================================================
rem All The Leisures - Update + Launch
rem Place in modpack version folder:
rem   .minecraft/versions/All The Leisures v1.0.1b/
rem Runs update (reuse 仅更新.bat), then opens PCL2.
rem ============================================================
setlocal
cd /d "%~dp0"

call "仅更新.bat" nopause
if errorlevel 1 (
    echo [ERROR] Update failed, game not launched.
    pause
    exit /b 1
)

echo [LAUNCH] Opening launcher...
if exist "Plain Craft Launcher.exe" (
    start "" "Plain Craft Launcher.exe"
) else (
    echo [NOTE] Plain Craft Launcher.exe not found, open PCL2 manually.
)
endlocal
