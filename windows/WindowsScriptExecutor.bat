@echo off
setlocal

set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"

set "restart_script_path=%base_scripts_directory%\restart-scripts\PalworldServerRestart.bat"
set "monitor_script_path=%base_scripts_directory%\monitor-scripts\PalworldMemoryMonitor.bat"
set "backup_script_path=%base_scripts_directory%\backup-scripts\PalworldBackup.bat"

echo Starting Palworld...
call %restart_script_path%
echo Hello Palworld!!

:start
echo Memory usage monitoring....
call %monitor_script_path%

for /f "tokens=1-3 delims=:." %%a in ("%TIME%") do (
    set /a "minutes=%%a*60 + 1%%b%%100"
)

set /a "backup_trigger=minutes %% 5"

if %backup_trigger% equ 0 (
    echo Execute backup...
    call %backup_script_path%
)

set /a "update_trigger=minutes %% 120"

if %update_trigger% equ 0 (
    echo Update check...

    echo %update_state% | find /i "No Error" >nul
    if %errorlevel% equ 0 (
        echo It's already the latest version.
    ) else (
        call %restart_script_path%
    )
)

timeout /t 60 /nobreak >nul
goto start