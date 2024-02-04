import time
import datetime
import tarfile
import psutil
from pathlib import Path

DATE_FORMMAT = '%Y-%m-%d'
TIME_FORMMAT = '%H-%M-%S'
DATETIME_FORMMAT = f'{DATE_FORMMAT} {TIME_FORMMAT}'

PAL_SERVER_PROCESS1 = 'PalServer.exe'
PAL_SERVER_PROCESS2 = 'PalServer-Win64-Test-Cmd.exe'

MAX_MEMORY_THRESHOLD_MB = 16384

BASE_DIR = Path.cwd()

BACKUP_DIR = BASE_DIR / 'backup'
BACKUP_FILE_DIR = BACKUP_DIR / 'backups'
BACKUP_LOG_DIR = BACKUP_DIR / 'logs'
BACKUP_LOG_FILE_NAME = 'BackupLog.txt'

MEMORY_MONITOR_DIR = BASE_DIR / 'monitor' / 'memory'
MEMORY_MONITOR_LOG_DIR = MEMORY_MONITOR_DIR / 'logs'
MEMORY_MONITOR_LOG_FILE_NAME = 'MemoryUsageLog.txt'

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
        with backup_log_file_path.open("a") as file:
            print(f"[{current_datetime}] Created Log File.", file=file)

    backup_file_directory = BACKUP_FILE_DIR / current_date

    if not backup_file_directory.exists():
        print("Create backup file directory...")
        backup_file_directory.mkdir(parents=True)

    backup_file_name = f'PalServer_Backup_{int(time.time())}.tar.gz'
    backup_file_path = backup_file_directory / backup_file_name

    if PAL_SAVE_DIR.exists():
        with tarfile.open(backup_file_path.resolve(), "w:gz") as tar:
            tar.add(PAL_SAVE_DIR, arcname=PAL_SAVE_DIR.name)

def memory_monitoring_task():
    current_raw_datetime = time.localtime()
    current_date = time.strftime(DATE_FORMMAT, current_raw_datetime)
    current_datetime = time.strftime(DATETIME_FORMMAT, current_raw_datetime)

    memory_monitor_log_directory = MEMORY_MONITOR_LOG_DIR / current_date

    if not memory_monitor_log_directory.exists():
        print("Create memory log directory...")
        memory_monitor_log_directory.mkdir(parents=True)

    memory_monitor_log_file_path = memory_monitor_log_directory / MEMORY_MONITOR_LOG_FILE_NAME
    
    if not memory_monitor_log_file_path.exists():
        with memory_monitor_log_file_path.open("a") as file:
            print(f"[{current_datetime}] Created Log File.", file=file)

    process1_usage_memory = 0
    process2_usage_memory = 0

    for proc in psutil.process_iter():
        if PAL_SERVER_PROCESS1 in proc.name():
            process1_usage_memory = proc.memory_info().rss
        if PAL_SERVER_PROCESS2 in proc.name():
            process2_usage_memory = proc.memory_info().rss
        
        if process1_usage_memory > 0 and process2_usage_memory > 0:
            break
    
    total_usage_memory = process1_usage_memory + process2_usage_memory
    total_usage_memory_mb = int(total_usage_memory / (1024 * 1024))

    with memory_monitor_log_file_path.open('a') as file:
        print(f"[{current_datetime}] Total Memory Usage: {total_usage_memory_mb} MB", file=file)

    if total_usage_memory_mb >= MAX_MEMORY_THRESHOLD_MB:
        with memory_monitor_log_file_path.open("a", encoding="utf-8") as file:
            file.write(f"[{current_datetime}] Memory usage exceeds the threshold.")

        # todo restart task

try:
    while True:
        current_time = int(time.time())

        if current_time % 5 == 0:
            memory_monitoring_task()

        if current_time % 300 == 0:
            backup_task()

        if current_time % 432000 == 0:
            # TODO
            print("update check")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("stop executor.")