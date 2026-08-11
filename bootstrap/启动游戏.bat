@echo off
rem ============================================================
rem All The Leisures — 一键更新 + 启动
rem 用法:双击运行。放在整合包版本目录内(.minecraft/versions/All The Leisures v1.0.1b/)
rem 流程:先增量更新(复用 仅更新.bat)→ 再打开 PCL2
rem 不喜欢用这个脚本启动的人,可以改用 仅更新.bat,更新完手动在 PCL2 里点启动
rem ============================================================
setlocal
chcp 65001 >nul
cd /d "%~dp0"

rem 先执行更新(传 nopause 不弹暂停,更新失败会自行报错退出)
call "仅更新.bat" nopause
if errorlevel 1 (
    echo [错误] 更新未完成,游戏未启动。
    pause
    exit /b 1
)

echo [启动] 打开启动器,请点击启动...
if exist "Plain Craft Launcher.exe" (
    start "" "Plain Craft Launcher.exe"
) else (
    echo [提示] 未找到 Plain Craft Launcher.exe,请手动打开 PCL2。
)
endlocal
