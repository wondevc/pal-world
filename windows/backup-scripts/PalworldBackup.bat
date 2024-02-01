@echo off
setlocal enabledelayedexpansion

set "base_backup_directory=%cd%\.backups"
set "backup_directory=%base_backup_directory%\%DATE%"

set "log_file_name=BackupLog.txt"
set "log_directory=%cd%\logs\%DATE%"
set "log_file_path=%log_directory%\%log_file_name%"

if not exist "%log_directory%" (
    mkdir "%log_directory%"
)

if not exist "%base_backup_directory%" (
    mkdir "%base_backup_directory%"
    echo [%DATE% %TIME%] Created base backup directory. >> %log_file_path%
)

if not exist "%backup_directory%" (
    mkdir "%backup_directory%"
    echo [%DATE% %TIME%] Created backup directory. >> %log_file_path%
)

echo [%DATE% %TIME%] Backup starting the PalWorld. >> %log_file_path%

for /f "delims=" %%a in ('wmic OS Get localdatetime ^| find "."') do set datetime=%%a
set timestamp=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!_!datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!

set "backup_file_name=PalServer_Backup_%timestamp%.zip"
set "backup_file_path=%backup_directory%\%backup_file_name%"

set "seven_zip_path=C:\Program Files\7-Zip\7z.exe"

if not exist "%seven_zip_path%" (
    echo [%DATE% %TIME%] Backup failed because 7-Zip is not installed. >> %log_file_path%

    endlocal

    exit /b
)

set "source_directory=..\..\SteamCMD\steamapps\common\PalServer\Pal\Saved"

if not exist "%source_directory%" (
    echo [%DATE% %TIME%] Backup failed because PalServer is not found. >> %log_file_path%

    endlocal

    exit /b
)

%seven_zip_path% a -r -tzip %backup_file_path% %source_directory%

echo [%DATE% %TIME%] Backup completed for name %backup_file_name%. >> %log_file_path%

endlocal

exit /b