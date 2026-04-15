# 贡献指南

欢迎为 DDNet 换色工具项目贡献代码！本指南将帮助你了解如何参与项目开发。

## 📋 开始之前

### 开发环境设置
1. **克隆仓库**
   ```bash
   git clone https://github.com/CAESIUS-TIM/ddnet-change-color.git
   cd ddnet-change-color
   ```

2. **设置虚拟环境**
   ```bash
   uv sync --dev
   ```

3. **验证安装**
   ```bash
   uv run python -m ddnet_change_color
   ```

### 代码质量工具
项目使用以下工具确保代码质量：
- **ruff**: 代码检查和格式化
- **pyright**: 静态类型检查  
- **pytest**: 测试框架
- **pytest-qt**: Qt 应用测试

## 🚀 开发流程

### 1. 选择任务
- 查看 [TODO.md](TODO.md) 中的任务列表
- 或查看 GitHub Issues 中标记为 `good first issue` 的 issue
- 在 issue 中留言表示你将负责该任务

### 2. 创建开发分支
使用 jujutsu 创建工作变更：
```bash
jj new -m "feat(scope): 简短描述"
```

### 3. 实现功能
- 遵循项目代码规范（见 [AGENTS.md](AGENTS.md)）
- 编写清晰的代码注释
- 添加必要的测试

### 4. 运行测试和检查
```bash
# 运行所有测试
just test

# 代码质量检查
just lint

# 类型检查
uv run pyright
```

### 5. 提交变更
```bash
jj amend -m "feat(scope): 详细描述变更"
```

### 6. 创建 Pull Request
1. 推送变更到 GitHub
2. 创建 Pull Request
3. 填写 PR 模板，描述变更内容
4. 等待代码审查

## 📝 代码规范

### 提交信息格式
使用约定式提交格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构代码
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变更

**示例**:
```
feat(models): 添加颜色预设支持

- 新增 PresetManager 类
- 支持预设保存和加载
- 添加预设管理对话框

Closes #123
```

### Python 代码规范
- 使用类型注解
- 遵循 PEP 8 风格指南
- 使用 Google 风格文档字符串
- 导入顺序：标准库 → 第三方库 → 本地模块

### 测试要求
- 新功能必须包含测试
- 测试覆盖率不能低于 94%
- UI 测试使用 `pytest-qt`
- 使用 fixture 共享测试设置

## 🧪 测试指南

### 运行测试
```bash
# 所有测试
uv run pytest

# 特定模块测试
uv run pytest tests/test_models/

# 带覆盖率报告
uv run pytest --cov=ddnet_change_color --cov-report=term-missing
```

### 编写测试
```python
def test_color_store_add_color(store: ColorStore):
    """测试添加颜色功能"""
    store.add_color("#66ccff")
    assert store.colors == ["#66ccff"]
```

### UI 测试注意事项
```python
def test_main_window_init(qtbot):
    """测试主窗口初始化"""
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.store is not None
```

## 🔍 代码审查

### 审查标准
- 代码符合项目规范
- 功能实现正确
- 测试覆盖充分
- 文档更新完整
- 向后兼容性考虑

### 审查流程
1. 至少需要一位维护者批准
2. 所有检查必须通过（测试、lint、类型检查）
3. 合并前解决所有评论

## 🐛 报告问题

### Bug 报告
1. 使用 GitHub Issues 报告问题
2. 提供详细的重现步骤
3. 包括错误信息和截图
4. 说明期望的行为

### 功能请求
1. 在 Issues 中描述功能需求
2. 说明使用场景和预期收益
3. 提供可能的实现思路

## 📞 获取帮助

- **文档**: 查看 [AGENTS.md](AGENTS.md) 和 [README.md](README.md)
- **讨论**: 在 GitHub Discussions 中提问
- **问题**: 在 Issues 中报告

## 🙏 致谢

感谢所有贡献者的付出！你的每一行代码都让项目变得更好。

---
*本指南基于 [GitHub 标准贡献指南](https://github.com/github/docs/blob/main/CONTRIBUTING.md) 编写*