import winreg
import configparser
import os.path
import ctypes


def get_registry_subkeys_list(registry_key):
    subkeys = []
    reg_dir = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, registry_key, 0, winreg.KEY_READ)
    try:
        i = 0
        while True:
            subkey = winreg.EnumKey(reg_dir, i)
            subkeys.append(subkey)
            i += 1
    except WindowsError:
        return subkeys

def set_reg(name, value, reg_path):
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except PermissionError:
        ctypes.windll.user32.MessageBoxW(0, message_error_permission, title_error, 0)
        exit()
    except WindowsError:
        return False

def get_reg(name, reg_path):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


ini_filename = 'port_config.ini'

title_error = "Ошибка"
title_success = "Успех!"
message_error_permission = "Недостаточно прав для работы. Откройте программу в режиме администратора!."
message_error_config_not_found = f"Упс! Похоже вы потеряли файл {ini_filename} , ничего страшного, мы создадим вам новый.\n" \
                         f"Заполните его и перезапустите скрипт."
message_success = "Переподключите устройства или перезагрузите компьютер, чтобы изменения вступили в силу."


config = configparser.ConfigParser()

if os.path.isfile(ini_filename):
    config.read(ini_filename)
else:
    ctypes.windll.user32.MessageBoxW(0, message_error_config_not_found, title_error, 0)
    config['Device 1'] = {'Device-id': 'VID_10C4&PID_EA60',
                          'Port': 'COM9'
                          }
    config['Device ??'] = {'Device-id': 'VID_????&PID_????',
                           'Port': 'COM?'
                          }
    with open('port_config.ini', 'w') as configfile:
        config.write(configfile)
    exit()

for device in config:
    try:
        device_id = config[device]['device-id']
        device_port = config[device]['port']
    except:
        continue

    device_registry_key = 'SYSTEM\\CurrentControlSet\\Enum\\USB\\' + device_id + '\\'
    cur_devices = get_registry_subkeys_list(device_registry_key)

    if len(cur_devices) > 0:
        for phys_device in cur_devices:

            device_key = device_registry_key + phys_device + '\\'
            device_parameters_key = device_key + 'Device Parameters\\'
            # Change port
            set_reg('PortName', device_port, device_parameters_key)
            # Change port in device name
            dev_name = get_reg('FriendlyName', device_key)
            correct_dev_name = dev_name.replace(dev_name[dev_name.find('(COM'):], f'({device_port})')
            set_reg('FriendlyName', correct_dev_name, device_key)


ctypes.windll.user32.MessageBoxW(0, message_success, title_success, 0)