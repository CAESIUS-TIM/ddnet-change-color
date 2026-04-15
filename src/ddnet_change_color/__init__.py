"""DDNet 换色工具包

主要导出：
- main: 应用入口函数
- MainWindow: 主窗口类
- ColorStore: 颜色存储模型
- 其他类可通过相应模块导入
"""

from .__main__ import main
from .dialogs.settings_dialog import SettingsDialog
from .models.color_store import ColorStore
from .ui.main_window import MainWindow
from .widgets.color_item import ColorItemWidget
from .widgets.color_list import ColorListWidget

__all__ = [
    "main",
    "ColorStore",
    "SettingsDialog",
    "ColorListWidget",
    "ColorItemWidget",
    "MainWindow",
]

__version__ = "0.1.0"
