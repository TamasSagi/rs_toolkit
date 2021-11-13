from abc import ABC, abstractmethod

from PyQt5.QtGui import QPainter, QPen, QColor


class Drawable(ABC):
    def __init__(self, brush: QColor = QColor(255, 0, 0, 255), is_active: bool = True, **kwargs) -> None:
        self.pen = QPen(brush, **kwargs)
        self.is_active = is_active

    @abstractmethod
    def draw(self, painter: QPainter) -> None:
        painter.setPen(self.pen)  # TODO: check if this is the right way to set color


class Point(Drawable):
    def __init__(self, x: int, y: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.x = x
        self.y = y

    def draw(self, painter: QPainter) -> None:
        super().draw(painter)
        painter.drawPoint(self.x, self.y)


class Line(Drawable):
    def __init__(self, x: int, y: int, x2: int, y2: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2

    def draw(self, painter: QPainter) -> None:
        super().draw(painter)
        painter.drawLine(self.x, self.y, self.x2, self.y2)


class Rect(Drawable):
    def __init__(self, x: int, y: int, w: int, h: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, painter: QPainter) -> None:
        super().draw(painter)
        painter.drawRect(self.x, self.y, self.w, self.h)

    def get(self):
        return [self.x, self.y, self.w, self.h]

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}, {self.w}, {self.h}]"


class Text(Drawable):
    def __init__(self, x: int, y: int, text: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.text = text

    def draw(self, painter: QPainter) -> None:
        super().draw(painter)
        painter.drawText(self.x, self.y, self.text)
