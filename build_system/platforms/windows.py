"""
Windows 平台特定配置
"""

from pathlib import Path
from typing import Any, Dict, List


def get_windows_specific_config(base_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    获取 Windows 特定配置

    参数:
        base_config: 基础配置字典

    返回:
        Dict[str, Any]: 更新后的配置
    """
    config = base_config.copy()

    # Windows 特定隐藏导入
    config.setdefault("hidden_imports", []).extend(
        [
            "pywintypes",  # Windows API 类型
            "win32api",  # Windows API
            "win32process",
            "win32security",
        ]
    )

    # Windows 特定排除模块
    config.setdefault("excludes", []).extend(
        [
            "PySide6.QtQml",
            "PySide6.QtQuick",
            "PySide6.QtWebEngine",
            "PySide6.QtWebEngineCore",
            "PySide6.QtWebEngineWidgets",
            "PySide6.QtWebSockets",
        ]
    )

    # Windows 运行时文件
    config["runtime_files"] = [
        # MSVC 运行时库（如果需要）
    ]

    # Windows 特定 UPX 排除
    config.setdefault("upx_exclude", []).extend(
        [
            "vcruntime140.dll",
            "vcruntime140_1.dll",
            "msvcp140.dll",
            "api-ms-win-*.dll",
        ]
    )

    # Windows 二进制优化
    config["binary_optimization"] = True

    return config


def get_windows_pyinstaller_args(config: Dict[str, Any]) -> List[str]:
    """
    获取 Windows 特定 PyInstaller 参数

    参数:
        config: 平台配置

    返回:
        List[str]: 附加参数列表
    """
    args = []

    # Windows 控制台设置
    if not config.get("console", False):
        args.append("--windowed")

    # 图标文件
    if config.get("icon") and Path(config["icon"]).exists():
        args.extend(["--icon", config["icon"]])

    # 版本信息文件
    if config.get("version_file") and Path(config["version_file"]).exists():
        args.extend(["--version-file", config["version_file"]])

    # Windows 特定资源
    if config.get("manifest"):
        args.extend(["--manifest", config["manifest"]])

    # UAC 管理员权限（默认不需要）
    if config.get("uac_admin"):
        args.append("--uac-admin")

    return args


def validate_windows_environment() -> bool:
    """
    验证 Windows 构建环境

    返回:
        bool: 环境是否有效
    """
    import platform
    import sys

    if not sys.platform.startswith("win"):
        print("警告: 当前不是 Windows 系统")
        return False

    # 检查 Windows 版本
    win_version = platform.version()
    print(f"Windows 版本: {win_version}")

    # 检查必要工具
    try:
        import PySide6

        print(f"PySide6 版本: {PySide6.__version__}")
    except ImportError:
        print("错误: PySide6 未安装")
        return False

    # 检查 UPX（可选）
    import shutil

    if shutil.which("upx"):
        print("UPX 已安装")
    else:
        print("UPX 未安装，二进制文件将不会被压缩")

    return True
