from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from src.services.schedule_service import ScheduleService


class ScheduleTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.schedule_service = ScheduleService()

        # Load matches from Supabase
        self.matches = self.schedule_service.get_matches()

        # Main layout
        self.layout = QVBoxLayout(self)

        # -------------------------
        # Filter
        # -------------------------

        filter_layout = QHBoxLayout()

        filter_label = QLabel("Filter by sport:")

        self.sport_filter = QComboBox()
        self.sport_filter.addItem("All Sports")

        # get_sports() returns strings
        self.sport_filter.addItems(
            self.schedule_service.get_sports()
        )

        self.sport_filter.currentTextChanged.connect(
            self.refresh_table
        )

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.sport_filter)
        filter_layout.addStretch()

        self.layout.addLayout(filter_layout)

        # -------------------------
        # Table
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "Sport",
                "Team A",
                "Team B",
                "Date",
                "Time",
                "Venue",
                "Status",
            ]
        )

        # Read-only table
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        # Stretch columns
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.layout.addWidget(self.table)

        # Populate table
        self.refresh_table()

    def refresh_table(self):
        selected_sport = self.sport_filter.currentText()

        # -------------------------
        # Filter matches
        # -------------------------

        if selected_sport == "All Sports":
            visible_matches = self.matches

        else:
            visible_matches = [
                match
                for match in self.matches
                if match.get("sport") == selected_sport
            ]

        # -------------------------
        # Populate table
        # -------------------------

        self.table.setRowCount(len(visible_matches))

        for row, match in enumerate(visible_matches):

            match_date = match.get("match_date", "")
            match_time = match.get("match_time", "")

            # Supabase may return time as HH:MM:SS.
            # We only display HH:MM.
            if isinstance(match_time, str) and len(match_time) >= 5:
                match_time = match_time[:5]

            values = [
                match.get("sport", ""),
                match.get("team_a", ""),
                match.get("team_b", ""),
                match_date,
                match_time,
                match.get("venue", ""),
                match.get("status", ""),
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                self.table.setItem(
                    row,
                    column,
                    item,
                )