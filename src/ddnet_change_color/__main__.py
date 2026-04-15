import sys
from ddnet_change_color.widget import MainWindow
from PyQt6.QtWidgets import QApplication
from ddnet_change_color.log import setup_logging


def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
