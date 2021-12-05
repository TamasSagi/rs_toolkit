import numpy as np

from Xlib import X
from PIL import Image

from scripts.linux.window_handler import WindowHandler
from scripts.base_screenshot_taker import ScreenshotTaker


class ScreenshotTaker_Linux(ScreenshotTaker):
    def __init__(self) -> None:
        self.window_handler = WindowHandler()
        self.window = self.window_handler.get_window("runescape")

        root_geom = self.window_handler.root.get_geometry()
        display_width, display_height = root_geom.width, root_geom.height

        geom = self.window.get_geometry()
        self.w, self.h = geom.width, geom.height
        self.offset_y = display_height - geom.y - self.h - 2

    def take_screenshot(self, debug: bool = False) -> None:
        # TODO: It only works if window is Fullscreen
        raw_img = self.window.get_image(0, 0, self.w, self.h, X.ZPixmap, 0xFFFFFFFF)
        pil_img = Image.frombytes("RGB", (self.w, self.h), raw_img.data, "raw", "BGRX")

        self.frame = np.array(pil_img)

        if debug:
            pil_img.save("get_screenshot.png")
