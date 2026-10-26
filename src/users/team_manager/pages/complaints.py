from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
)
from PyQt6.QtCore import Qt
from src.services.complaint_service import ComplaintService
from src.components.wave_heading import WaveHeading

class TeamManagerComplaintsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ComplaintService()
        self.complaints = []

        self.setup_ui()
        self.load_complaints()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = WaveHeading("Team Complaints")
        title.setObjectName("page_title")

        description = QLabel(
            "Submit a complaint to the tournament organizers "
            "and track its resolution."
        )
        description.setWordWrap(True)

        form = QFormLayout()

        self.team_input = QLineEdit()
        self.team_input.setPlaceholderText("Your VIT / team name")

        self.category_input = QComboBox()
        self.category_input.addItems([
            "Accommodation",
            "Transport",
            "Scheduling",
            "Facilities",
            "Conduct / Discipline",
            "Medical",
            "Other",
        ])

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Brief summary")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Describe the issue and include relevant details."
        )
        self.description_input.setMaximumHeight(110)

        form.addRow("VIT / team *", self.team_input)
        form.addRow("Category *", self.category_input)
        form.addRow("Subject *", self.subject_input)
        form.addRow("Description *", self.description_input)

        self.submit_button = QPushButton("Submit Complaint")
        self.submit_button.clicked.connect(self.submit_complaint)

        self.refresh_button = QPushButton("Refresh My Complaints")
        self.refresh_button.clicked.connect(self.load_complaints)

        buttons = QHBoxLayout()
        buttons.addWidget(self.submit_button)
        buttons.addWidget(self.refresh_button)
        buttons.addStretch()

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Submitted", "Category", "Subject", "Status", "Resolution",
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

        self.message = QLabel()
        self.message.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(QLabel("Submit a new complaint"))
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(QLabel("Your submitted complaints"))
        layout.addWidget(self.table)
        layout.addWidget(self.message)

    def submit_complaint(self):
        try:
            self.submit_button.setEnabled(False)

            self.service.submit_complaint(
                team_name=self.team_input.text(),
                category=self.category_input.currentText(),
                subject=self.subject_input.text(),
                description=self.description_input.toPlainText(),
            )

            self.subject_input.clear()
            self.description_input.clear()
            self.message.setText("Complaint submitted successfully.")
            self.load_complaints()

        except Exception as error:
            print("COMPLAINT SUBMISSION ERROR:", repr(error))
            QMessageBox.warning(
                self, "Submission failed", str(error)
            )
        finally:
            self.submit_button.setEnabled(True)

    def load_complaints(self):
        try:
            self.complaints = self.service.get_my_complaints()
            self.table.setRowCount(len(self.complaints))

            for row, complaint in enumerate(self.complaints):
                values = [
                    str(complaint.get("created_at") or "")[:16],
                    complaint.get("category") or "",
                    complaint.get("subject") or "",
                    complaint.get("status") or "Submitted",
                    complaint.get("resolution") or "Awaiting response",
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
            print("MY COMPLAINTS LOAD ERROR:", repr(error))
            self.message.setText(
                "Could not load complaints. Confirm you are logged "
                "in with a team_manager account and check Supabase."
            )
