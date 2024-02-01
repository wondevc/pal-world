@echo off
setlocal

set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"
set "scripts_directory=%base_scripts_directory%\restart-scripts"

set "log_file_name=StartLog.txt"
set "log_directory=%scripts_directory%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

set "pal_server_path=%base_directory%\SteamCMD\steamapps\common\PalServer\PalServer.exe"

set "stop_script_path=%scripts_directory%\PalworldServerStop.bat"
call %stop_script_path%

set "update_script_path=%base_scripts_directory%\update-scripts\PalworldUpdate.bat"
call %update_script_path%

echo [%DATE% %TIME%] Restarting Palworld server. >> %log_file_path%
start "" "%pal_server_path%"

endlocal