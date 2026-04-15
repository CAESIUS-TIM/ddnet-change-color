"""向后兼容模块：重新导出所有公共类

注意：新代码应使用显式导入，例如：
- from ddnet_change_color.models.color_store import ColorStore
- from ddnet_change_color.dialogs.settings_dialog import SettingsDialog
- from ddnet_change_color.widgets.color_list import ColorListWidget
- from ddnet_change_color.widgets.color_item import ColorItemWidget
- from ddnet_change_color.ui.main_window import MainWindow
"""

from .models.color_store import ColorStore
from .dialogs.settings_dialog import SettingsDialog
from .widgets.color_list import ColorListWidget
from .widgets.color_item import ColorItemWidget
from .ui.main_window import MainWindow

__all__ = [
    "ColorStore",
    "SettingsDialog",
    "ColorListWidget",
    "ColorItemWidget",
    "MainWindow",
]