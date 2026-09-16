from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class OrganizerHomePage(QWidget):

    def __init__(self, user):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("Organizer Dashboard")
        title.setObjectName("page_title")

        welcome = QLabel(
            f"Welcome, {user['name']}!"
        )

        layout.addWidget(title)
        layout.addWidget(welcome)

        layout.addStretch()