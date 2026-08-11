@echo off
rem ============================================================
rem All The Leisures - 开发者符号链接(打通工作区与开发实例)
rem 作用:把 开发实例 的 config/kubejs/scripts 链接到 工作区
rem       让"在实例里改脚本" == "改工作区文件",避免手动复制
rem
rem 用法:
rem   setup_dev_link.bat <工作区路径> <实例路径>  建立链接
rem   setup_dev_link.bat --remove <实例路径>      断开链接
rem
rem 示例:
rem   setup_dev_link.bat D:\Code\atl-modpack "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
rem ============================================================
setlocal
chcp 65001 >nul

set "MODE=%1"
set "WORKSPACE=%2"
set "INSTANCE=%3"

rem ---- 处理 --remove 模式 ----
if /i "%MODE%"=="--remove" (
    set "INSTANCE=%2"
    goto :remove
)

if "%WORKSPACE%"=="" goto :usage
if "%INSTANCE%"=="" goto :usage

echo [*] 工作区: %WORKSPACE%
echo [*] 实例:   %INSTANCE%

rem ---- 需要链接的目录 ----
set "LINK_DIRS=config kubejs scripts"

for %%d in (%LINK_DIRS%) do (
    echo.
    echo [%%d] 建立链接...
    rem 1. 备份实例里已有的真实目录(如果有)
    if exist "%INSTANCE%\%%d" (
        if not exist "%INSTANCE%\%%d.bak" (
            echo   [*] 备份实例的 %%d 到 %%d.bak
            move "%INSTANCE%\%%d" "%INSTANCE%\%%d.bak" >nul
        )
    )
    rem 2. 建立 junction(不需要管理员权限)
    mklink /J "%INSTANCE%\%%d" "%WORKSPACE%\%%d" >nul 2>&1
    if errorlevel 1 (
        echo   [错误] 建立 %%d 链接失败(目标已存在?)
    ) else (
        echo   [✓] 已链接 %%d -> 工作区
    )
)

echo.
echo [完成] 开发实例的 config/kubejs/scripts 已指向工作区。
echo 在实例里改脚本 = 改工作区文件,git 立即可见。
echo 注意:发布时 python tools/push.py 会自动 packwiz refresh。
pause
exit /b 0

:remove
echo [*] 断开链接...
for %%d in (config kubejs scripts) do (
    if exist "%INSTANCE%\%%d" (
        rem 检查是否是 junction
        fsutil reparsepoint query "%INSTANCE%\%%d" >nul 2>&1
        if errorlevel 1 (
            echo   [%%d] 是真实目录,跳过
        ) else (
            echo   [*] 移除 %%d 链接
            rmdir "%INSTANCE%\%%d" >nul 2>&1
            rem 恢复备份
            if exist "%INSTANCE%\%%d.bak" (
                echo   [*] 恢复 %%d.bak
                move "%INSTANCE%\%%d.bak" "%INSTANCE%\%%d" >nul
            )
        )
    )
)
echo [完成] 已断开链接。
pause
exit /b 0

:usage
echo 用法:
echo   setup_dev_link.bat ^<工作区路径^> ^<实例路径^>
echo   setup_dev_link.bat --remove ^<实例路径^>
echo.
echo 示例:
echo   setup_dev_link.bat D:\Code\atl-modpack "D:\Minecraft\.minecraft\versions\All The Leisures v1.0.1b"
pause
exit /b 1
