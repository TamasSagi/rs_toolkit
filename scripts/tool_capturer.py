import pyperclip
import sys

from pynput.mouse import Controller

from scripts.image_utils import get_img_region
from scripts.keypress_listener import KeyPressListener
from scripts.timer import Timer

from gui.drawables import Line, Rect, Text, Image

if sys.platform.startswith("win"):
    from scripts.windows.screenshot_taker import ScreenshotTaker_Windows as ScreenshotTaker
elif sys.platform.startswith("linux"):
    from scripts.linux.screenshot_taker import ScreenshotTaker_Linux as ScreenshotTaker
else:
    raise ImportError("rs_toolkit does not support your system! :(")


class ToolCapturer:
    def __init__(self, duration_s: int, drawables: dict) -> None:
        self.drawables = drawables
        self.duration_s = duration_s

        self.dragging = False
        self.freezed_img = None
        self.is_screen_freezed = False
        self.mouse = Controller()

        self.timer = Timer()
        self.listener = KeyPressListener()
        self.screenshot_taker = ScreenshotTaker()

        self.init_drawables()

    def init_drawables(self):
        self.drawables["freezed_screen"] = Image(0, 0, is_active=False)
        self.drawables["mouse_drag"] = Rect(0, 0, 0, 0, is_active=False)
        self.drawables["mouse_drag_text"] = Text(0, 0, "", is_active=False)

    def is_running(self):
        esc_was_pressed = self.listener.was_key_pressed("esc")
        finished = self.timer.get_elapsed_time() > self.duration_s

        if finished:
            print(f"Script has finished after {self.timer.get_elapsed_time():.2f}s!")

        if esc_was_pressed:
            print("ESC was pressed!")

        return not esc_was_pressed and not finished

    @Timer.timeit
    def update(self):
        self.update_highlight()

    def update_highlight(self):
        if self.listener.was_key_pressed("alt_l"):
            self.is_screen_freezed = True
            self.freezed_img = self.screenshot_taker.take_screenshot()
            self.drawables["freezed_screen"] = Image(0, 23, self.freezed_img)

        if not self.listener.is_key_pressed("alt_l"):
            if self.is_screen_freezed:
                self.is_screen_freezed = False
                self.drawables["freezed_screen"].is_active = False

        if self.listener.was_key_pressed("shift"):
            self.dragging = True
            start_x, start_y = self.mouse.position

            self.drawables["mouse_drag"].x = start_x
            self.drawables["mouse_drag"].y = start_y
            self.drawables["mouse_drag"].is_active = True
            self.drawables["mouse_drag_text"].is_active = True

        if self.listener.is_key_pressed("shift"):
            cur_x, cur_y = self.mouse.position

            w = cur_x - self.drawables["mouse_drag"].x
            h = cur_y - self.drawables["mouse_drag"].y

            self.drawables["mouse_drag"].w = w
            self.drawables["mouse_drag"].h = h

            mouse_drag_text_x = min(self.drawables["mouse_drag"].x, self.drawables["mouse_drag"].x + w)
            mouse_drag_text_y = min(self.drawables["mouse_drag"].y, self.drawables["mouse_drag"].y + h)
            mouse_drag_text = f"[{self.drawables['mouse_drag'].x}, {self.drawables['mouse_drag'].y}, {w}, {h}]"

            self.drawables["mouse_drag_text"].x = mouse_drag_text_x
            self.drawables["mouse_drag_text"].y = mouse_drag_text_y - 10
            self.drawables["mouse_drag_text"].text = mouse_drag_text

        else:
            if self.dragging:
                self.dragging = False
                pyperclip.copy(str(self.drawables["mouse_drag"]))

                captured_img = (
                    self.freezed_img
                    if self.listener.is_key_pressed("alt_l")
                    else self.screenshot_taker.take_screenshot()
                )

                image_obj = get_img_region(captured_img, self.drawables["mouse_drag"].get())

                h, w, _ = image_obj.img.shape
                self.drawables["alma"] = Image(100, 100, image_obj.img)
                self.drawables["fing"] = Rect(100, 100, w, h)

            self.drawables["mouse_drag"].is_active = False
            self.drawables["mouse_drag_text"].is_active = False
