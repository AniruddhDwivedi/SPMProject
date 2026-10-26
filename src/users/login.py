from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QFrame,
)
from src.components.wave_heading import WaveHeading

class LoginPage(QWidget):
    login_successful = pyqtSignal(object)

    def __init__(self, auth_service):
        super().__init__()

        self.auth_service = auth_service
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("login_page")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("login_card")
        card.setFixedWidth(600)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        title = WaveHeading("Inter VIT Tournament")
        title.setObjectName("title")

        subtitle = QLabel("Management System")
        subtitle.setObjectName("subtitle")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.message = QLabel()
        self.message.setObjectName("message")
        self.message.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.message.setWordWrap(True)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_button)
        card_layout.addWidget(self.message)

        layout.addWidget(card)

    def login(self):
        email = self.username_input.text().strip()
        password = self.password_input.text()

        if not email or not password:
            self.message.setText(
                "Please enter your email and password."
            )
            return

        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")

        try:
            user = self.auth_service.login(email, password)

            if user is None:
                self.message.setText(
                    "Login failed. Check your credentials "
                    "and user profile."
                )
                return

            self.message.clear()
            self.login_successful.emit(user)

        except Exception as error:
            print("LOGIN PAGE ERROR:", repr(error))
            self.message.setText(
                "An error occurred while logging in."
            )

        finally:
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
