"""
构建工具函数
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple
from .config import PROJECT_ROOT


def collect_qt_plugins() -> List[Tuple[str, str]]:
    """
    收集 PySide6 Qt 插件
    
    返回:
        List[Tuple[str, str]]: (源路径, 目标路径) 列表
    """
    try:
        from PySide6 import QtCore
        
        qt_plugin_path = Path(QtCore.__file__).parent / "plugins"
        if not qt_plugin_path.exists():
            print(f"警告: Qt 插件目录不存在: {qt_plugin_path}")
            return []
        
        plugins = []
        # 必需插件
        required_plugins = [
            "platforms",      # 平台插件 (windows, cocoa, xcb)
            "styles",         # 界面样式
            "iconengines",    # 图标引擎
            "imageformats",   # 图片格式支持
        ]
        
        for plugin in required_plugins:
            plugin_dir = qt_plugin_path / plugin
            if plugin_dir.exists():
                plugins.append((
                    str(plugin_dir),
                    f"PySide6/Qt/plugins/{plugin}"
                ))
                print(f"收集 Qt 插件: {plugin} -> PySide6/Qt/plugins/{plugin}")
            else:
                print(f"警告: Qt 插件目录不存在: {plugin_dir}")
        
        return plugins
        
    except ImportError as e:
        print(f"错误: 无法导入 PySide6: {e}")
        return []


def collect_translations() -> List[Tuple[str, str]]:
    """
    收集 Qt 翻译文件
    
    返回:
        List[Tuple[str, str]]: (源路径, 目标路径) 列表
    """
    try:
        from PySide6 import QtCore
        
        qt_translations_path = Path(QtCore.__file__).parent / "translations"
        if not qt_translations_path.exists():
            return []
        
        translations = []
        for file in qt_translations_path.glob("*.qm"):
            translations.append((
                str(file),
                f"PySide6/Qt/translations/{file.name}"
            ))
        
        return translations
        
    except ImportError:
        return []


def get_platform_config():
    """
    获取当前平台的配置
    
    返回:
        dict: 平台配置字典
    """
    platform = sys.platform
    if platform.startswith("win"):
        return "windows"
    elif platform.startswith("darwin"):
        return "darwin"
    elif platform.startswith("linux"):
        return "linux"
    else:
        raise RuntimeError(f"不支持的操作系统: {platform}")


def validate_assets():
    """
    验证资源文件是否存在
    
    返回:
        bool: 所有必需资源文件是否存在
    """
    from .config import ASSETS_DIR, PLATFORM_CONFIG
    
    platform = get_platform_config()
    config = PLATFORM_CONFIG[platform]
    
    missing_files = []
    
    # 检查图标文件
    if "icon" in config:
        icon_path = Path(config["icon"])
        if not icon_path.exists():
            missing_files.append(str(icon_path))
            print(f"警告: 图标文件不存在: {icon_path}")
            print(f"      使用 generate_icons.py 生成图标")
    
    # 检查 Windows 版本文件
    if platform == "windows" and "version_file" in config:
        version_file = Path(config["version_file"])
        if not version_file.exists():
            missing_files.append(str(version_file))
    
    # 检查 macOS Info.plist 模板
    if platform == "darwin" and "info_plist" in config:
        info_plist = Path(config["info_plist"])
        if not info_plist.exists():
            missing_files.append(str(info_plist))
    
    if missing_files:
        print(f"缺失 {len(missing_files)} 个资源文件")
        return False
    
    return True


def get_pyinstaller_args(config: dict, onefile: bool = True) -> List[str]:
    """
    生成 PyInstaller 参数列表
    
    参数:
        config: 平台配置
        onefile: 是否使用单文件模式
    
    返回:
        List[str]: PyInstaller 参数列表
    """
    args = [
        "--clean",
        "--noconfirm",
    ]
    
    if onefile:
        args.append("--onefile")
    
    # 平台特定参数
    platform = get_platform_config()
    
    if platform == "windows":
        args.append("--windowed")  # 隐藏控制台
        
        if "icon" in config and Path(config["icon"]).exists():
            args.extend(["--icon", config["icon"]])
        
        if "version_file" in config and Path(config["version_file"]).exists():
            args.extend(["--version-file", config["version_file"]])
    
    elif platform == "darwin":
        args.append("--windowed")
        args.extend(["--name", config["name"]])
        
        if "icon" in config and Path(config["icon"]).exists():
            args.extend(["--icon", config["icon"]])
        
        if "info_plist" in config and Path(config["info_plist"]).exists():
            args.extend(["--info-plist", config["info_plist"]])
    
    elif platform == "linux":
        # Linux 通常显示控制台
        if not config.get("console", True):
            args.append("--windowed")
    
    # 添加 UPX 压缩
    from .config import BUILD_CONFIG
    if BUILD_CONFIG.get("upx", True):
        args.append("--upx-exclude=vcruntime140.dll")
    
    return args


def get_version() -> str:
    """
    从 pyproject.toml 读取版本号
    
    返回:
        str: 版本号字符串
    """
    import tomllib
    
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if not pyproject_path.exists():
        raise FileNotFoundError(f"pyproject.toml 不存在: {pyproject_path}")
    
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    
    version = data.get("project", {}).get("version")
    if not version:
        raise ValueError("在 pyproject.toml 中未找到版本号")
    
    return version


def collect_data_files() -> List[Tuple[str, str]]:
    """
    收集所有数据文件（图标、翻译、Qt插件等）
    
    返回:
        List[Tuple[str, str]]: (源路径, 目标路径) 列表
    """
    data_files = []
    
    # 收集 Qt 插件
    data_files.extend(collect_qt_plugins())
    
    # 收集翻译文件
    data_files.extend(collect_translations())
    
    # 收集平台特定图标
    platform = get_platform_config()
    from .config import PLATFORM_CONFIG
    
    config = PLATFORM_CONFIG[platform]
    if "icon" in config:
        icon_path = Path(config["icon"])
        if icon_path.exists():
            # 图标文件复制到应用根目录
            data_files.append((
                str(icon_path),
                icon_path.name
            ))
    
    return data_files


def prepare_build_dir(build_dir: Path) -> None:
    """
    准备构建目录，清理旧文件
    
    参数:
        build_dir: 构建目录路径
    """
    import shutil
    
    if build_dir.exists():
        print(f"清理构建目录: {build_dir}")
        shutil.rmtree(build_dir)
    
    build_dir.mkdir(parents=True, exist_ok=True)
    print(f"创建构建目录: {build_dir}")


def run_pyinstaller(args: List[str], spec_file: str = None) -> bool:
    """
    运行 PyInstaller 命令
    
    参数:
        args: PyInstaller 参数列表
        spec_file: 可选的 spec 文件路径
    
    返回:
        bool: 是否成功
    """
    import subprocess
    
    cmd = ["pyinstaller"]
    if spec_file:
        cmd.append(spec_file)
    cmd.extend(args)
    
    print(f"运行 PyInstaller: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"警告: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller 失败: {e}")
        print(f"标准输出: {e.stdout}")
        print(f"标准错误: {e.stderr}")
        return False
    except FileNotFoundError:
        print("错误: 未找到 pyinstaller 命令")
        print("请安装 PyInstaller: uv add --group build pyinstaller")
        return False