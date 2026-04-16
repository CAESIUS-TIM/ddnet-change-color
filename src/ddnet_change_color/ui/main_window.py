import logging
from pathlib import Path
from typing import override

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QColor,
    QGuiApplication,
)
from PySide6.QtWidgets import (
    QColorDialog,
    QDialog,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QWidget,
)

from ..dialogs.settings_dialog import SettingsDialog
from ..models.color_store import ColorStore
from ..widgets.color_item import ColorItemWidget
from ..widgets.color_list import ColorListWidget

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.store: ColorStore = ColorStore()

        self.setWindowTitle("DDNet 换色工具")
        self.resize(500, 400)
        self.setMinimumSize(400, 300)

        self._setup_ui()
        self._load_colors()

    def _setup_ui(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        add_btn = QPushButton("添加颜色")
        add_btn.clicked.connect(self.add_color)  # pyright: ignore[reportUnusedCallResult]
        toolbar.addWidget(add_btn)  # pyright: ignore[reportUnusedCallResult]

        export_btn = QPushButton("导出配置")
        export_btn.clicked.connect(self.export_config)  # pyright: ignore[reportUnusedCallResult]
        toolbar.addWidget(export_btn)  # pyright: ignore[reportUnusedCallResult]

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)  # pyright: ignore[reportUnusedCallResult]

        settings_btn = QPushButton("⚙️ 设置")
        settings_btn.clicked.connect(self.show_settings)  # pyright: ignore[reportUnusedCallResult]
        toolbar.addWidget(settings_btn)  # pyright: ignore[reportUnusedCallResult]

        self.list_widget: ColorListWidget = ColorListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportUnusedCallResult]
        self.list_widget.itemClicked.connect(self.on_item_clicked)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportUnusedCallResult]

        self.status_bar: QStatusBar = self.statusBar()
        self.update_status()

        self.setCentralWidget(self.list_widget)

    def _load_colors(self):
        self.list_widget.clear()
        for hex_color in self.store.colors:
            self._add_color_item(hex_color)

    def _add_color_item(self, hex_color: str, index: int = -1):
        item = QListWidgetItem()
        widget = ColorItemWidget(hex_color)
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.ItemDataRole.UserRole, hex_color)

        if index >= 0:
            self.list_widget.insertItem(index, item)
            self.list_widget.setItemWidget(item, widget)
        else:
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)

    def add_color(self):
        color = QColorDialog.getColor(title="选择颜色")
        if color.isValid():
            hex_color = color.name().upper()
            self.store.add_color(hex_color)
            self._add_color_item(hex_color)
            self.update_status()

    def show_settings(self):
        dialog = SettingsDialog(self.store, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_status()

    def update_status(self):
        count = len(self.store.colors)
        self.status_bar.showMessage(
            f"绑定键: {self.store.bind_key}  |  输出: {self.store.output_folder}  |  "
            f"共 {count} 个颜色"
        )

    def show_context_menu(self, pos: QPoint):
        item = self.list_widget.itemAt(pos)
        if not item:
            return

        index = self.list_widget.row(item)
        menu = QMenu(self)

        copy_action = QAction("复制", self)
        copy_action.triggered.connect(lambda: self.copy_color(index))  # pyright: ignore[reportUnusedCallResult]
        menu.addAction(copy_action)

        modify_action = QAction("修改", self)
        modify_action.triggered.connect(lambda: self.modify_color(index))  # pyright: ignore[reportUnusedCallResult]
        menu.addAction(modify_action)

        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: self.delete_color(index))  # pyright: ignore[reportUnusedCallResult]
        menu.addAction(delete_action)

        menu.exec(self.list_widget.mapToGlobal(pos))  # pyright: ignore[reportUnusedCallResult]

    def copy_color(self, index: int):
        if 0 <= index < len(self.store.colors):
            hex_color = self.store.colors[index]
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(hex_color)
            self.status_bar.showMessage(f"已复制: {hex_color}", 2000)

    def modify_color(self, index: int):
        if 0 <= index < len(self.store.colors):
            current_color = self.store.colors[index]
            color = QColorDialog.getColor(QColor(current_color), self, "修改颜色")
            if color.isValid():
                hex_color = color.name().upper()
                self.store.update_color(index, hex_color)

                item = self.list_widget.item(index)
                # Method A
                widget = self.list_widget.itemWidget(item)
                if isinstance(widget, ColorItemWidget):
                    widget.update_color(hex_color)
                else:
                    raise TypeError(
                        f"Expected ColorItemWidget, got {type(widget).__name__} "
                        + f"(value: {widget})"
                    )
                # Method B
                # from typing import cast
                # widget = cast(ColorItemWidget, self.list_widget.itemWidget(item))
                # widget.update_color(hex_color)
                item.setData(Qt.ItemDataRole.UserRole, hex_color)

    def delete_color(self, index: int):
        if 0 <= index < len(self.store.colors):
            self.store.remove_color(index)
            self.list_widget.takeItem(index)  # pyright: ignore[reportUnusedCallResult]
            self.update_status()

    def on_item_clicked(self, item: QListWidgetItem) -> None:
        pass

    def export_config(self):
        if not self.store.colors:
            QMessageBox.warning(self, "警告", "没有颜色可导出")  # pyright: ignore[reportUnusedCallResult]
            return

        folder = Path(self.store.output_folder)
        try:
            folder.mkdir(parents=True, exist_ok=True)

            if any(folder.iterdir()):
                reply = QMessageBox.question(
                    self,
                    "确认",
                    f"目录 '{folder}' 不为空，是否清空？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    for f in folder.iterdir():
                        f.unlink()
                else:
                    return

            bind_key = self.store.bind_key
            colors = self.store.colors

            for i, color in enumerate(colors):
                cfg_file = folder / f"change-color{i}.cfg"
                next_idx = (i + 1) % len(colors)
                with open(cfg_file, "w") as f:
                    f.write(  # pyright: ignore[reportUnusedCallResult]
                        f"bind {bind_key} exec {folder / f'change-color{next_idx}.cfg'}\n"
                    )
                    f.write(f"player_color_body {color}\n")  # pyright: ignore[reportUnusedCallResult]
                    f.write(f"player_color_feet {color}\n")  # pyright: ignore[reportUnusedCallResult]
                    f.write(f"dummy_color_body {color}\n")  # pyright: ignore[reportUnusedCallResult]
                    f.write(f"dummy_color_feet {color}\n")  # pyright: ignore[reportUnusedCallResult]

            QMessageBox.information(  # pyright: ignore[reportUnusedCallResult]
                self, "成功", f"已导出 {len(colors)} 个配置文件到:\n{folder.absolute()}"
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {e}")  # pyright: ignore[reportUnusedCallResult]

    @override
    def closeEvent(self, event: QCloseEvent):
        new_order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            hex_color = item.data(Qt.ItemDataRole.UserRole)  # pyright: ignore[reportAny]
            new_order.append(hex_color)  # pyright: ignore[reportUnknownMemberType, reportAny]

        if new_order != self.store.colors:
            self.store.colors = new_order
            self.store.save()
        event.accept()
