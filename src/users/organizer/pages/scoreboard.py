from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QPushButton,
    QLineEdit,
)
from src.components.wave_heading import WaveHeading
from src.services.scoreboard_service import ScoreboardService

class OrganizerScoreboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.scoreboard_service = ScoreboardService()
        self.matches = []

        self.setup_ui()
        self.load_matches()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Update Scoreboard")
        title.setObjectName("page_title")

        description = QLabel(
            "Select a match, enter its final scores, and save."
        )

        self.match_combo = QComboBox()
        self.match_combo.currentIndexChanged.connect(
            self.load_selected_match
        )

        self.match_info = QLabel("Select a match.")

        score_layout = QHBoxLayout()

        self.team_a_label = QLabel("Team A")
        self.team_a_score = QSpinBox()
        self.team_a_score.setRange(0, 100000)

        self.team_b_label = QLabel("Team B")
        self.team_b_score = QSpinBox()
        self.team_b_score.setRange(0, 100000)

        score_layout.addWidget(self.team_a_label)
        score_layout.addWidget(self.team_a_score)
        score_layout.addWidget(self.team_b_label)
        score_layout.addWidget(self.team_b_score)

        self.details_input = QLineEdit()
        self.details_input.setPlaceholderText(
            "Optional result details"
        )

        self.save_button = QPushButton("Save Result")
        self.save_button.clicked.connect(self.save_result)

        self.refresh_button = QPushButton("Refresh Matches")
        self.refresh_button.clicked.connect(self.load_matches)

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(QLabel("Select match:"))
        layout.addWidget(self.match_combo)
        layout.addWidget(self.match_info)
        layout.addLayout(score_layout)
        layout.addWidget(self.details_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.message)
        layout.addStretch()

    def load_matches(self):
        self.save_button.setEnabled(False)
        self.match_combo.blockSignals(True)

        try:
            self.matches = self.scoreboard_service.get_matches()

            self.match_combo.clear()

            for match in self.matches:
                label = (
                    f'{match.get("sport", "Unknown sport")} | '
                    f'{match.get("team_a", "Team A")} vs '
                    f'{match.get("team_b", "Team B")} | '
                    f'{match.get("match_date", "")}'
                )

                self.match_combo.addItem(label, match.get("id"))

            self.message.setText(
                f"Loaded {len(self.matches)} matches."
            )

        except Exception as error:
            print("SCOREBOARD LOAD ERROR:", repr(error))
            self.message.setText(
                "Could not load matches. Check your connection "
                "and Supabase permissions."
            )

        finally:
            self.match_combo.blockSignals(False)

        self.load_selected_match()

    def load_selected_match(self, *_):
        match_id = self.match_combo.currentData()

        match = next(
            (
                item for item in self.matches
                if item.get("id") == match_id
            ),
            None,
        )

        if match is None:
            self.match_info.setText("No match selected.")
            self.save_button.setEnabled(False)
            return

        team_a = match.get("team_a", "Team A")
        team_b = match.get("team_b", "Team B")

        self.team_a_label.setText(team_a)
        self.team_b_label.setText(team_b)

        self.team_a_score.setValue(
            match.get("team_a_score")
            if match.get("team_a_score") is not None
            else 0
        )
        self.team_b_score.setValue(
            match.get("team_b_score")
            if match.get("team_b_score") is not None
            else 0
        )

        self.details_input.setText(
            match.get("result_details") or ""
        )

        self.match_info.setText(
            f'Status: {match.get("status", "Scheduled")}'
        )

        self.save_button.setEnabled(True)

    def save_result(self):
        match_id = self.match_combo.currentData()

        if match_id is None:
            self.message.setText("Please select a match.")
            return

        self.save_button.setEnabled(False)

        try:
            self.scoreboard_service.save_result(
                match_id=match_id,
                team_a_score=self.team_a_score.value(),
                team_b_score=self.team_b_score.value(),
                result_details=self.details_input.text(),
            )

            self.message.setText(
                "Result saved successfully."
            )

            self.load_matches()

        except Exception as error:
            print("SCOREBOARD SAVE ERROR:", repr(error))
            self.message.setText(
                "Could not save the result. Check that you are "
                "logged in as an organizer and have permission "
                "to update matches."
            )

        finally:
            self.save_button.setEnabled(
                self.match_combo.currentData() is not None
            )
