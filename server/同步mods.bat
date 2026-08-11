@echo off
rem ============================================================
rem All The Leisures — 服务器端 mods 同步
rem 用法:双击运行。放在服务器根目录(与 run.bat 同级)。
rem 流程:从 Pages 拉取 server/both 侧 mods → 提示开服
rem ============================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

rem ---- 更新包 URL(发布时替换为真实 Pages 地址)----
set "PACK_URL=https://USER.github.io/atl-modpack/pack.toml"

rem ---- 检查 bootstrap ----
if not exist "packwiz-installer-bootstrap.jar" (
    echo [错误] 缺少 packwiz-installer-bootstrap.jar
    echo 请从导入包中复制 bootstrap 到服务器根目录。
    pause
    exit /b 1
)

echo [同步] 更新服务器 mods (仅 server/both 侧,跳过纯客户端 mods)...
java -jar packwiz-installer-bootstrap.jar -g -s server "%PACK_URL%"
if errorlevel 1 (
    echo [错误] 同步失败。请检查网络后重试。
    pause
    exit /b 1
)

echo [完成] mods 已同步。请运行 run.bat 开服。
pause
