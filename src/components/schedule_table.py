from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHeaderView,
)


class ScheduleTable(QWidget):

    match_selected = pyqtSignal(dict)

    def __init__(self, editable=False):
        super().__init__()

        self.editable = editable
        self.matches = []

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Filters
        filters = QHBoxLayout()

        filters.addWidget(QLabel("Sport:"))

        self.sport_filter = QComboBox()
        self.sport_filter.addItem("All Sports")

        self.sport_filter.currentTextChanged.connect(
            self.filter_matches
        )

        filters.addWidget(self.sport_filter)
        filters.addStretch()

        layout.addLayout(filters)

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Sport",
            "Team A",
            "Team B",
            "Date",
            "Venue",
            "Status",
        ])

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        # Organizer actions
        if self.editable:
            actions = QHBoxLayout()

            self.add_button = QPushButton("Add Match")
            self.edit_button = QPushButton("Edit Match")
            self.delete_button = QPushButton("Delete Match")

            actions.addWidget(self.add_button)
            actions.addWidget(self.edit_button)
            actions.addWidget(self.delete_button)

            layout.addLayout(actions)

            self.edit_button.clicked.connect(
                self.edit_selected_match
            )

            self.delete_button.clicked.connect(
                self.delete_selected_match
            )

    def set_matches(self, matches):
        self.matches = matches

        sports = sorted({
            match["sport"]
            for match in matches
        })

        self.sport_filter.blockSignals(True)

        self.sport_filter.clear()
        self.sport_filter.addItem("All Sports")
        self.sport_filter.addItems(sports)

        self.sport_filter.blockSignals(False)

        self.filter_matches()

    def filter_matches(self):
        selected_sport = self.sport_filter.currentText()

        if selected_sport == "All Sports":
            filtered = self.matches

        else:
            filtered = [
                match
                for match in self.matches
                if match["sport"] == selected_sport
            ]

        self.populate_table(filtered)

    def populate_table(self, matches):
        self.table.setRowCount(0)

        for match in matches:
            row = self.table.rowCount()
            self.table.insertRow(row)

            values = [
                match["sport"],
                match["team_a"],
                match["team_b"],
                match["date"],
                match["venue"],
                match["status"],
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(row, column, item)

    def get_selected_match(self):
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            return None

        row = selected_rows[0].row()

        sport = self.table.item(row, 0).text()
        team_a = self.table.item(row, 1).text()
        team_b = self.table.item(row, 2).text()

        for match in self.matches:
            if (
                match["sport"] == sport
                and match["team_a"] == team_a
                and match["team_b"] == team_b
            ):
                return match

        return None

    def edit_selected_match(self):
        match = self.get_selected_match()

        if match:
            self.match_selected.emit(match)

    def delete_selected_match(self):
        match = self.get_selected_match()

        if match:
            self.matches.remove(match)
            self.filter_matches()