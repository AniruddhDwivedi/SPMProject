from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
)

from src.components.schedule_table import ScheduleTable
from src.services.schedule_service import ScheduleService


class OrganizerSchedulePage(QWidget):

    def __init__(self):
        super().__init__()

        self.schedule_service = ScheduleService()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Manage Schedule")
        title.setObjectName("page_title")

        layout.addWidget(title)

        self.schedule_table = ScheduleTable(
            editable=True
        )

        layout.addWidget(self.schedule_table)

        matches = self.schedule_service.get_matches()

        self.schedule_table.set_matches(matches)

        self.schedule_table.match_selected.connect(
            self.edit_match
        )

    def edit_match(self, match):
        QMessageBox.information(
            self,
            "Edit Match",
            f"Selected match:\n\n"
            f"{match['team_a']} vs {match['team_b']}\n"
            f"Sport: {match['sport']}\n"
            f"Date: {match['date']}\n"
            f"Venue: {match['venue']}"
        )