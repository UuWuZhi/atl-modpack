@echo off
rem ============================================================
rem All The Leisures - Server Update Only
rem Place in server root, next to run.bat.
rem Updates server/both mods and tracked config/kubejs/scripts.
rem Client-only mods are skipped.
rem Pass "nopause" to skip pause.
rem ============================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

rem ---- Pack URL ----
set "PACK_URL=https://uuwuzhi.github.io/atl-modpack/pack.toml"

rem ---- Check bootstrap ----
if not exist "packwiz-installer-bootstrap.jar" (
    echo [ERROR] packwiz-installer-bootstrap.jar not found.
    echo Copy it from bootstrap/ to the server root.
    if /i not "%~1"=="nopause" pause
    exit /b 1
)

rem ---- Detect Java 21 (JAVA_EXE override, system PATH, or common server folders) ----
if defined JAVA_EXE (
    "%JAVA_EXE%" -version >nul 2>nul
    if not errorlevel 1 goto :found_java
)
set "JAVA_EXE="
where java >nul 2>nul && set "JAVA_EXE=java"
if defined JAVA_EXE goto :found_java
if exist "java\bin\java.exe" (
    set "JAVA_EXE=java\bin\java.exe"
    goto :found_java
)
if exist "jdk\bin\java.exe" (
    set "JAVA_EXE=jdk\bin\java.exe"
    goto :found_java
)
if exist "runtime\bin\java.exe" (
    set "JAVA_EXE=runtime\bin\java.exe"
    goto :found_java
)

:found_java
if not defined JAVA_EXE (
    echo [ERROR] Java not found. Install Java 21 or set JAVA_EXE.
    if /i not "%~1"=="nopause" pause
    exit /b 1
)

echo [UPDATE] Checking server updates...
echo          Installing server/both mods and tracked config/kubejs/scripts.
echo          Client-only mods are skipped.
"%JAVA_EXE%" -jar packwiz-installer-bootstrap.jar -g -s server --bootstrap-no-update "%PACK_URL%"
if errorlevel 1 (
    echo [ERROR] Server update failed. Check network and retry.
    if /i not "%~1"=="nopause" pause
    exit /b 1
)

echo [DONE] Server files are up to date. Run run.bat to start the server.
if /i not "%~1"=="nopause" pause
endlocal
