from pynput.keyboard import Listener


class KeyPressListener:
    def __init__(self) -> None:
        self.keys = {}

        Listener(on_press=self.on_press, on_release=self.on_release).start()

    def on_press(self, key: str) -> None:
        if hasattr(key, "char"):
            self.keys[key.char] = {"is_pressed": True, "was_pressed": True}

        elif hasattr(key, "name"):
            self.keys[key.name] = {"is_pressed": True, "was_pressed": True}

    def on_release(self, key: str) -> None:
        if hasattr(key, "char"):
            self.keys[key.char]["is_pressed"] = False

        elif hasattr(key, "name"):
            self.keys[key.name]["is_pressed"] = False

    def is_key_pressed(self, key: str) -> bool:
        if key in self.keys.keys():
            return self.keys[key]["is_pressed"]

        return False

    def was_key_pressed(self, key: str) -> bool:
        if key in self.keys.keys():
            if self.keys[key]["was_pressed"]:
                self.keys[key]["was_pressed"] = False
                return True

        return False
