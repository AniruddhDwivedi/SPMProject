from src.components.wave_heading import WaveHeading
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QTextEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox,
)
from PyQt6.QtCore import Qt
from src.services.complaint_service import ComplaintService

class OrganizerComplaintsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ComplaintService()
        self.complaints = []
        self.selected_complaint_id = None

        self.setup_ui()
        self.load_complaints()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Manage Team Complaints")
        title.setObjectName("page_title")

        description = QLabel(
            "Review team complaints, update their status, "
            "and provide a resolution."
        )
        description.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Submitted", "Team", "Category", "Subject", "Status",
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
            self.load_selected_complaint
        )

        self.details = QTextEdit()
        self.details.setReadOnly(True)
        self.details.setPlaceholderText(
            "Select a complaint to view its full description."
        )
        self.details.setMaximumHeight(100)

        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Submitted",
            "Under Review",
            "Resolved",
        ])

        self.resolution_input = QTextEdit()
        self.resolution_input.setPlaceholderText(
            "Enter the response or resolution for the team."
        )
        self.resolution_input.setMaximumHeight(100)

        self.save_button = QPushButton("Save Complaint Update")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_update)

        self.refresh_button = QPushButton("Refresh Complaints")
        self.refresh_button.clicked.connect(self.load_complaints)

        actions = QHBoxLayout()
        actions.addWidget(QLabel("Status:"))
        actions.addWidget(self.status_combo)
        actions.addWidget(self.save_button)
        actions.addWidget(self.refresh_button)

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.table)
        layout.addWidget(QLabel("Complaint description"))
        layout.addWidget(self.details)
        layout.addLayout(actions)
        layout.addWidget(QLabel("Resolution / response"))
        layout.addWidget(self.resolution_input)
        layout.addWidget(self.message)

    def load_complaints(self):
        try:
            self.complaints = self.service.get_all_complaints()
            self.table.setRowCount(len(self.complaints))
            self.selected_complaint_id = None
            self.save_button.setEnabled(False)

            for row, complaint in enumerate(self.complaints):
                values = [
                    str(complaint.get("created_at") or "")[:16],
                    complaint.get("team_name") or "",
                    complaint.get("category") or "",
                    complaint.get("subject") or "",
                    complaint.get("status") or "Submitted",
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    item.setFlags(
                        item.flags() & ~Qt.ItemFlag.ItemIsEditable
                    )
                    self.table.setItem(row, column, item)

            self.message.setText(
                f"Loaded {len(self.complaints)} complaints."
            )

        except Exception as error:
            print("ORGANIZER COMPLAINT LOAD ERROR:", repr(error))
            self.message.setText(
                "Could not load complaints. Confirm organizer access "
                "and check the Supabase policies."
            )

    def load_selected_complaint(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.complaints):
            self.selected_complaint_id = None
            self.save_button.setEnabled(False)
            return

        complaint = self.complaints[row]
        self.selected_complaint_id = complaint.get("id")

        self.details.setPlainText(
            complaint.get("description") or ""
        )
        self.resolution_input.setPlainText(
            complaint.get("resolution") or ""
        )
        self.status_combo.setCurrentText(
            complaint.get("status") or "Submitted"
        )
        self.save_button.setEnabled(
            self.selected_complaint_id is not None
        )

    def save_update(self):
        if not self.selected_complaint_id:
            return

        try:
            self.service.update_complaint(
                complaint_id=self.selected_complaint_id,
                status=self.status_combo.currentText(),
                resolution=self.resolution_input.toPlainText(),
            )

            self.message.setText("Complaint updated successfully.")
            self.load_complaints()

        except Exception as error:
            print("COMPLAINT UPDATE ERROR:", repr(error))
            QMessageBox.warning(
                self, "Update failed", str(error)
            )
