from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class OrganizerScoreboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Update Scoreboard")
        title.setObjectName("page_title")

        description = QLabel(
            "Organizers will update match results here."
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()