@echo off
setlocal

:start

set "monitor_script_path=.\monitor-scripts\PalworldMemoryMonitor.bat"
call %monitor_script_path%

for /f "tokens=1-3 delims=:." %%a in ("%TIME%") do (
    set /a "minutes=%%a*60 + 1%%b%%100"
)

set /a "backup_trigger=minutes %% 5"

set "backup_script_path=..\backup-scripts\PalworldBackup.bat"
set "flag_file_path=.\backup-flag.txt"

if %backup_trigger% equ 0 (
    if not exist %flag_file_path% (
        @REM call %backup_script_path%
        echo backup start.
    )
)

timeout /t 60 /nobreak >nul
goto start