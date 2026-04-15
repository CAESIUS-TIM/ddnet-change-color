"""颜色项小部件"""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget


class ColorItemWidget(QWidget):
    def __init__(self, hex_color: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.hex_color: str = hex_color

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        self.handle_label: QLabel = QLabel("☰")
        self.handle_label.setStyleSheet("color: #888;")
        layout.addWidget(self.handle_label)

        self.color_label: QLabel = QLabel()
        self.color_label.setFixedSize(40, 25)
        layout.addWidget(self.color_label)

        self.hex_label: QLabel = QLabel(hex_color.upper())
        self.hex_label.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.hex_label)

        layout.addStretch()

        self.update_color(hex_color)

    def update_color(self, hex_color: str):
        self.hex_color = hex_color
        self.color_label.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #aaa;")
        self.hex_label.setText(hex_color.upper())
