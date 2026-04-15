# 开发规范与工具配置

## 📁 项目结构

### 源码结构 (`src/ddnet_change_color/`)
```
src/ddnet_change_color/
├── __init__.py              # 包导出，保持向后兼容
├── __main__.py             # 应用入口点
├── config.py               # 包级配置和常量管理
├── constants.py            # 验证函数和常量集合
├── models/                 # 数据模型层
│   ├── __init__.py
│   └── color_store.py      # ColorStore 数据模型
├── dialogs/                # 对话框组件
│   ├── __init__.py
│   └── settings_dialog.py  # 设置对话框
├── widgets/                # UI 小部件
│   ├── __init__.py
│   ├── color_list.py       # 颜色列表组件
│   └── color_item.py       # 颜色项组件
├── ui/                     # 主界面
│   ├── __init__.py
│   └── main_window.py      # 主窗口
└── utils/                  # 工具函数
    ├── __init__.py
    └── logging.py          # 日志配置
```

### 测试结构 (`tests/`)
```
tests/
├── conftest.py             # 共享 fixture 和配置
├── __init__.py
├── test_models/           # 模型测试
│   ├── __init__.py
│   └── test_color_store.py
├── test_dialogs/          # 对话框测试
│   ├── __init__.py
│   └── test_settings_dialog.py
├── test_widgets/          # 小部件测试
│   ├── __init__.py
│   ├── test_color_list.py
│   └── test_color_item.py
├── test_ui/               # UI 测试
│   ├── __init__.py
│   └── test_main_window.py
├── test_utils/            # 工具测试
│   ├── __init__.py
│   └── test_constants.py
└── test_integration.py    # 集成测试
```

## 🛠️ 开发工具配置

### 包管理 (uv)
```bash
# 安装依赖
uv sync

# 安装开发依赖
uv sync --dev

# 添加新依赖
uv add <package>
uv add --dev <package>
uv add --group <group> <package>
```

### 代码质量检查
```bash
# 代码格式化和检查
uv run ruff check .          # 检查
uv run ruff format .         # 格式化
uv run ruff check --fix .    # 自动修复

# 类型检查
uv run pyright

# 综合检查
just lint                    # 运行所有检查
```

### 测试
```bash
# 运行所有测试
just test
# 或
uv run pytest

# 运行特定测试
uv run pytest tests/test_models/
uv run pytest -k "test_color_store"

# 带覆盖率报告
uv run pytest --cov=ddnet_change_color --cov-report=term-missing

# 生成 HTML 报告
uv run pytest --cov=ddnet_change_color --cov-report=html
```

### 运行应用
```bash
just run
# 或
uv run python -m ddnet_change_color
```

## 📝 代码规范

### 导入顺序
1. 标准库导入
2. 第三方库导入
3. 本地模块导入
4. 相对导入

使用 ruff 自动排序导入。

### 类型注解
- 所有函数和方法必须有类型注解
- 使用 `typing` 模块中的泛型
- 复杂的类型使用 `TypeAlias` 定义

### 命名约定
- 类名：`PascalCase`
- 函数名：`snake_case`
- 变量名：`snake_case`
- 常量：`UPPER_SNAKE_CASE`
- 私有成员：`_leading_underscore`
- 模块私有：`__double_underscore`

### 文档字符串
- 所有公共模块、类、函数必须有文档字符串
- 使用 Google 风格文档字符串
- 包含参数、返回值和异常说明

### 错误处理
- 使用具体的异常类型
- 提供有意义的错误信息
- 使用 `try-except` 处理可恢复错误
- 使用 `logging` 记录异常

## 🔄 版本控制工作流

### Jujutsu (jj) 工作流

#### 基础命令
```bash
# 查看状态
jj status
jj log

# 创建新变更
jj new -m "描述信息"
jj amend            # 修改当前变更
jj edit <change-id> # 切换到指定变更

# 同步 Git
jj git fetch
jj git push
jj git pull
```

#### 提交规范
使用约定式提交格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变更

**示例**:
```bash
jj new -m "feat(models): 添加颜色预设支持

- 新增 PresetManager 类
- 支持预设保存和加载
- 添加预设管理对话框"
```

### Git 集成
项目使用 jujutsu 作为主要版本控制，但保持与 Git 的兼容性：

```bash
# 从 jj 推送到 Git 远程仓库
jj git push

# 从 Git 拉取更新
jj git fetch
jj git rebase -r main

# 查看 Git 状态
jj git status
```

## 🧪 测试规范

### 测试编写指南
1. **每个测试一个断言**: 保持测试简洁
2. **描述性测试名**: 使用 `test_<场景>_<期望>` 格式
3. **使用 fixture**: 共享设置代码放到 fixture 中
4. **模拟外部依赖**: 使用 `unittest.mock` 模拟 UI 和文件系统

### 测试覆盖率要求
- 总体覆盖率 ≥ 94%
- 新功能必须包含测试
- 重构不能降低覆盖率

### UI 测试注意事项
- 使用 `pytest-qt` 进行 Qt 应用测试
- 使用 `qtbot` fixture 管理窗口生命周期
- 避免依赖特定的 UI 实现细节

## 🔧 开发工作流程

### 开始新功能开发
1. 创建新变更: `jj new -m "feat(scope): 简短描述"`
2. 实现功能
3. 编写测试
4. 运行检查: `just lint && just test`
5. 提交变更: `jj amend`

### 代码审查
1. 确保所有检查通过
2. 更新相关文档
3. 确保向后兼容性
4. 提供清晰的变更描述

### 发布准备
1. 更新版本号 (`pyproject.toml`)
2. 更新 CHANGELOG.md
3. 运行完整测试套件
4. 构建和测试安装包

## 📊 工具配置详情

### Ruff 配置 (`pyproject.toml`)
```toml
[tool.ruff]
target-version = "py314"
line-length = 100
select = ["E", "F", "I", "W"]
```

### Pyright 配置
```toml
[tool.pyright]
pythonVersion = "3.14"
typeCheckingMode = "strict"
```

### 预提交钩子 (可选)
项目支持 pre-commit 钩子，配置文件位于 `.pre-commit-config.yaml`

## 🆘 常见问题

### 测试失败
1. 检查 Qt 环境变量是否正确设置
2. 确认虚拟环境已激活
3. 运行 `uv sync --dev` 更新依赖

### 导入错误
1. 确保模块在 `src/ddnet_change_color/__init__.py` 中导出
2. 检查相对导入路径
3. 运行 `uv run python -c "import ddnet_change_color"` 测试导入

### Jujutsu 问题
1. 查看帮助: `jj help`
2. 重置状态: `jj abandon` (谨慎使用)
3. 同步 Git: `jj git fetch && jj rebase -r main`

---

**最后更新**: 2025-04-15  
**维护者**: @CAESIUS-TIM