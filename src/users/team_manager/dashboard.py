from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)
from src.components.sidebar import Sidebar
from src.users.team_manager.pages.home import TeamManagerHomePage
from src.users.team_manager.pages.complaints import (
    TeamManagerComplaintsPage,
)

class TeamManagerDashboard(QWidget):
    def __init__(self, user, main_window):
        super().__init__()

        self.user = user
        self.main_window = main_window

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar(
            "VITMS Team Manager",
            [
                ("home", "Dashboard"),
                ("complaints", "Complaints"),
            ],
        )

        self.stack = QStackedWidget()

        self.pages = {
            "home": TeamManagerHomePage(self.user),
            "complaints": TeamManagerComplaintsPage(),
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
