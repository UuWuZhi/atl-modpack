@echo off
rem ============================================================
rem All The Leisures - Update Only (no game launch)
rem Place in modpack version folder:
rem   .minecraft/versions/All The Leisures v1.0.1b/
rem Double-click to run. Pass "nopause" to skip pause.
rem ============================================================
setlocal
cd /d "%~dp0"

rem ---- Pack URL ----
set "PACK_URL=https://uuwuzhi.github.io/atl-modpack/pack.toml"

rem ---- Check bootstrap ----
if not exist "packwiz-installer-bootstrap.jar" (
    echo [ERROR] packwiz-installer-bootstrap.jar not found.
    echo Please re-import the modpack or copy bootstrap here.
    pause
    exit /b 1
)

rem ---- Detect Java 21 (PCL2 bundled, or system PATH) ----
set "JAVA_EXE="
where java >nul 2>nul && set "JAVA_EXE=java"
if not defined JAVA_EXE (
    if exist "PCL\java.exe" set "JAVA_EXE=PCL\java.exe"
)
if not defined JAVA_EXE (
    for /d %%d in ("..\..\*") do (
        if exist "%%d\PCL\java.exe" (
            set "JAVA_EXE=%%d\PCL\java.exe"
            goto :found_java
        )
    )
)
:found_java
if not defined JAVA_EXE (
    echo [ERROR] Java not found. Install Java 21 or set JAVA_EXE.
    pause
    exit /b 1
)

echo [UPDATE] Checking for updates...
echo          First run downloads all mods (~560MB), please wait.
"%JAVA_EXE%" -jar packwiz-installer-bootstrap.jar -g --bootstrap-no-update "%PACK_URL%"
if errorlevel 1 (
    echo [ERROR] Update failed. Check network and retry.
    pause
    exit /b 1
)

echo [DONE] Modpack is up to date.
if /i not "%~1"=="nopause" pause
endlocal
