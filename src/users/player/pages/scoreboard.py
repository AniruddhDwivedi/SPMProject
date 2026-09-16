from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class PlayerScoreboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("View Scoreboard")
        title.setObjectName("page_title")

        description = QLabel(
            "Tournament scoreboards will appear here."
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()