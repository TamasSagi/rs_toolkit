from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QPushButton

from scripts.available_algos import AVAILABLE_ALGOS


class ScriptSelector(QWidget):
    def __init__(self, durations: list = [0.5, 1, 2, 3, 4, 5, 6]) -> None:
        super().__init__()

        layout = QVBoxLayout()
        self.script_cb = QComboBox()
        self.script_cb.addItems(AVAILABLE_ALGOS.keys())

        self.duration_cb = QComboBox()
        self.duration_cb.addItems(map(lambda i: str(i) + "h", durations))

        self.start_button = QPushButton("Start")
        self.start_button.pressed.connect(self.start)

        layout.addWidget(self.script_cb)
        layout.addWidget(self.duration_cb)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.resize(320, 90)
        self.setWindowTitle("Please Select Script")

    def start(self) -> None:
        self.selected_duration = float(self.duration_cb.currentText()[:-1]) * 3600  # Hour -> second
        self.selected_script = AVAILABLE_ALGOS[self.script_cb.currentText()]

        self.close()
