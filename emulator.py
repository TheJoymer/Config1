
import os
import tarfile
import xml.etree.ElementTree as ET
import configparser
import subprocess
import time
from datetime import datetime

# Конфигурация
CONFIG_PATH = '/home/mint/Desktop/work/config.ini'
DEFAULT_PATH = '/home/mint/Desktop/work'
# Чтение конфигурационного файла
config = configparser.ConfigParser()

# Чтение из файла
config.read('config.ini')

# Функция для записи в лог
def log_action(action):
    log_file = os.path.join(DEFAULT_PATH, 'log.xml')
    log_entry = ET.Element('log_entry')
    ET.SubElement(log_entry, 'action').text = action
    ET.SubElement(log_entry, 'timestamp').text = datetime.now().isoformat()

    if os.path.exists(log_file):
        tree = ET.parse(log_file)
        root = tree.getroot()
        root.append(log_entry)
        tree.write(log_file)
    else:
        root = ET.Element('log')
        root.append(log_entry)
        tree = ET.ElementTree(root)
        tree.write(log_file)

# Чтение конфигурации
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

HOSTNAME = config['DEFAULT']['hostname']
VFS_PATH = config['DEFAULT']['vfs_path']
STARTUP_SCRIPT = config['DEFAULT']['startup_script']

# Монтирование виртуальной файловой системы
with tarfile.open(VFS_PATH, 'r') as tar:
    tar.extractall(path=DEFAULT_PATH)

# Основной цикл эмулятора
current_path = DEFAULT_PATH
start_time = time.time()
def execute_command(command):
    global current_path

    if command.startswith("ls"):
        words=current_path.split('/')
        for word in words:
            print(word)
        log_action(f"Executed: {command}")

    elif command.startswith("cd "):
        path = command.split(maxsplit=1)
        if "home" in str(path[1]):
            current_path=str(path[1])+'/'
        else:  
            current_path = current_path+'/'+str(path[1])
        log_action(f"Executed: {command}")

    elif command == "exit":
        log_action("Exit command executed.")
        print("Exiting...")
        return False

    elif command.startswith("echo "):
        print(command[5:])
        log_action(f"Executed: {command}")

    elif command == "uptime":
        current_time = time.time()
        elapsed_time = current_time - start_time
        print(f"Uptime: {elapsed_time:.2f} seconds")
        log_action("Executed: uptime")

    else:
        print(f"{command}: command not found")
        log_action(f"Unknown command: {command}")

    return True

# Выполнение стартового скрипта
if os.path.exists(STARTUP_SCRIPT):
    with open(STARTUP_SCRIPT, 'r') as f:
        for line in f:
            execute_command(line.strip())

# Основной ввод команд
while True:
    command = input(f"{HOSTNAME}:{current_path}$ ")
    if not execute_command(command):
        break

