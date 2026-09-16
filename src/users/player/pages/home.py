from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFrame,
)


class PlayerHomePage(QWidget):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Dashboard")
        title.setObjectName("page_title")

        welcome = QLabel(
            f"Welcome, {self.user['name']}!"
        )

        layout.addWidget(title)
        layout.addWidget(welcome)

        cards = QHBoxLayout()

        cards.addWidget(
            self.create_card("Upcoming Matches", "3")
        )

        cards.addWidget(
            self.create_card("Matches Played", "5")
        )

        cards.addWidget(
            self.create_card("Kit Requests", "1")
        )

        layout.addLayout(cards)
        layout.addStretch()

    def create_card(self, title, value):
        card = QFrame()
        card.setObjectName("dashboard_card")

        card_layout = QVBoxLayout(card)

        title_label = QLabel(title)
        value_label = QLabel(value)

        value_label.setObjectName("card_value")

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)

        return card