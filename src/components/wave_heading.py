import math

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QLabel

class WaveHeading(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.phase = 0.0
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )

        self.animation = QTimer(self)
        self.animation.timeout.connect(self.animate)
        self.animation.start(45)

    def animate(self):
        self.phase += 0.10
        if self.phase > 2 * math.pi:
            self.phase -= 2 * math.pi
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.TextAntialiasing, True
        )
        painter.setFont(self.font())

        text = self.text()
        if not text:
            painter.end()
            return

        metrics = painter.fontMetrics()
        text_width = metrics.horizontalAdvance(text)

        alignment = self.alignment()

        if alignment & Qt.AlignmentFlag.AlignHCenter:
            x = (self.width() - text_width) / 2
        elif alignment & Qt.AlignmentFlag.AlignRight:
            x = self.width() - text_width
        else:
            x = 0

        baseline = (
            (self.height() - metrics.height()) / 2
            + metrics.ascent()
        )

        dark_green = QColor("#176b4d")
        light_green = QColor("#43b581")

        for index, character in enumerate(text):
            wave = (
                math.sin(index * 0.45 + self.phase) + 1
            ) / 2

            color = QColor(
                round(
                    dark_green.red()
                    + (light_green.red() - dark_green.red()) * wave
                ),
                round(
                    dark_green.green()
                    + (light_green.green() - dark_green.green()) * wave
                ),
                round(
                    dark_green.blue()
                    + (light_green.blue() - dark_green.blue()) * wave
                ),
            )

            painter.setPen(color)
            painter.drawText(
                round(x), round(baseline), character
            )
            x += metrics.horizontalAdvance(character)

        painter.end()
