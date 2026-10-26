from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from src.services.auth_service import AuthService
from src.services.supabase_client import supabase
from src.users.login import LoginPage
from src.users.player.dashboard import PlayerDashboard
from src.users.organizer.dashboard import OrganizerDashboard
from src.users.team_manager.dashboard import TeamManagerDashboard

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Inter VIT Tournament Management System"
        )

        self.resize(1200, 750)

        self.auth_service = AuthService()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_page = LoginPage(
            self.auth_service
        )

        self.stack.addWidget(self.login_page)

        self.login_page.login_successful.connect(
            self.handle_login
        )

        self.dashboard_page = None
        self.current_user = None

        self.stack.setCurrentWidget(
            self.login_page
        )


    def handle_login(self, user):
        self.current_user = user

        if user.role == "player":
            self.show_player_dashboard()

        elif user.role == "organizer":
            self.show_organizer_dashboard()

        elif user.role == "team_manager":
            self.show_team_manager_dashboard()

    def show_player_dashboard(self):
        self.remove_dashboard()
        self.dashboard_page = PlayerDashboard(
            self.current_user, self
        )
        self.stack.addWidget(self.dashboard_page)
        self.stack.setCurrentWidget(self.dashboard_page)

    def show_team_manager_dashboard(self):
        self.remove_dashboard()

        self.dashboard_page = TeamManagerDashboard(
            self.current_user,
            self,
        )

        self.stack.addWidget(self.dashboard_page)
        self.stack.setCurrentWidget(self.dashboard_page)

    def show_organizer_dashboard(self):
        self.remove_dashboard()
        self.dashboard_page = OrganizerDashboard(
            self.current_user, self
        )
        self.stack.addWidget(self.dashboard_page)
        self.stack.setCurrentWidget(self.dashboard_page)
        
    def remove_dashboard(self):
        if self.dashboard_page is not None:
            self.stack.removeWidget(
                self.dashboard_page
            )

            self.dashboard_page.deleteLater()

            self.dashboard_page = None

    def logout(self):
        self.remove_dashboard()

        self.current_user = None

        try:
            supabase.auth.sign_out()
        except Exception:
            pass

        self.login_page.username_input.clear()
        self.login_page.password_input.clear()
        self.login_page.message.clear()

        self.stack.setCurrentWidget(
            self.login_page
        )