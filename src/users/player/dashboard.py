from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from src.components.sidebar import Sidebar

from src.users.player.pages.home import PlayerHomePage
from src.users.player.pages.schedule import PlayerSchedulePage
from src.users.player.pages.scoreboard import PlayerScoreboardPage


class PlayerDashboard(QWidget):

    def __init__(self, user, main_window):
        super().__init__()

        self.user = user
        self.main_window = main_window

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar(
            "IITMS Player",
            [
                ("home", "Dashboard"),
                ("schedule", "View Schedule"),
                ("scoreboard", "View Scoreboard"),
            ],
        )

        self.stack = QStackedWidget()

        self.pages = {
            "home": PlayerHomePage(self.user),
            "schedule": PlayerSchedulePage(),
            "scoreboard": PlayerScoreboardPage(),
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