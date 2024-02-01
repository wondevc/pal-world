@echo off
setlocal

:start
set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"

set "monitor_script_path=%base_scripts_directory%\monitor-scripts\PalworldMemoryMonitor.bat"
echo Memory usage monitoring....
call %monitor_script_path%

for /f "tokens=1-3 delims=:." %%a in ("%TIME%") do (
    set /a "minutes=%%a*60 + 1%%b%%100"
)

set /a "backup_trigger=minutes %% 5"

set "backup_script_path=%base_scripts_directory%\backup-scripts\PalworldBackup.bat"

if %backup_trigger% equ 0 (
    echo Execute backup...
    call %backup_script_path%
)

timeout /t 60 /nobreak >nul
goto start