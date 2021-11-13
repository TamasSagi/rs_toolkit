import numpy as np

from Xlib import X
from PIL import Image

from scripts.window_handler import WindowHandler


class ImageHandler:
    def __init__(self) -> None:
        self.window_handler = WindowHandler()
        self.window = self.window_handler.get_window("runescape")

        root_geom = self.window_handler.root.get_geometry()
        display_width, display_height = root_geom.width, root_geom.height

        geom = self.window.get_geometry()
        self.w, self.h = geom.width, geom.height
        self.offset_y = display_height - geom.y - self.h - 2

        self.latest_image = None

    def get_screenshot(self, debug: bool = False) -> None:
        # TODO: It only works if window is Fullscreen
        raw_img = self.window.get_image(0, 0, self.w, self.h, X.ZPixmap, 0xFFFFFFFF)
        pil_img = Image.frombytes("RGB", (self.w, self.h), raw_img.data, "raw", "BGRX")

        self.latest_image = np.array(pil_img)

        if debug:
            pil_img.save("get_screenshot.png")

    def get_img_region(self, rect: list, debug: bool = False) -> np.array:
        # Calculate x, y coordinates and index from top left corner
        # +1 is to exclude the border drawn by the mouse.
        x = sorted([rect[0] + 1, rect[0] + rect[2]])
        y = sorted([rect[1] - self.offset_y + 1, rect[1] - self.offset_y + rect[3]])

        region = self.latest_image[y[0] : y[1], x[0] : x[1]]

        if debug:
            Image.fromarray(region).save("get_img_region_result.png")

        return region
