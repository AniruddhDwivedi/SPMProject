import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from src.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(
        "Inter IIT Tournament Management System"
    )

    stylesheet_path = (
        Path(__file__).parent / "src" / "style.qss"
    )

    with open(stylesheet_path, "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()