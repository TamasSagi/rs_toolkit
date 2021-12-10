import os
import psutil
import sys

from collections import OrderedDict
from PyQt5.QtWidgets import QApplication

from scripts.clock import Clock
from scripts.timer import Timer

from gui.drawables import Text
from gui.script_selector import ScriptSelector
from gui.window import TransparenWindow


class Controller:

    FPS = 30.0

    def __init__(self) -> None:
        self.drawables = OrderedDict()  # Drawables are shared between the algo and GUI
        self.app = QApplication([])
        self.clock = Clock(Controller.FPS)
        self.timer = Timer()

        self.script_selector = ScriptSelector()
        self.script_selector.show()
        selected_script, duration = self.select_script()

        self.algo = selected_script(duration, self.drawables)

        screen_rect = self.app.desktop().screenGeometry()
        self.gui = TransparenWindow(screen_rect.width(), screen_rect.height(), self.drawables)

    def select_script(self) -> None:
        while self.script_selector.isVisible():
            self.app.processEvents()
            self.script_selector.update()

            self.clock.sleep()

        return self.script_selector.selected_script, self.script_selector.selected_duration

    def run(self) -> None:
        self.gui.show()

        while self.algo.is_running():
            try:
                self.update()

            except KeyboardInterrupt:
                sys.exit("Ctrl + C pressed by the user!")

        print("Script is ended gracefully!")

    @Timer.timeit
    def update(self) -> None:
        self.algo.update()

        self.app.processEvents()
        self.gui.update()

        self.update_status_message()

        self.clock.sleep()

    def update_status_message(self) -> None:
        duration = self.timer.get_formatted()
        fps = 1.0 / self.timer.get_last_update_time()
        algo_dur = self.algo.timer.get_avg_time()
        gui_dur = self.gui.timer.get_avg_time()

        mem_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2

        status_text = f"{duration} FPS: {fps:.2f}, Mem: {mem_usage:.2f}MB, algo: {algo_dur:.2f}ms gui: {gui_dur:.2f}ms"

        self.drawables["status"] = Text(100, 15, status_text, color=(0, 0, 0, 255))


if __name__ == "__main__":
    controller = Controller()
    controller.run()
