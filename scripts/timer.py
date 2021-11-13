import sys
import time

from collections import deque


class Timer:
    def __init__(self, queue_size=30) -> None:
        self.start_time = time.time()
        self.measure_start = 0.0
        self.update_times = deque([0.33], maxlen=queue_size)

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
        return time.time() - self.start_time

    def get_avg_time(self) -> float:
        return (sum(self.update_times) / len(self.update_times)) * 1000.0  # [ms]

    def start(self):
        self.measure_start = time.time()

    def end(self):
        self.update_times.append(time.time() - self.measure_start)
