from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QFrame,
)


class LoginPage(QWidget):

    login_successful = pyqtSignal(dict)

    def __init__(self, auth_service):
        super().__init__()

        self.auth_service = auth_service

        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("login_page")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login card
        card = QFrame()
        card.setObjectName("login_card")
        card.setFixedWidth(400)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        title = QLabel("Inter IIT Tournament")
        title.setObjectName("title")

        subtitle = QLabel("Management System")
        subtitle.setObjectName("subtitle")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.role_input = QComboBox()
        self.role_input.addItems([
            "Player",
            "Organizer",
        ])

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.message = QLabel()
        self.message.setObjectName("message")
        self.message.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.role_input)
        card_layout.addWidget(self.login_button)
        card_layout.addWidget(self.message)

        layout.addWidget(card)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        user = self.auth_service.login(username, password)

        if user is None:
            self.message.setText("Invalid username or password.")
            return

        selected_role = self.role_input.currentText().lower()

        if user["role"] != selected_role:
            self.message.setText("Selected role does not match the account.")
            return

        self.message.setText("")

        self.login_successful.emit(user)