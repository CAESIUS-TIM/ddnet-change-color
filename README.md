# DDNet 换色工具

一个用于 DDNet 客户端的颜色配置文件生成工具，支持创建和管理颜色配置。

## 功能特性

- 🎨 可视化颜色管理界面
- 🔄 拖拽重新排序颜色
- ⚙️ 自定义绑定键和输出目录
- 📁 自动生成 DDNet 配置文件
- 💾 配置持久化保存

## 安装

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

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！请参考 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 相关链接

- [DDNet 官网](https://ddnet.org/)
- [DDNet 客户端配置文档](https://github.com/ddnet/ddnet#configuration)