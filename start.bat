@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 设置标题
title 程序启动器

:: 检查 Python 是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python未安装或未添加到环境变量！
    echo 请安装Python并确保添加到环境变量。
    pause
    exit /b 1
)

:: 检查必要的文件是否存在
if not exist "gui_main.py" (
    echo 错误：找不到主程序文件 gui_main.py
    pause
    exit /b 1
)

:: 检查并创建必要的目录
if not exist "output" mkdir output
if not exist "resource" mkdir resource

:: 尝试启动程序
echo 正在启动程序...
python gui_main.py

if %errorlevel% neq 0 (
    echo 程序运行出错！
    echo 错误代码：%errorlevel%
    pause
) else (
    echo 程序已正常结束
    timeout /t 3
) 