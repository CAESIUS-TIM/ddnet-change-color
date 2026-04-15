import sys

from PySide6.QtWidgets import QApplication

from .log import setup_logging
from .ui.main_window import MainWindow


def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
