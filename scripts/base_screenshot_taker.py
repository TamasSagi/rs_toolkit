from abc import ABC, abstractmethod


class ScreenshotTaker(ABC):
    def __init__(self) -> None:
        self.frame = None

    @abstractmethod
    def take_screenshot(self, debug: bool = False, window_name: str = "RuneScape") -> None:
        pass
