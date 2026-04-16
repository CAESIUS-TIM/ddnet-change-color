"""
macOS 平台特定配置
"""

from pathlib import Path
from typing import Any, Dict, List


def get_macos_specific_config(base_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    获取 macOS 特定配置

    参数:
        base_config: 基础配置字典

    返回:
        Dict[str, Any]: 更新后的配置
    """
    config = base_config.copy()

    # macOS 特定隐藏导入
    config.setdefault("hidden_imports", []).extend(
        [
            "objc",  # Objective-C 桥接
            "Foundation",
            "AppKit",
        ]
    )

    # macOS 特定排除模块
    config.setdefault("excludes", []).extend(
        [
            "PySide6.QtWebEngine",
            "PySide6.QtWebEngineCore",
            "PySide6.QtWebEngineWidgets",
            "PySide6.QtWebSockets",
            "PySide6.QtQuick3D",
        ]
    )

    # macOS 应用包配置
    config["bundle"] = {
        "name": config.get("name", "DDNet Change Color"),
        "identifier": config.get("bundle_identifier", "com.ddnet.change-color"),
        "version": config.get("version", "1.0.0"),
        "signature": "????",  # 开发者签名（可选）
        "entitlements": None,  # 权限文件（可选）
    }

    # macOS 特定 UPX 排除
    config.setdefault("upx_exclude", []).extend(
        [
            "libqcocoa.dylib",  # Qt macOS 平台插件
        ]
    )

    # macOS 二进制优化
    config["binary_optimization"] = True

    return config


def get_macos_pyinstaller_args(config: Dict[str, Any]) -> List[str]:
    """
    获取 macOS 特定 PyInstaller 参数

    参数:
        config: 平台配置

    返回:
        List[str]: 附加参数列表
    """
    args = []

    # macOS 应用包设置
    args.append("--windowed")
    args.extend(["--name", config.get("name", "DDNet Change Color")])

    # 图标文件
    if config.get("icon") and Path(config["icon"]).exists():
        args.extend(["--icon", config["icon"]])

    # Info.plist 文件
    if config.get("info_plist") and Path(config["info_plist"]).exists():
        args.extend(["--info-plist", config["info_plist"]])

    # macOS 应用包优化
    args.append("--osx-bundle-identifier")
    args.append(config.get("bundle_identifier", "com.ddnet.change-color"))

    # 代码签名（可选）
    if config.get("codesign_identity"):
        args.extend(["--codesign-identity", config["codesign_identity"]])

    # 公证（可选）
    if config.get("notarize"):
        args.append("--notarize")

    return args


def validate_macos_environment() -> bool:
    """
    验证 macOS 构建环境

    返回:
        bool: 环境是否有效
    """
    import platform
    import subprocess
    import sys

    if not sys.platform.startswith("darwin"):
        print("警告: 当前不是 macOS 系统")
        return False

    # 检查 macOS 版本
    mac_version = platform.mac_ver()[0]
    print(f"macOS 版本: {mac_version}")

    # 检查必要工具
    try:
        import PySide6

        print(f"PySide6 版本: {PySide6.__version__}")
    except ImportError:
        print("错误: PySide6 未安装")
        return False

    # 检查 Xcode 命令行工具（可选）
    try:
        result = subprocess.run(["xcode-select", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Xcode 命令行工具已安装")
    except FileNotFoundError:
        print("Xcode 命令行工具未安装（可选）")

    # 检查 UPX（可选）
    import shutil

    if shutil.which("upx"):
        print("UPX 已安装")
    else:
        print("UPX 未安装，二进制文件将不会被压缩")

    return True
