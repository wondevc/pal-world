@echo off
setlocal

set "log_file_name=StartLog.txt"
set "log_directory=%cd%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

set "steamcmd_directory=..\..\SteamCMD"
set "pal_server_path=%steamcmd_directory%\steamapps\common\PalServer\PalServer.exe"

set "stop_script_path=..\restart-scripts\PalworldServerStop.bat"
call %stop_script_path%

echo [%DATE% %TIME%] Restarting Palworld server. >> %log_file_path%
start "" "%pal_server_path%"

endlocal