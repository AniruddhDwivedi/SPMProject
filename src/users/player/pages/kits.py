from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
)

from src.services.kit_service import KitService
from src.components.wave_heading import WaveHeading

SPORTS = [
    "Athletics", "Badminton", "Basketball", "Cricket", "Football",
    "Hockey", "Lawn Tennis", "Squash", "Swimming", "Table Tennis",
    "Volleyball", "Water Polo", "Weightlifting",
]

KIT_TYPE = "Standard kit"

class PlayerKitsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = KitService()
        self.inventory = []

        self.setup_ui()
        self.load_inventory()
        self.load_requests()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Playing Kit Requests")
        title.setObjectName("page_title")

        description = QLabel(
            "Request your tournament kit and track its collection status."
        )
        description.setWordWrap(True)

        form = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Your full name")

        self.vit_input = QLineEdit()
        self.vit_input.setPlaceholderText("Your VIT / team")

        self.sport_input = QComboBox()
        self.sport_input.addItems(SPORTS)
        self.sport_input.currentTextChanged.connect(
            self.update_stock_display
        )

        # Kit type is predetermined; no dropdown is required.
        self.kit_label = QLabel(KIT_TYPE)

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 20)
        self.quantity_input.setValue(1)

        form.addRow("Player name *", self.name_input)
        form.addRow("VIT / team *", self.vit_input)
        form.addRow("Sport *", self.sport_input)
        form.addRow("Kit type", self.kit_label)
        form.addRow("Quantity *", self.quantity_input)

        self.stock_label = QLabel("Inventory not loaded.")
        self.stock_label.setWordWrap(True)

        self.submit_button = QPushButton("Submit Kit Request")
        self.submit_button.clicked.connect(self.submit_request)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_all)

        actions = QHBoxLayout()
        actions.addWidget(self.submit_button)
        actions.addWidget(self.refresh_button)
        actions.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Requested", "Sport", "Kit", "Qty", "Status", "Message",
        ])
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(QLabel("New request"))
        layout.addLayout(form)
        layout.addWidget(self.stock_label)
        layout.addLayout(actions)
        layout.addWidget(QLabel("My kit requests"))
        layout.addWidget(self.table)
        layout.addWidget(self.message)

    def load_inventory(self):
        try:
            self.inventory = self.service.get_inventory()
            self.update_stock_display()
        except Exception as error:
            self.inventory = []
            print("KIT INVENTORY LOAD ERROR:", repr(error))
            self.stock_label.setText(
                "Could not load inventory. Check Supabase permissions."
            )

    def update_stock_display(self, *_):
        sport = self.sport_input.currentText()

        matching_stock = next(
            (
                item for item in self.inventory
                if item.get("sport") == sport
                and item.get("kit_type") == KIT_TYPE
            ),
            None,
        )

        if matching_stock:
            quantity = matching_stock.get("available_quantity", 0)
            self.stock_label.setText(
                f"Available {KIT_TYPE} stock for {sport}: {quantity}"
            )
        else:
            self.stock_label.setText(
                f"No {KIT_TYPE} inventory record exists for {sport}. "
                "You can still submit a request for the organizer to review."
            )

    def submit_request(self):
        try:
            self.submit_button.setEnabled(False)

            self.service.submit_request(
                player_name=self.name_input.text(),
                vit_name=self.vit_input.text(),
                sport=self.sport_input.currentText(),
                kit_type=KIT_TYPE,
                quantity=self.quantity_input.value(),
            )

            self.name_input.clear()
            self.message.setText("Kit request submitted successfully.")
            self.load_requests()

        except Exception as error:
            print("KIT REQUEST ERROR:", repr(error))
            QMessageBox.warning(
                self, "Request failed", str(error)
            )
        finally:
            self.submit_button.setEnabled(True)

    def load_requests(self):
        try:
            requests = self.service.get_my_requests()
            self.table.setRowCount(len(requests))

            for row, request in enumerate(requests):
                collection = request.get("collection_at")
                resubmit = request.get("resubmit_after")
                status = request.get("status") or "Submitted"

                message = request.get("organizer_message") or ""

                if collection:
                    message = f"Collect: {collection}"
                elif (
                    status == "Unavailable - Resubmit Tomorrow"
                    and resubmit
                ):
                    message = f"Resubmit after: {resubmit}"

                values = [
                    str(request.get("created_at") or "")[:16],
                    request.get("sport") or "",
                    request.get("kit_type") or "",
                    str(request.get("quantity") or 1),
                    status,
                    message,
                ]

                for column, value in enumerate(values):
                    self.table.setItem(
                        row,
                        column,
                        QTableWidgetItem(str(value)),
                    )

            self.message.setText(
                f"Loaded {len(requests)} kit requests."
            )

        except Exception as error:
            print("MY KIT REQUESTS ERROR:", repr(error))
            self.message.setText(
                "Could not load your requests. Check your player account."
            )

    def refresh_all(self):
        self.load_inventory()
        self.load_requests()
