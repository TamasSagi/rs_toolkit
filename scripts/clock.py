import time


class Clock:
    def __init__(self, fps: float) -> None:
        self.start_time = time.perf_counter()
        self.frame_duration = 1.0 / fps

    @property
    def tick(self) -> int:
        return int((time.perf_counter() - self.start_time) / self.frame_duration)

    def sleep(self) -> None:
        next_frame_start_time = self.tick + 1
        while self.tick < next_frame_start_time:
            time.sleep(0.001)
