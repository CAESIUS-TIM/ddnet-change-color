# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent
src_dir = project_root / "src"

# 添加源代码路径
sys.path.insert(0, str(src_dir))

# 导入构建配置
try:
    from build.config import BUILD_CONFIG, PLATFORM_CONFIG
    from build.utils import collect_qt_plugins, collect_translations
except ImportError:
    # 回退到简单配置
    BUILD_CONFIG = {
        "hidden_imports": [
            "PySide6",
            "PySide6.QtCore",
            "PySide6.QtGui",
            "PySide6.QtWidgets",
        ],
        "excludes": [],
    }
    PLATFORM_CONFIG = {}
    
    def collect_qt_plugins():
        return []
    
    def collect_translations():
        return []


# 获取平台
platform = sys.platform
if platform.startswith("win"):
    platform_key = "windows"
elif platform.startswith("darwin"):
    platform_key = "darwin"
elif platform.startswith("linux"):
    platform_key = "linux"
else:
    platform_key = platform

# 平台配置
platform_config = PLATFORM_CONFIG.get(platform_key, {})

# 版本信息
try:
    import tomllib
    with open(project_root / "pyproject.toml", "rb") as f:
        pyproject = tomllib.load(f)
    version = pyproject.get("project", {}).get("version", "1.0.0")
except:
    version = "1.0.0"

block_cipher = None

# 收集数据文件
datas = []

# Qt 插件
for src, dst in collect_qt_plugins():
    datas.append((src, dst))

# Qt 翻译文件
for src, dst in collect_translations():
    datas.append((src, dst))

# 平台特定图标
if "icon" in platform_config:
    icon_path = Path(platform_config["icon"])
    if icon_path.exists():
        datas.append((str(icon_path), icon_path.name))

# 分析的主脚本
main_script = str(src_dir / "ddnet_change_color" / "__main__.py")

# 隐藏导入
hiddenimports = BUILD_CONFIG.get("hidden_imports", [])

# 排除模块
excludes = BUILD_CONFIG.get("excludes", [])

# 添加平台特定隐藏导入
if platform_key in PLATFORM_CONFIG:
    platform_hidden = PLATFORM_CONFIG[platform_key].get("hidden_imports", [])
    hiddenimports.extend(platform_hidden)
    
    platform_excludes = PLATFORM_CONFIG[platform_key].get("excludes", [])
    excludes.extend(platform_excludes)

# 二进制分析配置
a = Analysis(
    [main_script],
    pathex=[str(src_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PySide6 特定钩子
pyqt_hooks = []

# 收集必要的 DLL/共享库
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 可执行文件配置
exe_name = platform_config.get("name", "ddnet-change-color")
if platform_key == "windows":
    exe_name += ".exe"

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=platform_config.get("console", platform_key != "windows"),
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=platform_config.get("icon") if Path(platform_config.get("icon", "")).exists() else None,
)

# Windows 特定配置
if platform_key == "windows":
    version_file = platform_config.get("version_file")
    if version_file and Path(version_file).exists():
        exe.version = version_file

# macOS 特定配置  
if platform_key == "darwin":
    info_plist = platform_config.get("info_plist")
    if info_plist and Path(info_plist).exists():
        exe.info_plist = info_plist
    
    # macOS 应用包
    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=platform_config.get("name", "DDNet Change Color"),
        icon=platform_config.get("icon") if Path(platform_config.get("icon", "")).exists() else None,
    )
else:
    # 单文件模式或目录模式
    coll = exe