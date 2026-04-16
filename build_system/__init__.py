"""
构建模块

提供跨平台构建功能，支持 Windows、macOS 和 Linux。
"""

from .builder import Builder, build_for_platform, build_all_platforms
from .utils import collect_qt_plugins, get_platform_config, get_version, validate_assets
from .config import PLATFORM_CONFIG, BUILD_CONFIG, PROJECT_ROOT, SRC_DIR, ASSETS_DIR

__all__ = [
    "Builder",
    "build_for_platform",
    "build_all_platforms",
    "collect_qt_plugins", 
    "get_platform_config",
    "get_version",
    "validate_assets",
    "PLATFORM_CONFIG",
    "BUILD_CONFIG",
    "PROJECT_ROOT",
    "SRC_DIR",
    "ASSETS_DIR",
]