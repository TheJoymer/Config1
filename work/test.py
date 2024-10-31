import unittest
import os
import tarfile
import xml.etree.ElementTree as ET
from unittest.mock import patch
from io import StringIO
from emulator import execute_command, log_action, CONFIG_PATH, DEFAULT_PATH, VFS_PATH

class TestEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создание тестового архива tar и конфигурационного файла для тестов
        os.makedirs(DEFAULT_PATH, exist_ok=True)

        
        with open(CONFIG_PATH, 'w') as config_file:
            config_file.write("[DEFAULT]\n")
            config_file.write("hostname = test_host\n")
            config_file.write("vfs_path = test_vfs.tar\n")
            config_file.write("startup_script = startup.sh\n")
        
        cls.log_file = os.path.join(DEFAULT_PATH, 'log.xml')
    def setUp(self):
        # Подготовка среды перед каждым тестом
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
    
    def test_ls_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            execute_command("ls")
            output = fake_out.getvalue().strip()
    
    def test_cd_command(self):
        current_path = os.getcwd()
        os.makedirs('test_dir', exist_ok=True)
        execute_command("cd test_dir")
        new_path = os.getcwd()
        self.assertEqual(new_path, os.path.join(current_path, 'test_dir'))
    
    def test_echo_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            execute_command("echo Hello World")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "Hello World")
    
    def test_uptime_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            execute_command("uptime")
            output = fake_out.getvalue().strip()
            self.assertTrue(output.startswith("Uptime: "))
    
    def test_exit_command(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = execute_command("exit")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "Exiting...")
            self.assertFalse(result)
    
    def test_log_action(self):
        action = "test_action"
        log_action(action)
        tree = ET.parse(self.log_file)
        root = tree.getroot()
        last_entry = root[-1]
        self.assertEqual(last_entry.find('action').text, action)
        self.assertIsNotNone(last_entry.find('timestamp').text)

    @classmethod
    def tearDownClass(cls):
        # Удаление тестовых файлов после завершения всех тестов
        if os.path.exists(CONFIG_PATH):
            os.remove(CONFIG_PATH)
        if os.path.exists('test_vfs.tar'):
            os.remove('test_vfs.tar')
        if os.path.exists(cls.log_file):
            os.remove(cls.log_file)
        if os.path.exists('test_dir'):
            os.rmdir('test_dir')

if __name__ == '__main__':
    unittest.main()
