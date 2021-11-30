from dataclasses import dataclass
from pynput.keyboard import Listener


@dataclass
class KeyPressEvent:
    is_pressed: bool
    was_pressed: bool


class KeyPressListener:

    POSSIBLE_FIELDS = ["char", "name"]

    def __init__(self) -> None:
        self.keys = {}

        Listener(on_press=self.on_press, on_release=self.on_release).start()

    def on_press(self, key) -> None:
        for field in KeyPressListener.POSSIBLE_FIELDS:
            if hasattr(key, field) and getattr(key, field) not in self.keys.keys():
                self.keys[getattr(key, field)] = KeyPressEvent(True, True)
                break

    def on_release(self, key) -> None:
        for field in KeyPressListener.POSSIBLE_FIELDS:
            if hasattr(key, field):
                self.keys.pop(getattr(key, field))

    def is_key_pressed(self, key: str) -> bool:
        return self.keys.get(key, False)

    def was_key_pressed(self, key: str) -> bool:
        if key in self.keys.keys():
            if self.keys[key].was_pressed:
                self.keys[key].was_pressed = False
                return True

        return False
