import numpy as np

from abc import ABC, abstractmethod
from PIL import Image


class ScreenshotTaker(ABC):
    def __init__(self) -> None:
        self.frame = None

    @abstractmethod
    def take_screenshot(self, debug: bool = False, window_name: str = "RuneScape") -> None:
        pass

    def get_img_region(self, rect: list, debug: bool = False) -> np.array:
        # Calculate x, y coordinates and index from top left corner
        # +1 is to exclude the border drawn by the mouse.
        x = sorted([rect[0] + 1, rect[0] + rect[2]])
        y = sorted([rect[1] - self.offset_y + 1, rect[1] - self.offset_y + rect[3]])

        region = self.frame[y[0] : y[1], x[0] : x[1]]

        if debug:
            Image.fromarray(region).save("get_img_region_result.png")

        return region
