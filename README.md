# DDNet 换色工具

一个用于 DDNet 客户端的颜色配置文件生成工具，支持创建和管理颜色配置。

## 功能特性

- 🎨 可视化颜色管理界面
- 🔄 拖拽重新排序颜色
- ⚙️ 自定义绑定键和输出目录
- 📁 自动生成 DDNet 配置文件
- 💾 配置持久化保存

## 安装

### 下载预编译版本（推荐）
前往 [GitHub Releases](https://github.com/CAESIUS-TIM/ddnet-change-color/releases) 下载对应平台的单文件可执行程序：

- **Windows**: `ddnet-change-color-windows-*.exe`
- **macOS**: `ddnet-change-color-macos-*.zip` (解压后运行 .app)
- **Linux**: `ddnet-change-color-linux-*.tar.gz` (解压后运行可执行文件)

### 使用 pip
```bash
pip install ddnet-change-color
```

### 从源码运行
```bash
git clone https://github.com/CAESIUS-TIM/ddnet-change-color.git
cd ddnet-change-color
uv install
uv run python -m ddnet_change_color
```

## 使用说明

1. **添加颜色**: 点击"添加颜色"按钮选择颜色
2. **管理颜色**: 右键点击颜色项进行复制、修改、删除操作
3. **拖拽排序**: 拖动颜色项重新排列顺序
4. **设置配置**: 点击"设置"按钮配置绑定键和输出目录
5. **导出配置**: 点击"导出配置"生成 DDNet 配置文件

## 开发

### 环境设置
```bash
uv sync --dev
```

### 运行测试
```bash
just test
# 或
uv run pytest
```

### 代码质量检查
```bash
uv run ruff check .
uv run pyright
```

### 运行应用
```bash
just run
# 或
uv run python -m ddnet_change_color
```

## 项目结构

```
src/ddnet_change_color/
├── config.py          # 包级配置和常量
├── constants.py       # 验证函数和常量集合
├── models/           # 数据模型
├── dialogs/          # 对话框组件
├── widgets/          # UI 小部件
├── ui/               # 主界面
└── utils/            # 工具函数
```

## 技术栈

- **Python 3.14+**
- **PySide6**: Qt 框架绑定
- **pytest**: 测试框架
- **ruff**: 代码检查和格式化
- **pyright**: 静态类型检查
- **PyInstaller**: 应用打包
- **GitHub Actions**: CI/CD 自动化

## 构建和发布

### 本地构建
```bash
# 安装构建依赖
uv sync --group build

# 为当前平台构建单文件可执行程序
python build_script.py

# 为指定平台构建
python build_script.py --platform windows
python build_script.py --platform linux
python build_script.py --platform darwin

# 验证构建环境
python build_script.py --validate

# 清理构建目录
python build_script.py --clean
```

### 发布流程
项目使用自动化发布流程：

1. **创建版本标签**
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

2. **自动触发发布**
   - GitHub Actions 自动为 Windows、macOS、Linux 构建单文件可执行程序
   - 生成 SHA256 校验和
   - 创建 GitHub Release 包含所有平台二进制文件

3. **手动构建（高级）**
   ```bash
   # 为所有平台构建
   python build_script.py --all
   
   # 使用目录模式（开发）
   python build_script.py --no-onefile
   ```

### 平台支持
- **Windows**: 单文件 `.exe` 程序，隐藏控制台窗口
- **macOS**: 应用程序包 `.app`，支持代码签名
- **Linux**: 可执行文件，支持桌面集成（.desktop 文件）

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 相关链接

- [DDNet 官网](https://ddnet.org/)
- [DDNet 客户端配置文档](https://github.com/ddnet/ddnet#configuration) 