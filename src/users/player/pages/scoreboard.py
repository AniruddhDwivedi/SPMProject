from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from src.components.wave_heading import WaveHeading
from src.services.scoreboard_service import ScoreboardService

class PlayerScoreboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.scoreboard_service = ScoreboardService()
        self.matches = []

        self.setup_ui()
        self.load_results()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("View Scoreboard")
        title.setObjectName("page_title")

        description = QLabel(
            "View match scores and completed results."
        )

        filter_layout = QHBoxLayout()

        self.sport_filter = QComboBox()
        self.sport_filter.addItem("All Sports")
        self.sport_filter.currentTextChanged.connect(
            self.refresh_table
        )

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_results)

        filter_layout.addWidget(QLabel("Sport:"))
        filter_layout.addWidget(self.sport_filter)
        filter_layout.addWidget(self.refresh_button)
        filter_layout.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Sport",
            "Team A",
            "Score",
            "Team B",
            "Score",
            "Date",
            "Venue",
            "Status",
        ])

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.message)

    def load_results(self):
        try:
            self.matches = self.scoreboard_service.get_matches()

            current_sport = self.sport_filter.currentText()

            sports = sorted({
                match.get("sport")
                for match in self.matches
                if match.get("sport")
            })

            self.sport_filter.blockSignals(True)
            self.sport_filter.clear()
            self.sport_filter.addItem("All Sports")
            self.sport_filter.addItems(sports)

            if current_sport in sports:
                self.sport_filter.setCurrentText(current_sport)

            self.sport_filter.blockSignals(False)

            self.message.setText(
                f"Loaded {len(self.matches)} matches."
            )

            self.refresh_table()

        except Exception as error:
            self.sport_filter.blockSignals(False)
            print("PLAYER SCOREBOARD ERROR:", repr(error))
            self.message.setText(
                "Could not load results. Check your connection "
                "and Supabase permissions."
            )

    def refresh_table(self, *_):
        selected_sport = self.sport_filter.currentText()

        visible_matches = [
            match for match in self.matches
            if (
                selected_sport == "All Sports"
                or match.get("sport") == selected_sport
            )
        ]

        self.table.setRowCount(len(visible_matches))

        for row, match in enumerate(visible_matches):
            score_a = match.get("team_a_score")
            score_b = match.get("team_b_score")

            values = [
                match.get("sport", ""),
                match.get("team_a", ""),
                "—" if score_a is None else str(score_a),
                match.get("team_b", ""),
                "—" if score_b is None else str(score_b),
                match.get("match_date", ""),
                match.get("venue", ""),
                match.get("status", ""),
            ]

            for column, value in enumerate(values):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )
