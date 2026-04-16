#!/usr/bin/env python3
"""
DDNet Change Color 构建脚本

使用:
    python build_script.py [选项]

示例:
    python build_script.py                  # 为当前平台构建
    python build_script.py --platform windows  # 为 Windows 构建
    python build_script.py --all           # 为所有平台构建
    python build_script.py --help          # 显示帮助
"""

import argparse
import sys
import os
from pathlib import Path

# 添加 build 模块到路径
script_dir = str(Path(__file__).parent)
sys.path.insert(0, script_dir)
print(f"DEBUG: Script directory: {script_dir}", file=sys.stderr)
print(f"DEBUG: Current working directory: {os.getcwd()}", file=sys.stderr)
print(f"DEBUG: sys.path: {sys.path}", file=sys.stderr)
print(
    f"DEBUG: Checking if build directory exists: {os.path.isdir(os.path.join(script_dir, 'build'))}",
    file=sys.stderr,
)

from build.builder import build_all_platforms, build_for_platform
from build.config import PLATFORM_CONFIG


def main():
    parser = argparse.ArgumentParser(
        description="DDNet Change Color 应用构建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
平台支持:
  windows    Windows 平台 (.exe)
  darwin     macOS 平台 (.app)
  linux      Linux 平台 (可执行文件)

环境要求:
  1. 安装构建依赖: uv add --group build
  2. 安装 UPX (可选): https://upx.github.io/
  3. 平台特定构建工具 (如 Windows: Visual C++, macOS: Xcode)

示例:
  %(prog)s                         # 为当前平台构建单文件
  %(prog)s --platform windows      # 为 Windows 构建
  %(prog)s --platform linux        # 为 Linux 构建
  %(prog)s --all                   # 为所有平台构建
  %(prog)s --no-onefile            # 构建目录模式 (开发)
  %(prog)s --clean                 # 清理构建目录
  %(prog)s --validate              # 只验证环境
        """,
    )

    parser.add_argument(
        "--platform",
        choices=list(PLATFORM_CONFIG.keys()),
        help="目标平台 (默认: 当前平台)",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="为所有平台构建",
    )

    parser.add_argument(
        "--no-onefile",
        action="store_true",
        help="使用目录模式 (默认: 单文件模式)",
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="清理构建目录",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="只验证构建环境",
    )

    parser.add_argument(
        "--spec",
        action="store_true",
        help="使用 spec 文件构建",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="详细输出 (-v, -vv)",
    )

    args = parser.parse_args()

    # 设置日志级别
    if args.verbose >= 2:
        import logging

        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose >= 1:
        import logging

        logging.basicConfig(level=logging.INFO)

    # 清理构建目录
    if args.clean:
        import shutil

        from build.config import BUILD_CONFIG

        build_dir = Path(BUILD_CONFIG["build_dir"])
        dist_dir = Path(BUILD_CONFIG["dist_dir"])

        print("清理构建目录...")
        if build_dir.exists():
            shutil.rmtree(build_dir)
            print(f"删除: {build_dir}")

        if dist_dir.exists():
            shutil.rmtree(dist_dir)
            print(f"删除: {dist_dir}")

        print("清理完成")
        return 0

    # 验证模式
    if args.validate:
        from build.builder import Builder

        platform = args.platform
        if not platform:
            import sys

            if sys.platform.startswith("win"):
                platform = "windows"
            elif sys.platform.startswith("darwin"):
                platform = "darwin"
            elif sys.platform.startswith("linux"):
                platform = "linux"
            else:
                print(f"未知平台: {sys.platform}")
                return 1

        try:
            builder = Builder(platform, not args.no_onefile)
            if builder.validate_environment():
                print("✓ 环境验证通过")
                return 0
            else:
                print("✗ 环境验证失败")
                return 1
        except Exception as e:
            print(f"验证错误: {e}")
            return 1

    # 构建模式
    try:
        if args.all:
            print("为所有平台构建...")
            results = build_all_platforms(not args.no_onefile)

            print("\n构建结果:")
            success_count = 0
            for platform, success in results.items():
                status = "✓ 成功" if success else "✗ 失败"
                print(f"  {platform}: {status}")
                if success:
                    success_count += 1

            if success_count == len(results):
                print("\n所有平台构建成功!")
                return 0
            else:
                print(f"\n{success_count}/{len(results)} 个平台构建成功")
                return 1

        else:
            # 单个平台构建
            onefile = not args.no_onefile
            platform = args.platform

            print(
                f"开始构建 (平台: {platform or '当前'}, 模式: {'单文件' if onefile else '目录'})..."
            )

            success = build_for_platform(platform, onefile)

            if success:
                print("构建成功!")
                return 0
            else:
                print("构建失败!")
                return 1

    except KeyboardInterrupt:
        print("\n构建被用户中断")
        return 130
    except Exception as e:
        print(f"构建错误: {e}")
        import traceback

        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
