"""包级配置和常量管理"""

from pathlib import Path

# 包名常量，用于避免硬编码
PACKAGE_NAME = "ddnet_change_color"

# 配置目录和文件路径
CONFIG_DIR = Path.home() / ".ddnet-change-color"
CONFIG_FILE = CONFIG_DIR / "colors.json"