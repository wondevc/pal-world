@echo off
setlocal

set "base_directory=D:\pal-world"
set "base_scripts_directory=%base_directory%\windows"
set "scripts_directory=%base_scripts_directory%\update-scripts"

set "log_file_name=UpdateLog.txt"
set "log_directory=%scripts_directory%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

set "steamcmd_directory=%base_directory%\SteamCMD"
set "steamcmd_path=%steamcmd_directory%\steamcmd.exe"

set "app_id=2394010"

set "seven_zip_path=C:\Program Files\7-Zip\7z.exe"

set "steamcmd_zip_path=%scripts_directory%\steamcmd.zip"

if not exist "%steamcmd_directory%" (
    mkdir "%steamcmd_directory%"
    echo [%DATE% %TIME%] Created steamcmd directory. >> %log_file_path%
)

if not exist "%steamcmd_path%" (
    if not exist "%seven_zip_path%" (
        echo [%DATE% %TIME%] Backup failed because 7-Zip is not installed. >> %log_file_path%

        endlocal

        exit /b
    )

    curl -o %steamcmd_zip_path% https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip

    "%seven_zip_path%" x "%steamcmd_zip_path%" -o"%steamcmd_directory%" -y

    del "%steamcmd_zip_path%"
)

start "" /wait %steamcmd_path% +login anonymous +app_update %app_id% validate +quit

echo [%DATE% %TIME%] Update Completed. >> %log_file_path%

endlocal

exit /b