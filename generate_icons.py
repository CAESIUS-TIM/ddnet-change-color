#!/usr/bin/env python3
"""
图标生成工具

此脚本从 SVG 文件生成多平台图标。
需要安装 Pillow 库：uv add --group build pillow

使用方法：
    python generate_icons.py

注意：
- 对于 Windows .ico 文件，需要安装额外的工具（如 ImageMagick 或 GIMP）
- 对于 macOS .icns 文件，需要在 macOS 系统上使用 iconutil 工具
- 生成的 PNG 文件可用于手动转换
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("错误：需要安装 Pillow 库")
    print("请运行: uv add --group build pillow")
    sys.exit(1)


def create_simple_icon(size: int = 256) -> Image.Image:
    """创建简单的占位图标"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 背景：DDNet 蓝渐变
    for i in range(size):
        # 简单的渐变效果
        r = int(45 * (1 - i/size) + 26 * (i/size))  # #2D7DD2 到 #1A5CA6
        g = int(125 * (1 - i/size) + 92 * (i/size))
        b = int(210 * (1 - i/size) + 166 * (i/size))
        draw.line([(0, i), (size, i)], fill=(r, g, b, 255))

    # 调色盘
    palette_center = (size // 2, int(size * 0.55))
    palette_radius = int(size * 0.27)
    draw.ellipse(
        [
            palette_center[0] - palette_radius,
            palette_center[1] - int(palette_radius * 0.86),
            palette_center[0] + palette_radius,
            palette_center[1] + int(palette_radius * 0.86)
        ],
        fill=(255, 255, 255, 230),
        outline=(255, 255, 255, 180),
        width=2
    )

    # 颜色点
    colors = [
        (255, 153, 0, 255),    # 橙色 #FF9900
        (45, 125, 210, 255),   # DDNet 蓝 #2D7DD2
        (102, 204, 255, 255),  # 浅蓝 #66CCFF
    ]

    for i, color in enumerate(colors):
        x = palette_center[0] - palette_radius // 2 + i * palette_radius // 2
        y = palette_center[1] - palette_radius // 4
        radius = int(size * 0.07)
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=color,
            outline=(255, 255, 255, 200),
            width=2
        )

    # DCC 文字
    try:
        font = ImageFont.truetype("Arial", size // 10)
    except OSError:
        font = ImageFont.load_default()

    text = "DCC"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = size // 2 - text_width // 2
    text_y = int(size * 0.78) - text_height // 2

    draw.text(
        (text_x, text_y),
        text,
        fill=(255, 255, 255, 220),
        font=font,
        stroke_width=1,
        stroke_fill=(0, 0, 0, 80)
    )

    # 外边框
    draw.ellipse(
        [4, 4, size - 4, size - 4],
        fill=None,
        outline=(255, 255, 255, 100),
        width=4
    )

    return img


def generate_png_icons():
    """生成 PNG 格式图标"""
    sizes = [16, 32, 48, 64, 128, 256, 512]

    # 创建 linux 目录
    linux_dir = Path("assets/linux")
    linux_dir.mkdir(parents=True, exist_ok=True)

    print("生成 PNG 图标...")
    for size in sizes:
        img = create_simple_icon(size)
        filename = linux_dir / f"icon_{size}x{size}.png"
        img.save(filename, "PNG")
        print(f"  ✓ 生成 {filename}")

    # 主图标文件（256x256）
    main_icon = create_simple_icon(256)
    main_icon.save(linux_dir / "icon.png", "PNG")
    print(f"  ✓ 生成 {linux_dir / 'icon.png'}")


def create_placeholder_files():
    """创建占位符图标文件（用于 CI/CD）"""
    assets_dir = Path("assets")

    # Windows .ico 占位符
    windows_dir = assets_dir / "windows"
    windows_dir.mkdir(parents=True, exist_ok=True)

    ico_placeholder = windows_dir / "icon.ico"
    with open(ico_placeholder, "wb") as f:
        # 简单的 ICO 文件头（无效但占位）
        f.write(b'ICO_PLACEHOLDER - Replace with actual .ico file\n')
        f.write(b'To create proper .ico file:\n')
        f.write(b'1. Use ImageMagick: convert icon_*.png icon.ico\n')
        f.write(b'2. Or use online converter\n')

    print(f"  ⚠  创建占位符 {ico_placeholder}")
    print("     提示：需要手动转换为有效的 .ico 文件")

    # macOS .icns 占位符
    macos_dir = assets_dir / "macos"
    macos_dir.mkdir(parents=True, exist_ok=True)

    icns_placeholder = macos_dir / "icon.icns"
    with open(icns_placeholder, "wb") as f:
        f.write(b'ICNS_PLACEHOLDER - Replace with actual .icns file\n')
        f.write(b'To create proper .icns file on macOS:\n')
        f.write(b'1. Create .iconset directory with PNG files\n')
        f.write(b'2. Run: iconutil -c icns icon.iconset\n')

    print(f"  ⚠  创建占位符 {icns_placeholder}")
    print("     提示：需要在 macOS 上创建 .icns 文件")


def main():
    """主函数"""
    print("DDNet 换色工具 - 图标生成器")
    print("=" * 50)

    # 检查 assets 目录
    assets_dir = Path("assets")
    if not assets_dir.exists():
        assets_dir.mkdir(parents=True)

    # 生成 PNG 图标
    generate_png_icons()

    # 创建占位符文件
    create_placeholder_files()

    print("\n" + "=" * 50)
    print("图标生成完成！")
    print("\n下一步：")
    print("1. 对于 Windows：将 PNG 图标转换为 .ico 格式")
    print("2. 对于 macOS：在 macOS 系统上创建 .icns 文件")
    print("3. 或者使用在线图标转换工具")
    print("\n提示：占位符文件可用于 CI/CD 测试，但最终发布需要真实图标")


if __name__ == "__main__":
    main()
