import os
import tarfile
import xml.etree.ElementTree as ET
import configparser
import subprocess
import time
from datetime import datetime

CONFIG_PATH = 'config.ini'
DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()


config.read('config.ini')


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


config = configparser.ConfigParser()
config.read(CONFIG_PATH)

HOSTNAME = config['DEFAULT']['hostname']
VFS_PATH = config['DEFAULT']['vfs_path']
STARTUP_SCRIPT = config['DEFAULT']['startup_script']


extracted_files = []
with tarfile.open(VFS_PATH, 'r') as tar:
    extracted_files = tar.getnames() 
current_path = os.getcwd()  
start_time = time.time()

def execute_command(command):
    global current_path

    if command.startswith("ls"):

        if command=="ls":
            try:
                items = os.listdir(current_path)
                for item in items:
                    print(item)
            except FileNotFoundError:
                print(f"ls: cannot access '{current_path}': No such directory")
            log_action(f"Executed: {command}")
        else:
            path = command.split(maxsplit=1)[1]
            try:
                new_path=os.path.join(current_path, path) if not os.path.isabs(path) else path
                items = os.listdir(new_path)
                for item in items:
                    print(item)
            except FileNotFoundError:
                print(f"ls: cannot access '{new_path}': No such directory")
            log_action(f"Executed: {command}")
    elif command.startswith("cd "):
        # Обработка команды cd
        path = command.split(maxsplit=1)[1]
        new_path = os.path.join(current_path, path) if not os.path.isabs(path) else path
        if os.path.isdir(new_path):
            current_path = new_path
            os.chdir(current_path) 
        else:
            print(f"cd: no such file or directory: {path}")
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

if os.path.exists(STARTUP_SCRIPT):
    with open(STARTUP_SCRIPT, 'r') as f:
        for line in f:
            execute_command(line.strip())

while True:
    command = input(f"{HOSTNAME}:{current_path}$ ")
    if not execute_command(command):
        break