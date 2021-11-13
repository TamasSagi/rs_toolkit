import sys
import time

from collections import deque


class Timer:

    S_TO_MS = 1000
    GUESSED_UPDATE_TIME = 0.033  # 30FPS

    def __init__(self, queue_size=30) -> None:
        self.start_time = time.perf_counter()
        self.measure_start = 0.0
        self.update_times = deque(maxlen=queue_size)

    # TODO: type hint
    @staticmethod
    def timeit(func):
        def wrapper(*args, **kwargs):
            if not hasattr(args[0], "timer") or not type(args[0].timer) == Timer:
                sys.exit("Do not use '@timeit' decorator on objects which does not implement Timer.")

            args[0].timer.start()
            ret = func(*args, **kwargs)
            args[0].timer.end()

            return ret

        return wrapper

    def get_formatted(self) -> str:
        # Returns time in [hh:mm:ss] format
        return time.strftime("%H:%M:%S", time.gmtime(int(self.get_elapsed_time())))

    def get_elapsed_time(self) -> float:
        return time.perf_counter() - self.start_time

    def get_avg_time(self) -> float:
        return (sum(self.update_times) / len(self.update_times)) * Timer.S_TO_MS

    def get_last_update_time(self) -> float:
        return self.update_times[-1] if len(self.update_times) > 0 else Timer.GUESSED_UPDATE_TIME

    def start(self) -> None:
        self.measure_start = time.perf_counter()

    def end(self) -> None:
        self.update_times.append(time.perf_counter() - self.measure_start)
