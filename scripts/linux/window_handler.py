import sys

from Xlib import display, X
from Xlib.error import BadWindow
from Xlib.xobject.drawable import Window


class WindowHandler:
    def __init__(self) -> None:
        self.available_windows = []
        self.display = display.Display()
        self.root = self.display.screen().root

    def find_available_windows(self, window_name: str, window: Window = None) -> None:
        window = window if window else self.root

        try:
            children = window.query_tree().children
            for child_window in children:
                child_window_name = child_window.get_wm_name()

                if type(child_window_name) is str and window_name.lower() in child_window_name.lower():
                    self.available_windows.append(child_window)

                else:
                    self.find_available_windows(window_name, child_window)

        except BadWindow:
            print("Bad window found :(")

    def get_window(self, window_name: str) -> Window:
        self.find_available_windows(window_name)

        for window in self.available_windows:
            try:
                window.get_image(0, 0, 1, 1, X.ZPixmap, 0xFFFFFFFF)
                return window
            except Exception as e:
                print(f'Window "{window}" is bad!')

        sys.exit(f"Window '{window_name}' not found!")
