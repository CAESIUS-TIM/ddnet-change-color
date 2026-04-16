import sys

from PySide6.QtWidgets import QApplication

from .log import setup_logging
from .ui.main_window import MainWindow


def main():
    setup_logging()

    # 处理命令行参数
    if "--help" in sys.argv or "-h" in sys.argv:
        print("DDNet Change Color - DDNet 颜色修改工具")
        print("\n使用方法:")
        print("  python -m ddnet_change_color [选项]")
        print("\n选项:")
        print("  -h, --help     显示此帮助信息")
        print("  -v, --version  显示版本信息")
        print("\n启动应用:")
        print("  不带任何参数启动应用")
        sys.exit(0)

    if "--version" in sys.argv or "-v" in sys.argv:
        from . import __version__

        print(f"DDNet Change Color 版本 {__version__}")
        sys.exit(0)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
