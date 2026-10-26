from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from src.components.schedule_table import ScheduleTable
from src.components.wave_heading import WaveHeading

class PlayerSchedulePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Tournament Schedule")

        self.schedule_table = ScheduleTable()

        layout.addWidget(title)
        layout.addWidget(self.schedule_table)