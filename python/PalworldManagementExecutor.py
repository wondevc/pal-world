import time
import datetime
import tarfile
from pathlib import Path

DATE_FORMMAT = '%Y-%m-%d'
TIME_FORMMAT = '%H-%M-%S'
DATETIME_FORMMAT = f'{DATE_FORMMAT} {TIME_FORMMAT}'

BASE_DIR = Path.cwd()

BACKUP_DIR = BASE_DIR / 'backup'
BACKUP_FILE_DIR = BACKUP_DIR / 'backups'
BACKUP_LOG_DIR = BACKUP_DIR / 'logs'
BACKUP_LOG_FILE_NAME = 'BackupLog.txt'

STEAMCMD_DIR = BASE_DIR / '..' / 'SteamCMD'
PAL_SAVE_DIR = STEAMCMD_DIR / 'steamapps' / 'common'/ 'PalServer' / 'Pal' / 'Saved'

def backup_task():
    current_raw_datetime = time.localtime()
    current_date = time.strftime(DATE_FORMMAT, current_raw_datetime)
    current_datetime = time.strftime(DATETIME_FORMMAT, current_raw_datetime)
    backup_log_directory = BACKUP_LOG_DIR / current_date

    if not backup_log_directory.exists():
        print("Create backup log directory...")
        backup_log_directory.mkdir(parents=True)

    backup_log_file_path = backup_log_directory / BACKUP_LOG_FILE_NAME

    if not backup_log_file_path.exists():
        with backup_log_file_path.open("w", encoding="utf-8") as file:
            file.write(f"[{current_datetime}] Created Log File.")

    backup_file_directory = BACKUP_FILE_DIR / current_date

    if not backup_file_directory.exists():
        print("Create backup file directory...")
        backup_file_directory.mkdir(parents=True)

    backup_file_name = f'PalServer_Backup_{int(time.time())}.tar.gz'
    backup_file_path = backup_file_directory / backup_file_name

    if PAL_SAVE_DIR.exists():
        with tarfile.open(backup_file_path.resolve(), "w:gz") as tar:
            tar.add(PAL_SAVE_DIR, arcname=PAL_SAVE_DIR.name)

try:
    while True:
        current_time = int(time.time())

        if current_time % 5 == 0:
            # TODO
            print("memory monitoring")

        if current_time % 300 == 0:
            backup_task()

        if current_time % 432000 == 0:
            # TODO
            print("update check")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("stop executor.")