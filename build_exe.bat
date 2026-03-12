@echo off
chcp 65001 >nul
echo ========================================
echo 每日报表生成器 - Windows 构建脚本
echo ========================================

REM 创建虚拟环境
if not exist venv (
    echo [1/4] 创建虚拟环境...
    python -m venv venv
) else (
    echo [1/4] 虚拟环境已存在
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo [2/4] 安装依赖...
pip install -r requirements.txt -q

REM 清理旧构建
echo [3/4] 清理旧构建...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist output mkdir output

REM 执行 PyInstaller
echo [4/4] 执行 PyInstaller 打包...
pyinstaller --onefile --windowed --name DailyReport --icon=report_app/resources/app_icon.ico app.py

REM 复制 EXE 到 output
if exist dist\DailyReport.exe (
    copy dist\DailyReport.exe output\ >nul
    echo.
    echo ========================================
    echo ✅ 构建成功！
    echo 输出文件：output\DailyReport.exe
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ❌ 构建失败！
    echo ========================================
    exit /b 1
)

pause
