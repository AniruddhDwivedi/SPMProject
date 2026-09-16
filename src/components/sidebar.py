from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
)


class Sidebar(QWidget):

    navigation_requested = pyqtSignal(str)

    def __init__(self, title, menu_items):
        super().__init__()

        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("sidebar_title")

        layout.addWidget(title_label)
        layout.addSpacing(20)

        self.buttons = {}

        for page_name, button_text in menu_items:
            button = QPushButton(button_text)

            button.setObjectName("sidebar_button")
            button.setCheckable(True)

            button.clicked.connect(
                lambda checked, name=page_name:
                    self.navigation_requested.emit(name)
            )

            self.buttons[page_name] = button

            layout.addWidget(button)

        layout.addStretch()

        logout_button = QPushButton("Logout")
        logout_button.setObjectName("logout_button")

        logout_button.clicked.connect(
            lambda: self.navigation_requested.emit("logout")
        )

        layout.addWidget(logout_button)

    def set_active(self, page_name):
        for name, button in self.buttons.items():
            button.setChecked(name == page_name)