"""
Linux 平台特定配置
"""

from pathlib import Path
from typing import Any, Dict, List


def get_linux_specific_config(base_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    获取 Linux 特定配置

    参数:
        base_config: 基础配置字典

    返回:
        Dict[str, Any]: 更新后的配置
    """
    config = base_config.copy()

    # Linux 特定隐藏导入
    config.setdefault("hidden_imports", []).extend(
        [
            "dbus",  # D-Bus 系统总线
            "gi",  # GObject Introspection
            "xdg",  # XDG 桌面规范
        ]
    )

    # Linux 特定排除模块
    config.setdefault("excludes", []).extend(
        [
            "PySide6.QtWebEngine",
            "PySide6.QtWebEngineCore",
            "PySide6.QtWebEngineWidgets",
            "PySide6.QtQuick3D",
        ]
    )

    # Linux 桌面集成
    config["desktop_integration"] = {
        "desktop_file": config.get("desktop_file", ""),
        "icon_theme": "hicolor",  # 标准图标主题
        "mime_types": [],  # 关联的 MIME 类型
        "categories": ["Utility", "Graphics"],  # 应用分类
    }

    # Linux 库依赖
    config["library_dependencies"] = [
        "libxcb",  # X11 客户端库
        "libxcb-icccm",
        "libxcb-image",
        "libxcb-keysyms",
        "libxcb-randr",
        "libxcb-render",
        "libxcb-render-util",
        "libxcb-shape",
        "libxcb-shm",
        "libxcb-sync",
        "libxcb-xfixes",
        "libxcb-xinerama",
        "libxcb-xkb",
        "libxcb-xv",
        "libGL",  # OpenGL
        "libfontconfig",
        "libfreetype",
        "libssl",  # SSL 支持
        "libcrypto",
    ]

    # Linux 特定 UPX 排除
    config.setdefault("upx_exclude", []).extend(
        [
            "libQt6Core.so",
            "libQt6Gui.so",
            "libQt6Widgets.so",
        ]
    )

    # Linux 二进制优化
    config["binary_optimization"] = True

    return config


def get_linux_pyinstaller_args(config: Dict[str, Any]) -> List[str]:
    """
    获取 Linux 特定 PyInstaller 参数

    参数:
        config: 平台配置

    返回:
        List[str]: 附加参数列表
    """
    args = []

    # Linux 控制台设置
    if not config.get("console", True):
        args.append("--windowed")

    # 图标文件
    if config.get("icon") and Path(config["icon"]).exists():
        args.extend(["--icon", config["icon"]])

    # 桌面文件（用于创建 .desktop 入口）
    if config.get("desktop_file") and Path(config["desktop_file"]).exists():
        args.extend(["--add-data", f"{config['desktop_file']}:."])

    # Linux 应用名称
    args.extend(["--name", config.get("name", "ddnet-change-color")])

    # Linux 特定优化
    args.append("--strip")  # 去除调试符号

    return args


def validate_linux_environment() -> bool:
    """
    验证 Linux 构建环境

    返回:
        bool: 环境是否有效
    """
    import subprocess
    import sys

    if not sys.platform.startswith("linux"):
        print("警告: 当前不是 Linux 系统")
        return False

    # 检查 Linux 发行版
    try:
        with open("/etc/os-release", "r") as f:
            os_release = f.read()
        for line in os_release.split("\n"):
            if line.startswith("PRETTY_NAME="):
                distro = line.split("=")[1].strip('"')
                print(f"Linux 发行版: {distro}")
                break
    except FileNotFoundError:
        print("无法确定 Linux 发行版")

    # 检查必要工具
    try:
        import PySide6

        print(f"PySide6 版本: {PySide6.__version__}")
    except ImportError:
        print("错误: PySide6 未安装")
        return False

    # 检查系统库依赖
    missing_libs = []
    libs_to_check = ["libxcb", "libGL", "libfontconfig", "libfreetype", "libssl", "libcrypto"]

    for lib in libs_to_check:
        try:
            result = subprocess.run(["ldconfig", "-p"], capture_output=True, text=True)
            if lib not in result.stdout:
                missing_libs.append(lib)
        except FileNotFoundError:
            # 使用 alternative check
            pass

    if missing_libs:
        print(f"警告: 以下系统库可能缺失: {', '.join(missing_libs)}")
        print(
            "建议安装: sudo apt-get install libxcb-* libgl1-mesa-dev"
            " libfontconfig1 libfreetype6 libssl-dev"
        )

    # 检查 UPX（可选）
    import shutil

    if shutil.which("upx"):
        print("UPX 已安装")
    else:
        print("UPX 未安装，二进制文件将不会被压缩")

    return True
