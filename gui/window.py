from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent
from PyQt5.QtWidgets import QWidget, QMainWindow


class TransparenWindow(QMainWindow):
    def __init__(self, screen_width: int, screen_height: int, drawables: dict) -> None:
        super().__init__()
        self.drawables = drawables
        self.resize(screen_width, screen_height)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Set attributes and flags to make window:
        # transparent, always on top, frameless, click through
        flags = Qt.Window | Qt.X11BypassWindowManagerHint | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(flags)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.central_widget.painter = QPainter()
        self.central_widget.painter.begin(self)

        for drawable_name, drawable in self.drawables.items():
            if drawable.is_active:
                drawable.draw(self.central_widget.painter)

        self.central_widget.painter.end()
