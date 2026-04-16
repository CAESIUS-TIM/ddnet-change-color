"""
主构建器模块
"""

import sys
from pathlib import Path
from typing import Dict, Optional

from .config import (
    BUILD_CONFIG,
    PLATFORM_CONFIG,
    PROJECT_ROOT,
)
from .utils import (
    collect_data_files,
    get_platform_config,
    get_pyinstaller_args,
    get_version,
    prepare_build_dir,
    run_pyinstaller,
    validate_assets,
)


class Builder:
    """
    应用构建器
    """

    def __init__(self, platform: Optional[str] = None, onefile: bool = True):
        """
        初始化构建器

        参数:
            platform: 目标平台 (windows, darwin, linux)
            onefile: 是否生成单文件
        """
        self.platform = platform or get_platform_config()
        self.onefile = onefile

        if self.platform not in PLATFORM_CONFIG:
            raise ValueError(f"不支持的平台: {self.platform}")

        self.config = PLATFORM_CONFIG[self.platform].copy()
        self.build_config = BUILD_CONFIG.copy()

        # 加载平台特定配置
        self._load_platform_specific_config()

        # 设置版本
        self.version = get_version()
        self.config["version"] = self.version

        print("构建配置:")
        print(f"  平台: {self.config.get('platform_name', self.platform)}")
        print(f"  版本: {self.version}")
        print(f"  模式: {'单文件' if onefile else '目录'}")

    def _load_platform_specific_config(self):
        """加载平台特定配置"""
        if self.platform == "windows":
            from .platforms.windows import get_windows_specific_config

            self.config = get_windows_specific_config(self.config)

        elif self.platform == "darwin":
            from .platforms.macos import get_macos_specific_config

            self.config = get_macos_specific_config(self.config)

        elif self.platform == "linux":
            from .platforms.linux import get_linux_specific_config

            self.config = get_linux_specific_config(self.config)

    def validate_environment(self) -> bool:
        """
        验证构建环境

        返回:
            bool: 环境是否有效
        """
        print("验证构建环境...")

        # 验证平台特定环境
        if self.platform == "windows":
            from .platforms.windows import validate_windows_environment

            if not validate_windows_environment():
                return False

        elif self.platform == "darwin":
            from .platforms.macos import validate_macos_environment

            if not validate_macos_environment():
                return False

        elif self.platform == "linux":
            from .platforms.linux import validate_linux_environment

            if not validate_linux_environment():
                return False

        # 验证资源文件
        if not validate_assets():
            print("警告: 资源文件验证失败，构建可能无法包含图标等资源")

        # 验证构建工具
        try:
            import PyInstaller

            print(f"PyInstaller 版本: {PyInstaller.__version__}")
        except ImportError:
            print("错误: PyInstaller 未安装")
            print("请安装: uv add --group build pyinstaller")
            return False

        # 验证 UPX（可选）
        import shutil

        if self.build_config.get("upx", True) and not shutil.which("upx"):
            print("警告: UPX 未安装，二进制文件将不会被压缩")
            print("安装 UPX: https://upx.github.io/")

        print("环境验证通过")
        return True

    def prepare_build(self) -> bool:
        """
        准备构建

        返回:
            bool: 是否成功
        """
        print("准备构建...")

        # 创建构建目录
        build_dir = Path(self.build_config["build_dir"])
        prepare_build_dir(build_dir)

        # 创建输出目录
        dist_dir = Path(self.build_config["dist_dir"])
        dist_dir.mkdir(parents=True, exist_ok=True)
        print(f"输出目录: {dist_dir}")

        # 准备平台特定文件
        self._prepare_platform_files()

        return True

    def _prepare_platform_files(self):
        """准备平台特定文件"""
        if self.platform == "windows":
            # 确保版本信息文件存在
            version_file = Path(self.config.get("version_file", ""))
            if version_file.exists():
                # 更新版本信息文件中的版本号
                self._update_version_file(version_file)

        elif self.platform == "darwin":
            # 确保 Info.plist 存在
            info_plist = Path(self.config.get("info_plist", ""))
            if info_plist.exists():
                # 更新 Info.plist 中的版本号
                self._update_info_plist(info_plist)

        elif self.platform == "linux":
            # 确保 .desktop 文件存在
            desktop_file = Path(self.config.get("desktop_file", ""))
            if desktop_file.exists():
                # 更新 .desktop 文件中的版本号
                self._update_desktop_file(desktop_file)

    def _update_version_file(self, version_file: Path):
        """更新 Windows 版本信息文件"""
        try:
            content = version_file.read_text(encoding="utf-8")
            # 替换版本号
            import re

            content = re.sub(
                r"FILEVERSION\s+\d+,\d+,\d+,\d+",
                f"FILEVERSION {self.version.replace('.', ',')},0",
                content,
            )
            content = re.sub(
                r"PRODUCTVERSION\s+\d+,\d+,\d+,\d+",
                f"PRODUCTVERSION {self.version.replace('.', ',')},0",
                content,
            )
            content = re.sub(
                r'VALUE "FileVersion", "[^"]*"', f'VALUE "FileVersion", "{self.version}"', content
            )
            content = re.sub(
                r'VALUE "ProductVersion", "[^"]*"',
                f'VALUE "ProductVersion", "{self.version}"',
                content,
            )
            version_file.write_text(content, encoding="utf-8")
            print(f"更新版本信息文件: {version_file}")
        except Exception as e:
            print(f"更新版本信息文件失败: {e}")

    def _update_info_plist(self, info_plist: Path):
        """更新 macOS Info.plist 文件"""
        try:
            content = info_plist.read_text(encoding="utf-8")
            # 替换版本号
            import re

            content = re.sub(
                r"<key>CFBundleShortVersionString</key>\s*<string>[^<]*</string>",
                f"<key>CFBundleShortVersionString</key>\n    <string>{self.version}</string>",
                content,
            )
            content = re.sub(
                r"<key>CFBundleVersion</key>\s*<string>[^<]*</string>",
                f"<key>CFBundleVersion</key>\n    <string>{self.version}</string>",
                content,
            )
            info_plist.write_text(content, encoding="utf-8")
            print(f"更新 Info.plist 文件: {info_plist}")
        except Exception as e:
            print(f"更新 Info.plist 文件失败: {e}")

    def _update_desktop_file(self, desktop_file: Path):
        """更新 Linux .desktop 文件"""
        try:
            content = desktop_file.read_text(encoding="utf-8")
            # 替换版本号（如果存在 Version 字段）
            import re

            if "Version=" in content:
                content = re.sub(r"Version=.*", f"Version={self.version}", content)
            desktop_file.write_text(content, encoding="utf-8")
            print(f"更新 .desktop 文件: {desktop_file}")
        except Exception as e:
            print(f"更新 .desktop 文件失败: {e}")

    def build(self) -> bool:
        """
        执行构建

        返回:
            bool: 是否成功
        """
        print("开始构建...")

        # 验证环境
        if not self.validate_environment():
            return False

        # 准备构建
        if not self.prepare_build():
            return False

        # 检查是否使用 spec 文件
        spec_file = self.build_config.get("spec_file")
        use_spec = Path(spec_file).exists()

        # 生成 PyInstaller 参数
        args = self._generate_pyinstaller_args(include_main_script=not use_spec)

        # 运行 PyInstaller
        if use_spec:
            print(f"使用 spec 文件: {spec_file}")
            success = run_pyinstaller(args, spec_file)
        else:
            success = run_pyinstaller(args)

        if success:
            print("构建成功!")
            self._post_build()
        else:
            print("构建失败!")

        return success

    def _generate_pyinstaller_args(self, include_main_script: bool = True) -> list:
        """生成 PyInstaller 参数

        参数:
            include_main_script: 是否包含主脚本 (当使用 spec 文件时应为 False)
        """
        args = get_pyinstaller_args(self.config, self.onefile)

        # 主脚本 (仅当不使用 spec 文件时添加)
        if include_main_script:
            args.append(self.build_config["main_script"])

        # 工作目录
        args.extend(["--workpath", self.build_config["build_dir"]])
        args.extend(["--distpath", self.build_config["dist_dir"]])
        args.extend(["--specpath", str(PROJECT_ROOT)])

        # 隐藏导入
        for imp in self.build_config.get("hidden_imports", []):
            args.extend(["--hidden-import", imp])

        # 平台特定隐藏导入
        for imp in self.config.get("hidden_imports", []):
            args.extend(["--hidden-import", imp])

        # 排除模块
        for exc in self.build_config.get("excludes", []):
            args.extend(["--exclude-module", exc])

        # 平台特定排除模块
        for exc in self.config.get("excludes", []):
            args.extend(["--exclude-module", exc])

        # 添加数据文件
        data_files = collect_data_files()
        for src, dst in data_files:
            args.extend(["--add-data", f"{src}:{dst}"])

        # 添加源代码路径
        for path in self.build_config.get("pathex", []):
            args.extend(["--paths", path])

        # UPX 配置
        if self.build_config.get("upx", True):
            args.append("--upx-dir")
            args.append(str(PROJECT_ROOT / "tools" / "upx"))  # 假设 UPX 在此目录

        # UPX 排除列表
        for exclude in self.config.get("upx_exclude", []):
            args.append(f"--upx-exclude={exclude}")

        return args

    def _post_build(self):
        """构建后处理"""
        print("构建后处理...")

        dist_dir = Path(self.build_config["dist_dir"])

        if self.onefile:
            # 查找生成的可执行文件
            output_name = self.config["name"]
            if self.platform == "windows":
                output_name += ".exe"

            executable = dist_dir / output_name
            if executable.exists():
                print(f"生成的可执行文件: {executable}")

                # 计算文件大小
                size_mb = executable.stat().st_size / (1024 * 1024)
                print(f"文件大小: {size_mb:.2f} MB")

                # 重命名文件以包含平台和版本信息
                artifact_name = self.config.get("artifact_name", "ddnet-change-color")
                new_name = f"{artifact_name}-{self.version}"
                if self.platform == "windows":
                    new_name += ".exe"

                new_path = dist_dir / new_name
                executable.rename(new_path)
                print(f"重命名为: {new_path}")
            else:
                print("警告: 未找到生成的可执行文件")
        else:
            print(f"生成的应用目录: {dist_dir / self.config['name']}")

        # 平台特定后处理
        if self.platform == "linux" and self.config.get("desktop_file"):
            self._create_linux_desktop_entry(dist_dir)

    def _create_linux_desktop_entry(self, dist_dir: Path):
        """创建 Linux 桌面入口"""
        desktop_src = Path(self.config["desktop_file"])
        if not desktop_src.exists():
            return

        # 复制 .desktop 文件到应用目录
        desktop_dst = dist_dir / f"{self.config['name']}.desktop"
        import shutil

        shutil.copy2(desktop_src, desktop_dst)

        # 更新 .desktop 文件中的路径
        content = desktop_dst.read_text(encoding="utf-8")

        # 替换 Exec 路径
        exec_path = f"{dist_dir / self.config['name']}/{self.config['name']}"
        content = content.replace("Exec=ddnet-change-color", f"Exec={exec_path}")

        # 替换 Icon 路径
        icon_path = dist_dir / self.config["name"] / Path(self.config["icon"]).name
        content = content.replace("Icon=ddnet-change-color", f"Icon={icon_path}")

        desktop_dst.write_text(content, encoding="utf-8")
        print(f"创建桌面入口: {desktop_dst}")


def build_for_platform(platform: str, onefile: bool = True) -> bool:
    """
    为指定平台构建

    参数:
        platform: 目标平台
        onefile: 是否生成单文件

    返回:
        bool: 是否成功
    """
    try:
        builder = Builder(platform, onefile)
        return builder.build()
    except Exception as e:
        print(f"构建失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def build_all_platforms(onefile: bool = True) -> Dict[str, bool]:
    """
    为所有平台构建

    参数:
        onefile: 是否生成单文件

    返回:
        Dict[str, bool]: 各平台构建结果
    """
    results = {}

    for platform in PLATFORM_CONFIG.keys():
        print(f"\n{'=' * 60}")
        print(f"构建平台: {platform}")
        print(f"{'=' * 60}")

        # 设置平台环境变量（模拟跨平台构建）
        original_platform = sys.platform
        sys.platform = platform

        try:
            results[platform] = build_for_platform(platform, onefile)
        finally:
            # 恢复原始平台
            sys.platform = original_platform

    return results
