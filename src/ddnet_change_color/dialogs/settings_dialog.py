"""设置对话框"""

from typing import override

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..models.color_store import ColorStore


class SettingsDialog(QDialog):
    def __init__(self, store: ColorStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store: ColorStore = store
        self.setWindowTitle("设置")
        self.setModal(True)

        layout = QVBoxLayout(self)

        bind_layout = QHBoxLayout()
        bind_layout.addWidget(QLabel("绑定键:"))
        self.bind_edit: QLineEdit = QLineEdit(self.store.bind_key)
        self.bind_edit.setMaximumWidth(100)
        bind_layout.addWidget(self.bind_edit)
        layout.addLayout(bind_layout)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("输出目录:"))
        self.folder_edit: QLineEdit = QLineEdit(self.store.output_folder)
        self.folder_edit.setReadOnly(True)
        folder_layout.addWidget(self.folder_edit)
        self.folder_btn: QPushButton = QPushButton("选择...")
        self.folder_btn.clicked.connect(self.choose_folder)
        folder_layout.addWidget(self.folder_btn)
        layout.addLayout(folder_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.store.output_folder
        )
        if folder:
            self.folder_edit.setText(folder)

    @override
    def accept(self):
        self.store.bind_key = self.bind_edit.text().strip() or "w"
        self.store.output_folder = self.folder_edit.text().strip() or "./change-colors"
        self.store.save()
        super().accept()
