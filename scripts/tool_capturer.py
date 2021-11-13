from pynput import mouse
import pyperclip

from pynput.mouse import Controller

from scripts.image_handler import ImageHandler
from scripts.keypress_listener import KeyPressListener
from scripts.timer import Timer

from gui.drawables import Line, Rect, Text, Image


class ToolCapturer:
    def __init__(self, duration_s: int, drawables: dict) -> None:
        self.drawables = drawables
        self.duration_s = duration_s

        self.dragging = False
        self.mouse = Controller()

        self.timer = Timer()
        self.listener = KeyPressListener()
        self.img_handler = ImageHandler()

        self.init_drawables()

    def init_drawables(self):
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

                self.img_handler.get_screenshot()
                region = self.img_handler.get_img_region(self.drawables["mouse_drag"].get())

                h, w, _ = region.shape
                self.drawables["alma"] = Image(100, 100, region)
                self.drawables["fing"] = Rect(100, 100, w, h)

            self.drawables["mouse_drag"].is_active = False
            self.drawables["mouse_drag_text"].is_active = False
