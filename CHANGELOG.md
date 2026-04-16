# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 完整的 CI/CD 发布流水线
- 多平台单文件可执行程序打包支持 (Windows, macOS, Linux)
- 自动化 GitHub Releases 发布流程
- 构建系统模块 (`build/`) 包含平台特定配置
- 命令行构建工具 (`build_script.py`)
- GitHub Actions 工作流 (`ci.yml`, `release.yml`)
- 图标资源和桌面集成文件
- Windows 版本信息文件
- macOS Info.plist 模板
- Linux .desktop 桌面入口文件

### Changed
- 重构 MainWindow 到 `ui/main_window.py` 模块
- 更新项目结构文档
- 改进测试模块组织

### Fixed
- 保持向后兼容的导入

## [0.1.0] - 2025-04-15

### Added
- 初始版本发布
- 基础颜色管理功能
- 可视化颜色编辑界面
- 拖拽重新排序颜色
- 自定义绑定键和输出目录配置
- 配置持久化保存
- 完整的测试套件（覆盖率 >97%）
- 代码质量检查工具配置
- 项目文档和贡献指南

### Technical Details
- Python 3.14+ with PySide6 Qt 框架
- 模块化架构：models, dialogs, widgets, ui, utils
- 使用 uv 进行依赖管理
- 使用 jujutsu 进行版本控制
- 完整的开发工具链（ruff, pyright, pytest）

## 发布说明

### 版本命名规则
- `v0.1.0`: 初始功能完整的发布
- `v1.0.0`: 第一个稳定版本
- `v1.2.3`: 语义化版本 (主版本.次版本.修订版本)

### 发布流程
1. 创建版本标签：`git tag v1.2.3`
2. 推送标签：`git push origin v1.2.3`
3. GitHub Actions 自动构建并发布到 GitHub Releases

### 校验和验证
每个发布文件都包含 SHA256 校验和文件，用于验证文件完整性。

**Windows**:
```powershell
certutil -hashfile ddnet-change-color-windows-*.exe SHA256
```

**macOS**:
```bash
shasum -a 256 ddnet-change-color-macos-*.zip
```

**Linux**:
```bash
sha256sum ddnet-change-color-linux-*.tar.gz
```