from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.services.auth_service import AuthService
from src.users.login import LoginPage
from src.users.player.dashboard import PlayerDashboard
from src.users.organizer.dashboard import OrganizerDashboard


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Inter IIT Tournament Management System"
        )

        self.resize(1200, 750)

        self.auth_service = AuthService()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(self.auth_service)

        self.stack.addWidget(self.login_page)

        self.login_page.login_successful.connect(
            self.handle_login
        )

        self.dashboard_page = None

        self.stack.setCurrentWidget(self.login_page)

    def handle_login(self, user):
        self.current_user = user

        if self.dashboard_page is not None:
            self.stack.removeWidget(self.dashboard_page)
            self.dashboard_page.deleteLater()
            self.dashboard_page = None

        if user["role"] == "player":
            self.dashboard_page = PlayerDashboard(
                user,
                self
            )

        elif user["role"] == "organizer":
            self.dashboard_page = OrganizerDashboard(
                user,
                self
            )

        self.stack.addWidget(self.dashboard_page)
        self.stack.setCurrentWidget(self.dashboard_page)

    def logout(self):
        if self.dashboard_page is not None:
            self.stack.removeWidget(self.dashboard_page)
            self.dashboard_page.deleteLater()
            self.dashboard_page = None

        self.current_user = None

        self.stack.setCurrentWidget(self.login_page)

        self.login_page.username_input.clear()
        self.login_page.password_input.clear()