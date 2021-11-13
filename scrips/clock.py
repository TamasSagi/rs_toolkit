import time


class Clock:
    def __init__(self, fps: float) -> None:
        self.start = time.perf_counter()
        self.frame_length = 1.0 / fps

    @property
    def tick(self) -> int:
        return int((time.perf_counter() - self.start) / self.frame_length)

    def sleep(self) -> None:
        r = self.tick + 1
        while self.tick < r:
            time.sleep(0.001)
