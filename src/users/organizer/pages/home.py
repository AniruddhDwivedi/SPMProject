from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)
from src.components.wave_heading import WaveHeading

class OrganizerHomePage(QWidget):

    def __init__(self, user):
        super().__init__()

        layout = QVBoxLayout(self)

        title = WaveHeading("Organizer Dashboard")
        title.setObjectName("page_title")

        welcome = QLabel(
            f"Welcome, {user.username}!"
        )

        layout.addWidget(title)
        layout.addWidget(welcome)

        layout.addStretch()