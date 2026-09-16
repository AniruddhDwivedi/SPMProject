from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)

from src.components.schedule_table import ScheduleTable
from src.services.schedule_service import ScheduleService


class PlayerSchedulePage(QWidget):

    def __init__(self):
        super().__init__()

        self.schedule_service = ScheduleService()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("View Schedule")
        title.setObjectName("page_title")

        layout.addWidget(title)

        self.schedule_table = ScheduleTable(
            editable=False
        )

        layout.addWidget(self.schedule_table)

        matches = self.schedule_service.get_matches()

        self.schedule_table.set_matches(matches)