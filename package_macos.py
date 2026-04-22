#!/usr/bin/env python3
"""
macOS 应用打包工具

此脚本将 PyInstaller 生成的可执行文件转换为 .app 目录结构。
"""

import os
import shutil
import sys
from pathlib import Path


def create_app_bundle(exe_path: str, version: str, output_dir: str = ".") -> str:
    """创建 macOS .app 目录结构

    参数:
        exe_path: 可执行文件路径
        version: 版本号
        output_dir: 输出目录

    返回:
        生成的 ZIP 文件路径
    """
    exe_name = Path(exe_path).name

    # .app 目录名称（不含 .app 后缀）
    app_name = "DDNet Change Color"
    app_bundle = f"{app_name}.app"

    # 创建目录结构
    app_contents = os.path.join(output_dir, app_bundle, "Contents", "MacOS")
    os.makedirs(app_contents, exist_ok=True)

    # 复制可执行文件
    dst_exe = os.path.join(app_contents, exe_name)
    shutil.copy2(exe_path, dst_exe)
    os.chmod(dst_exe, 0o755)

    # 创建 Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{exe_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.ddnet.change-color</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>{version}</string>
    <key>CFBundleVersion</key>
    <string>{version}</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""

    info_plist_path = os.path.join(output_dir, app_bundle, "Contents", "Info.plist")
    with open(info_plist_path, "w", encoding="utf-8") as f:
        f.write(info_plist)

    # 创建 ZIP 文件
    zip_name = f"ddnet-change-color-macos-{version}.zip"
    zip_path = os.path.join(output_dir, zip_name)

    # 使用 zip 命令
    os.system(f'cd "{output_dir}" && zip -r "{zip_name}" "{app_bundle}"')

    return zip_path


def main():
    if len(sys.argv) < 3:
        print("用法: python package_macos.py <可执行文件路径> <版本号> [输出目录]")
        sys.exit(1)

    exe_path = sys.argv[1]
    version = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "."

    if not os.path.exists(exe_path):
        print(f"错误: 找不到可执行文件 {exe_path}")
        sys.exit(1)

    print(f"创建 macOS 应用包...")
    print(f"  可执行文件: {exe_path}")
    print(f"  版本: {version}")
    print(f"  输出目录: {output_dir}")

    zip_path = create_app_bundle(exe_path, version, output_dir)
    print(f"完成: {zip_path}")


if __name__ == "__main__":
    main()
