from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from src.components.sidebar import Sidebar
from src.users.organizer.pages.player_reporting import PlayerReportingPage
from src.users.organizer.pages.home import OrganizerHomePage
from src.users.organizer.pages.schedule import OrganizerSchedulePage
from src.users.organizer.pages.scoreboard import OrganizerScoreboardPage
from src.users.organizer.pages.complaints import OrganizerComplaintsPage
from src.users.organizer.pages.kits import OrganizerKitsPage

class OrganizerDashboard(QWidget):

    def __init__(self, user, main_window):
        super().__init__()

        self.user = user
        self.main_window = main_window

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar(
            "VITMS Organizer",
            [
                ("home", "Dashboard"),
                ("schedule", "Manage Schedule"),
                ("scoreboard", "Update Scoreboard"),
                ("player_reporting", "Player Reporting"),
                ("complaints", "Complaints"),
                ("player_kits", "Player Kits")
            ],
        )

        self.stack = QStackedWidget()

        self.pages = {
            "home": OrganizerHomePage(self.user),
            "schedule": OrganizerSchedulePage(),
            "scoreboard": OrganizerScoreboardPage(),
            "player_reporting": PlayerReportingPage(),
            "complaints": OrganizerComplaintsPage(),
            "player_kits": OrganizerKitsPage(),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack)

        self.sidebar.navigation_requested.connect(
            self.navigate
        )

        self.navigate("home")

    def navigate(self, page_name):
        if page_name == "logout":
            self.main_window.logout()
            return

        page = self.pages.get(page_name)

        if page is None:
            return

        self.stack.setCurrentWidget(page)
        self.sidebar.set_active(page_name)