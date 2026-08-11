@echo off
rem ============================================================
rem All The Leisures — 一键更新 + 启动
rem 用法:双击运行。放在整合包版本目录内(.minecraft/versions/All The Leisures v1.0.1b/)
rem 流程:检查更新(增量)→ 打开 PCL2 → 玩家点启动
rem ============================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

rem ---- 更新包 URL(发布时替换为真实 Pages 地址)----
set "PACK_URL=https://USER.github.io/atl-modpack/pack.toml"

rem ---- 检查 bootstrap ----
if not exist "packwiz-installer-bootstrap.jar" (
    echo [错误] 缺少 packwiz-installer-bootstrap.jar
    echo 请重新下载完整导入包,或手动将 bootstrap 放到本目录。
    pause
    exit /b 1
)

rem ---- 自动探测 Java 21 (PCL2 自带,或系统 PATH)----
set "JAVA_EXE="
where java >nul 2>nul && set "JAVA_EXE=java"
if not defined JAVA_EXE (
    rem 常见 PCL2 Java 目录:版本目录的 PCL 子目录 / 上级 .minecraft 目录
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
    echo [错误] 未找到 Java。请安装 Java 21 (JDK),或把 PCL2 的 java 完整路径填到下方。
    pause
    exit /b 1
)

echo [1/2] 检查更新中... (首次运行会下载全部 mods,约 562MB,请耐心)
"%JAVA_EXE%" -jar packwiz-installer-bootstrap.jar -g "%PACK_URL%"
if errorlevel 1 (
    echo [错误] 更新失败。请检查网络后重试。
    pause
    exit /b 1
)

echo [2/2] 打开启动器,请点击启动...
if exist "Plain Craft Launcher.exe" (
    start "" "Plain Craft Launcher.exe"
) else (
    echo [提示] 未找到 Plain Craft Launcher.exe,请手动打开 PCL2。
)
endlocal
