from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QCheckBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from src.components.wave_heading import WaveHeading
from src.services.player_reporting_service import PlayerReportingService


class PlayerReportingPage(QWidget):
    def __init__(self):
        super().__init__()

        self.service = PlayerReportingService()
        self.players = []
        self.selected_report_id = None

        self.setup_ui()
        self.load_players()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Initial Player Reporting")
        title.setObjectName("page_title")

        description = QLabel(
            "Register players arriving at the host IIT and track "
            "documents, accommodation, ID cards, and credentials."
        )
        description.setWordWrap(True)

        # Registration fields
        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Player's full name")

        self.player_id_input = QLineEdit()
        self.player_id_input.setPlaceholderText(
            "Optional tournament/player ID"
        )

        self.iit_input = QLineEdit()
        self.iit_input.setPlaceholderText("e.g. IIT Delhi")

        self.sport_input = QComboBox()
        self.sport_input.setEditable(True)
        self.sport_input.addItems([
            "Athletics",
            "Badminton",
            "Basketball",
            "Cricket",
            "Football",
            "Hockey",
            "Lawn Tennis",
            "Squash",
            "Swimming",
            "Table Tennis",
            "Volleyball",
            "Water Polo",
            "Weightlifting",
        ])

        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(70)

        form.addRow("Player name *", self.name_input)
        form.addRow("Player ID", self.player_id_input)
        form.addRow("IIT / team *", self.iit_input)
        form.addRow("Sport *", self.sport_input)
        form.addRow("Email", self.email_input)
        form.addRow("Phone", self.phone_input)
        form.addRow("Notes", self.notes_input)

        self.register_button = QPushButton("Register Player")
        self.register_button.clicked.connect(self.register_player)

        # Registration progress fields for the selected player
        self.documents_check = QCheckBox("Documents received")
        self.hall_check = QCheckBox("Hall allocated")
        self.id_card_check = QCheckBox("ID card issued")
        self.credentials_check = QCheckBox("Credentials created")

        self.hall_input = QLineEdit()
        self.hall_input.setPlaceholderText("Allocated hall / room")

        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Pending",
            "In Progress",
            "Complete",
        ])

        self.update_button = QPushButton("Update Selected Player")
        self.update_button.clicked.connect(self.update_player)
        self.update_button.setEnabled(False)

        self.refresh_button = QPushButton("Refresh Register")
        self.refresh_button.clicked.connect(self.load_players)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.documents_check)
        progress_layout.addWidget(self.hall_check)
        progress_layout.addWidget(self.id_card_check)
        progress_layout.addWidget(self.credentials_check)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.register_button)
        action_layout.addWidget(self.update_button)
        action_layout.addWidget(self.refresh_button)

        # Player register table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Player ID",
            "Player Name",
            "IIT / Team",
            "Sport",
            "Documents",
            "Hall",
            "Status",
        ])
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.itemSelectionChanged.connect(
            self.load_selected_player
        )

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(QLabel("Register a new player"))
        layout.addLayout(form)
        layout.addWidget(self.register_button)
        layout.addWidget(QLabel("Selected player's reporting progress"))
        layout.addLayout(progress_layout)

        hall_row = QHBoxLayout()
        hall_row.addWidget(QLabel("Hall / room:"))
        hall_row.addWidget(self.hall_input)
        hall_row.addWidget(QLabel("Reporting status:"))
        hall_row.addWidget(self.status_combo)
        layout.addLayout(hall_row)

        layout.addLayout(action_layout)
        layout.addWidget(QLabel("Registered players"))
        layout.addWidget(self.table)
        layout.addWidget(self.message)

    def register_player(self):
        data = {
            "player_name": self.name_input.text(),
            "player_id": self.player_id_input.text(),
            "iit_name": self.iit_input.text(),
            "sport": self.sport_input.currentText(),
            "email": self.email_input.text(),
            "phone": self.phone_input.text(),
            "notes": self.notes_input.toPlainText(),
        }

        try:
            self.service.register_player(data)
            self.clear_registration_form()
            self.load_players()
            self.message.setText("Player registered successfully.")
        except Exception as error:
            print("PLAYER REGISTRATION ERROR:", repr(error))
            QMessageBox.warning(
                self,
                "Registration failed",
                str(error),
            )

    def load_players(self):
        try:
            self.players = self.service.get_players()
            self.table.setRowCount(len(self.players))

            for row, player in enumerate(self.players):
                hall = player.get("hall_name") or (
                    "Allocated" if player.get("hall_allocated") else "Not allocated"
                )

                values = [
                    player.get("player_id") or "—",
                    player.get("player_name") or "",
                    player.get("iit_name") or "",
                    player.get("sport") or "",
                    "Received" if player.get("documents_received") else "Pending",
                    hall,
                    player.get("reporting_status") or "Pending",
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(
                        item.flags()
                        & ~Qt.ItemFlag.ItemIsEditable
                    )
                    self.table.setItem(row, column, item)

            self.message.setText(
                f"Loaded {len(self.players)} player records."
            )
        except Exception as error:
            print("PLAYER REGISTER LOAD ERROR:", repr(error))
            self.message.setText(
                "Could not load player records. Check your "
                "Supabase connection and organizer permissions."
            )

    def load_selected_player(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.players):
            self.selected_report_id = None
            self.update_button.setEnabled(False)
            return

        player = self.players[row]
        self.selected_report_id = player.get("id")

        self.documents_check.setChecked(
            bool(player.get("documents_received"))
        )
        self.hall_check.setChecked(
            bool(player.get("hall_allocated"))
        )
        self.id_card_check.setChecked(
            bool(player.get("id_card_issued"))
        )
        self.credentials_check.setChecked(
            bool(player.get("credentials_created"))
        )

        self.hall_input.setText(player.get("hall_name") or "")
        self.notes_input.setPlainText(player.get("notes") or "")
        self.status_combo.setCurrentText(
            player.get("reporting_status") or "Pending"
        )
        self.update_button.setEnabled(True)

    def update_player(self):
        if not self.selected_report_id:
            QMessageBox.information(
                self,
                "Select a player",
                "Select a player from the register first.",
            )
            return

        data = {
            "documents_received": self.documents_check.isChecked(),
            "hall_allocated": self.hall_check.isChecked(),
            "hall_name": self.hall_input.text(),
            "id_card_issued": self.id_card_check.isChecked(),
            "credentials_created": self.credentials_check.isChecked(),
            "reporting_status": self.status_combo.currentText(),
            "notes": self.notes_input.toPlainText(),
        }

        try:
            self.service.update_player(self.selected_report_id, data)
            self.load_players()
            self.message.setText("Player reporting details updated.")
        except Exception as error:
            print("PLAYER REPORT UPDATE ERROR:", repr(error))
            QMessageBox.warning(
                self,
                "Update failed",
                str(error),
            )

    def clear_registration_form(self):
        self.name_input.clear()
        self.player_id_input.clear()
        self.iit_input.clear()
        self.sport_input.setCurrentIndex(0)
        self.email_input.clear()
        self.phone_input.clear()
        self.notes_input.clear()
