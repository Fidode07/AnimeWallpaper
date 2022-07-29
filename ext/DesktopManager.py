import win32gui
import win32con


class Handle:

    def __init__(self) -> None:
        self.worker: int = 0
        self.all_workers: list = []

    def __enum_handler(self, hwnd, ctx):
        icon_window = win32gui.FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
        if icon_window != 0:
            self.worker = win32gui.FindWindowEx(None, hwnd, "WorkerW", None)

    def send_behind(self, target):
        prog_man = win32gui.FindWindow("Progman", "Program Manager")

        win32gui.SendMessageTimeout(prog_man, 0x52C,
                                    0, 0, win32con.SMTO_NORMAL, 1000)

        win32gui.SetParent(target, prog_man)

        self.all_workers = [0]
        win32gui.EnumWindows(self.__callb, None)

        win32gui.ShowWindow(self.all_workers[0], win32con.SW_HIDE)

        win32gui.SetParent(target, prog_man)

        win32gui.ShowWindow(self.worker, win32con.SW_SHOW)

    def __callb(self, hwnd, ctx):
        tmp_tg = win32gui.FindWindowEx(hwnd, None, "SHELLDLL_DefView", None)
        if tmp_tg != 0 and tmp_tg is not None:
            self.all_workers[0] = win32gui.FindWindowEx(None, hwnd, "WorkerW", None)

    def repair(self):
        prog = win32gui.FindWindow("Progman", None)
        win32gui.EnumWindows(self.__enum_handler, None)

        if self.worker is not None:
            win32gui.ShowWindow(prog, win32con.SW_HIDE)
            win32gui.ShowWindow(self.worker, win32con.SW_HIDE)

            win32gui.ShowWindow(prog, win32con.SW_SHOW)
            win32gui.ShowWindow(self.worker, win32con.SW_SHOW)
