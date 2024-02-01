@echo off
setlocal enabledelayedexpansion

set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"
set "scripts_directory=%base_scripts_directory%\monitor-scripts"

set "log_file_name=MemoryUsageLog.txt"
set "log_directory=%scripts_directory%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

set "PAL_SERVER_PROCESS1=PalServer.exe"
set "PAL_SERVER_PROCESS2=PalServer-Win64-Test-Cmd.exe"

@REM MAX_MEMORY_THRESHOLD is MB.
set "MAX_MEMORY_THRESHOLD=16384"

set "restart_script_path=%base_scripts_directory%\restart-scripts\PalworldServerStop.bat"

tasklist | find /i "PalServer.exe" > nul
if %errorlevel% neq 0 (
    call %restart_script_path%
) else (
    echo [%DATE% %TIME%] Program running normally. >> %log_file_path%
)

set "TOTAL_MEMORY_USAGE=0"

for /f %%a in ('wmic process where "Name='%PAL_SERVER_PROCESS1%'" get WorkingSetSize^|findstr [0-9]') do (
    set "MEMORY1=%%a"
    set "MEGABYTES1="
    for /f %%b in ('powershell -command "[math]::Round([float]::Parse(!MEMORY1!) / 1MB)"') do set "MEGABYTES1=%%b"
)

for /f %%a in ('wmic process where "Name='%PAL_SERVER_PROCESS2%'" get WorkingSetSize^|findstr [0-9]') do (
    set "MEMORY2=%%a"
    set "MEGABYTES2="
    for /f %%b in ('powershell -command "[math]::Round([float]::Parse(!MEMORY2!) / 1MB)"') do set "MEGABYTES2=%%b"
)

if defined MEGABYTES1 set /a TOTAL_MEMORY_USAGE+=%MEGABYTES1%
if defined MEGABYTES2 set /a TOTAL_MEMORY_USAGE+=%MEGABYTES2%

echo [%DATE% %TIME%] %TOTAL_MEMORY_USAGE% MB >> %log_file_path%

echo [%DATE% %TIME%] Total Memory Usage: %TOTAL_MEMORY_USAGE% MB

if %TOTAL_MEMORY_USAGE% gtr %MAX_MEMORY_THRESHOLD% (
    echo [%DATE% %TIME%] Memory usage exceeds the threshold. >> %log_file_path%
    
    call %restart_script_path%
)

endlocal