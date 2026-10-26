from datetime import datetime
from src.components.wave_heading import WaveHeading
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSpinBox, QLineEdit, QTextEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDateTimeEdit,
)
from PyQt6.QtCore import Qt, QDateTime
from src.services.kit_service import KitService

class OrganizerKitsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = KitService()
        self.requests = []
        self.selected_request_id = None

        self.setup_ui()
        self.load_inventory()
        self.load_requests()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Playing Kit Distribution")
        title.setObjectName("page_title")

        description = QLabel(
            "Review requests, check stock, schedule collection, "
            "and confirm kit distribution."
        )
        description.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Requested", "Player", "IIT / Team", "Sport",
            "Kit / Qty", "Status",
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
            self.load_selected_request
        )

        self.details = QLabel("Select a request to review it.")
        self.details.setWordWrap(True)

        self.collection_time = QDateTimeEdit()
        self.collection_time.setCalendarPopup(True)
        self.collection_time.setDisplayFormat("dd MMM yyyy HH:mm")
        self.collection_time.setDateTime(
            QDateTime.currentDateTime().addSecs(3600)
        )

        self.organizer_message = QTextEdit()
        self.organizer_message.setPlaceholderText(
            "Collection instructions or reason for unavailability."
        )
        self.organizer_message.setMaximumHeight(75)

        self.review_status = QComboBox()
        self.review_status.addItems([
            "Available for Collection",
            "Unavailable - Resubmit Tomorrow",
            "Fulfilled",
        ])

        self.save_review_button = QPushButton("Save Review")
        self.save_review_button.clicked.connect(self.save_review)
        self.save_review_button.setEnabled(False)

        self.refresh_button = QPushButton("Refresh Requests")
        self.refresh_button.clicked.connect(self.load_requests)

        review_form = QFormLayout()
        review_form.addRow("Decision", self.review_status)
        review_form.addRow("Collection date/time", self.collection_time)
        review_form.addRow("Message", self.organizer_message)

        review_actions = QHBoxLayout()
        review_actions.addWidget(self.save_review_button)
        review_actions.addWidget(self.refresh_button)
        review_actions.addStretch()

        # Inventory controls
        self.inventory_sport = QComboBox()
        self.inventory_sport.addItems([
            "Athletics", "Badminton", "Basketball", "Cricket",
            "Football", "Hockey", "Lawn Tennis", "Squash",
            "Swimming", "Table Tennis", "Volleyball", "Water Polo",
            "Weightlifting",
        ])

        self.inventory_kit = QLabel("Standard kit")

        self.inventory_quantity = QSpinBox()
        self.inventory_quantity.setRange(0, 100000)

        self.save_inventory_button = QPushButton("Save Inventory")
        self.save_inventory_button.clicked.connect(
            self.save_inventory
        )

        inventory_form = QFormLayout()
        inventory_form.addRow("Sport", self.inventory_sport)
        inventory_form.addRow("Kit type", self.inventory_kit)
        inventory_form.addRow("Available quantity", self.inventory_quantity)

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(QLabel("Incoming kit requests"))
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Selected request"))
        layout.addWidget(self.details)
        layout.addLayout(review_form)
        layout.addLayout(review_actions)
        layout.addWidget(QLabel("Manage kit inventory"))
        layout.addLayout(inventory_form)
        layout.addWidget(self.save_inventory_button)
        layout.addWidget(self.message)

    def load_inventory(self):
        try:
            inventory = self.service.get_inventory()
            self.inventory_rows = inventory
        except Exception as error:
            self.inventory_rows = []
            print("ORGANIZER INVENTORY LOAD ERROR:", repr(error))

    def save_inventory(self):
        sport = self.inventory_sport.currentText()
        kit_type = self.inventory_kit.text().strip()
        quantity = self.inventory_quantity.value()

        if not kit_type:
            QMessageBox.warning(
                self, "Missing kit type", "Enter a kit type."
            )
            return

        try:
            self.service.set_inventory(sport, kit_type, quantity)
            self.load_inventory()
            self.message.setText("Inventory saved.")
        except Exception as error:
            print("INVENTORY SAVE ERROR:", repr(error))
            QMessageBox.warning(self, "Inventory failed", str(error))

    def load_requests(self):
        try:
            self.requests = self.service.get_all_requests()
            self.table.setRowCount(len(self.requests))

            for row, request in enumerate(self.requests):
                values = [
                    str(request.get("created_at") or "")[:16],
                    request.get("player_name") or "",
                    request.get("iit_name") or "",
                    request.get("sport") or "",
                    f'{request.get("kit_type", "")} / '
                    f'{request.get("quantity", 1)}',
                    request.get("status") or "Submitted",
                ]

                for column, value in enumerate(values):
                    self.table.setItem(
                        row, column, QTableWidgetItem(str(value))
                    )

            self.message.setText(
                f"Loaded {len(self.requests)} requests."
            )

        except Exception as error:
            print("ORGANIZER KIT REQUEST LOAD ERROR:", repr(error))
            self.message.setText(
                "Could not load requests. Check organizer permissions."
            )

    def load_selected_request(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.requests):
            self.selected_request_id = None
            self.save_review_button.setEnabled(False)
            return

        request = self.requests[row]
        self.selected_request_id = request.get("id")

        self.details.setText(
            f'Player: {request.get("player_name", "")}\n'
            f'Team: {request.get("iit_name", "")}\n'
            f'Sport / kit: {request.get("sport", "")} / '
            f'{request.get("kit_type", "")}\n'
            f'Quantity: {request.get("quantity", 1)}\n'
            f'Current status: {request.get("status", "Submitted")}'
        )

        status = request.get("status", "Submitted")
        if status == "Unavailable - Resubmit Tomorrow":
            self.review_status.setCurrentText(status)
        elif status == "Fulfilled":
            self.review_status.setCurrentText("Fulfilled")
        else:
            self.review_status.setCurrentText(
                "Available for Collection"
            )

        self.organizer_message.setPlainText(
            request.get("organizer_message") or ""
        )

        self.save_review_button.setEnabled(
            status != "Fulfilled" and self.selected_request_id is not None
        )

    def save_review(self):
        if not self.selected_request_id:
            return

        decision = self.review_status.currentText()
        collection_at = None

        if decision == "Available for Collection":
            value = self.collection_time.dateTime().toPyDateTime()
            collection_at = value

        try:
            self.service.review_request(
                request_id=self.selected_request_id,
                decision=decision,
                message=self.organizer_message.toPlainText(),
                collection_at=collection_at,
            )
            self.message.setText("Kit request updated.")
            self.load_inventory()
            self.load_requests()

        except Exception as error:
            print("KIT REVIEW ERROR:", repr(error))
            QMessageBox.warning(
                self, "Review failed", str(error)
            )
