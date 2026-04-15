"""共享测试配置和 fixture"""

import pytest

from ddnet_change_color.models.color_store import ColorStore


@pytest.fixture
def temp_config_dir(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """临时配置目录 fixture，隔离测试配置"""
    config_dir = tmp_path / ".ddnet-change-color"
    config_file = config_dir / "colors.json"

    # Patch config module
    monkeypatch.setattr("ddnet_change_color.config.CONFIG_DIR", config_dir)
    monkeypatch.setattr("ddnet_change_color.config.CONFIG_FILE", config_file)

    # Also patch references in modules that imported these constants
    monkeypatch.setattr("ddnet_change_color.models.color_store.CONFIG_DIR", config_dir)
    monkeypatch.setattr("ddnet_change_color.models.color_store.CONFIG_FILE", config_file)

    return config_dir, config_file


@pytest.fixture
def store(temp_config_dir):
    """ColorStore 实例 fixture"""
    return ColorStore()


@pytest.fixture
def sample_colors():
    """示例颜色列表 fixture"""
    return ["#66ccff", "#12231a", "#ff9900"]


@pytest.fixture
def sample_config_data():
    """示例配置数据 fixture"""
    return {
        "colors": ["#123456", "#789abc"],
        "settings": {"bind_key": "ctrl+t", "output_folder": "./test-output"},
    }
