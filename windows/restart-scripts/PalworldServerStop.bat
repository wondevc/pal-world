@echo off
setlocal

set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"
set "scripts_directory=%base_scripts_directory%\restart-scripts"

set "log_file_name=StopLog.txt"
set "log_directory=%scripts_directory%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

set "backup_script_path=%scripts_directory%\backup-scripts\PalworldBackup.bat"
call %backup_script_path%

echo [%DATE% %TIME%] Stop Palworld server. >> %log_file_path%
taskkill /f /im "PalServer-Win64-Test-Cmd.exe"
taskkill /f /im "PalServer.exe"

endlocal