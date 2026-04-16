"""
构建配置常量
"""

from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
ASSETS_DIR = PROJECT_ROOT / "assets"

# 平台特定配置
PLATFORM_CONFIG = {
    "windows": {
        "name": "ddnet-change-color",
        "console": False,  # 隐藏控制台窗口
        "icon": str(ASSETS_DIR / "windows" / "icon.ico"),
        "version_file": str(PROJECT_ROOT / "version_info.txt"),
        "output_ext": ".exe",
        "platform_name": "Windows",
        "artifact_name": "ddnet-change-color-windows",
    },
    "darwin": {
        "name": "DDNet Change Color",
        "console": False,
        "icon": str(ASSETS_DIR / "macos" / "icon.icns"),
        "info_plist": str(PROJECT_ROOT / "Info.plist.template"),
        "output_ext": "",
        "platform_name": "macOS",
        "artifact_name": "ddnet-change-color-macos",
        "bundle_identifier": "com.ddnet.change-color",
    },
    "linux": {
        "name": "ddnet-change-color",
        "console": True,  # 显示控制台（方便调试）
        "icon": str(ASSETS_DIR / "linux" / "icon.png"),
        "desktop_file": str(PROJECT_ROOT / "ddnet-change-color.desktop"),
        "output_ext": "",
        "platform_name": "Linux",
        "artifact_name": "ddnet-change-color-linux",
    },
}

# 构建配置
BUILD_CONFIG = {
    "main_script": str(SRC_DIR / "ddnet_change_color" / "__main__.py"),
    "spec_file": str(PROJECT_ROOT / "ddnet-change-color.spec"),
    "dist_dir": str(PROJECT_ROOT / "dist"),
    "build_dir": str(PROJECT_ROOT / "build"),
    "hidden_imports": [
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
    ],
    "excludes": [],
    "upx": True,  # 启用 UPX 压缩
    "upx_exclude": [],
    "pathex": [str(SRC_DIR)],
}
