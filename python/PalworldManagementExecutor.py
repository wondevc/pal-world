import time
import tarfile
import psutil
import subprocess
from pathlib import Path

DATE_FORMMAT = '%Y-%m-%d'
TIME_FORMMAT = '%H-%M-%S'
DATETIME_FORMMAT = f'{DATE_FORMMAT} {TIME_FORMMAT}'

PAL_SERVER_PROCESS1 = 'PalServer.exe'
PAL_SERVER_PROCESS2 = 'PalServer-Win64-Test-Cmd.exe'

MAX_MEMORY_THRESHOLD_MB = 16384

BASE_DIR = Path.cwd()

COMMON_DIR = BASE_DIR / 'common'
COMMON_LOG_DIR = COMMON_DIR / 'logs'
COMMON_LOG_FILE_NAME = 'CommonLog.txt'

BACKUP_DIR = BASE_DIR / 'backup'
BACKUP_FILE_DIR = BACKUP_DIR / 'backups'
BACKUP_LOG_DIR = BACKUP_DIR / 'logs'
BACKUP_LOG_FILE_NAME = 'BackupLog.txt'

MEMORY_MONITOR_DIR = BASE_DIR / 'monitor' / 'memory'
MEMORY_MONITOR_LOG_DIR = MEMORY_MONITOR_DIR / 'logs'
MEMORY_MONITOR_LOG_FILE_NAME = 'MemoryUsageLog.txt'

STEAMCMD_DIR = BASE_DIR / '..' / 'SteamCMD'
PAL_SERVER_DIR = STEAMCMD_DIR / 'steamapps' / 'common'/ 'PalServer'
PAL_SERVER_EXECUTOR_PATH = PAL_SERVER_DIR / 'PalServer.exe'
PAL_SAVE_DIR = PAL_SERVER_DIR / 'Pal' / 'Saved'

def backup_task():
    current_raw_datetime = time.localtime()
    current_date = time.strftime(DATE_FORMMAT, current_raw_datetime)

    backup_file_directory = BACKUP_FILE_DIR / current_date

    if not backup_file_directory.exists():
        save_log(
            text="Create backup file directory...",
            path=BACKUP_LOG_DIR,
            file_name=BACKUP_LOG_FILE_NAME
        )
        backup_file_directory.mkdir(parents=True)

    backup_file_name = f'PalServer_Backup_{int(time.time())}.tar.gz'
    backup_file_path = backup_file_directory / backup_file_name

    if PAL_SAVE_DIR.exists():
        with tarfile.open(backup_file_path.resolve(), "w:gz") as tar:
            tar.add(PAL_SAVE_DIR, arcname=PAL_SAVE_DIR.name)

def memory_monitoring_task():
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

    save_log(
        text=f"Total Memory Usage: {total_usage_memory_mb} MB",
        path=MEMORY_MONITOR_LOG_DIR,
        file_name=MEMORY_MONITOR_LOG_FILE_NAME
    )

    if total_usage_memory_mb >= MAX_MEMORY_THRESHOLD_MB:
        save_log(
            text="Memory usage exceeds the threshold.",
            path=MEMORY_MONITOR_LOG_DIR,
            file_name=MEMORY_MONITOR_LOG_FILE_NAME
        )

        # todo restart task

def start_task():
    save_log(
        text="Start Palworld.",
        path=COMMON_LOG_DIR,
        file_name=COMMON_LOG_FILE_NAME
    )

    subprocess.call([PAL_SERVER_EXECUTOR_PATH])

def stop_task():
    backup_task()

    process1_pid = None
    process2_pid = None

    for proc in psutil.process_iter():
        if PAL_SERVER_PROCESS1 in proc.name():
            process1_pid = proc.pid
        if PAL_SERVER_PROCESS2 in proc.name():
            process2_pid = proc.pid

        if process1_pid is not None and process2_pid is not None:
            break
    
    if process1_pid is not None:
        process_kill_task(process1_pid)
    if process2_pid is not None:
        process_kill_task(process2_pid)

def process_kill_task(pid: int):
    save_log(
        text=f"Stop process... pid: {pid}",
        path=COMMON_LOG_DIR,
        file_name=COMMON_LOG_FILE_NAME
    )

    parent = psutil.Process(pid)
    parent.kill()

def save_log(text: str, path: Path, file_name: str):
    current_raw_datetime = time.localtime()
    current_date = time.strftime(DATE_FORMMAT, current_raw_datetime)
    current_datetime = time.strftime(DATETIME_FORMMAT, current_raw_datetime)

    log_path = path / current_date

    if not log_path.exists():
        print(f"{log_path} > [{current_datetime}] Create Log Directory...")
        log_path.mkdir(parents=True)
    
    log_file_path = log_path / file_name

    if not log_file_path.exists():
        with log_file_path.open('a') as file:
            print(f"[{current_datetime}] Created Log File.", file=file)

    print(f"[{current_datetime}] {text}")

    with log_file_path.open('a') as file:
        print(f"[{current_datetime}] {text}", file=file)

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