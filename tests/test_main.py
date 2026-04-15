from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QMessageBox
import json
from unittest.mock import patch, MagicMock

import pytest

from ddnet_change_color.widget import ColorStore


@pytest.fixture
def temp_config_dir(monkeypatch: pytest.MonkeyPatch, tmp_path):
    config_dir = tmp_path / ".ddnet-change-color"
    config_file = config_dir / "colors.json"
    monkeypatch.setattr("ddnet_change_color.widget.CONFIG_DIR", config_dir)
    monkeypatch.setattr("ddnet_change_color.widget.CONFIG_FILE", config_file)
    return config_dir, config_file


@pytest.fixture
def store(temp_config_dir):
    return ColorStore()


class TestColorStore:
    def test_default_values(self, store: ColorStore):
        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_add_color(self, store: ColorStore):
        store.add_color("#66ccff")
        assert store.colors == ["#66ccff"]

    def test_add_duplicate_color(self, store: ColorStore):
        store.add_color("#66ccff")
        store.add_color("#66ccff")
        assert store.colors == ["#66ccff"]

    def test_remove_color(self, store: ColorStore):
        store.colors = ["#66ccff", "#12231a"]
        store.remove_color(0)
        assert store.colors == ["#12231a"]

    def test_remove_color_invalid_index(self, store: ColorStore):
        store.colors = ["#66ccff"]
        store.remove_color(5)
        assert store.colors == ["#66ccff"]

    def test_update_color(self, store: ColorStore):
        store.colors = ["#66ccff"]
        store.update_color(0, "#ff0000")
        assert store.colors == ["#ff0000"]

    def test_update_color_invalid_index(self, store: ColorStore):
        store.colors = ["#66ccff"]
        store.update_color(5, "#ff0000")
        assert store.colors == ["#66ccff"]

    def test_move_color(self, store: ColorStore):
        store.colors = ["#66ccff", "#12231a", "#ff0000"]
        store.move_color(0, 2)
        assert store.colors == ["#12231a", "#ff0000", "#66ccff"]

    def test_save_and_load(self, temp_config_dir, store: ColorStore):
        store.colors = ["#66ccff", "#12231a"]
        store.bind_key = "ctrl+q"
        store.output_folder = "./output"
        store.save()

        _, config_file = temp_config_dir
        assert config_file.exists()

        with open(config_file) as f:
            data = json.load(f)

        assert data["colors"] == ["#66ccff", "#12231a"]
        assert data["settings"]["bind_key"] == "ctrl+q"
        assert data["settings"]["output_folder"] == "./output"

    def test_load_existing_wrong_colors_config(self, temp_config_dir):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        data = {
            "colors": ["#abc"],
            "settings": {"bind_key": "t", "output_folder": "./test"},
        }
        with open(config_file, "w") as f:
            json.dump(data, f)

        store = ColorStore()

        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_load_existing_wrong_bind_key_config(self, temp_config_dir):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        data = {
            "colors": ["#22ffcc"],
            "settings": {"bind_key": "ctrl+", "output_folder": "./test"},
        }
        with open(config_file, "w") as f:
            json.dump(data, f)

        store = ColorStore()

        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_load_existing_wrong_output_folder_config(self, temp_config_dir):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        data = {
            "colors": ["#ffcc11"],
            "settings": {"bind_key": "t", "output_folder": 1},
        }
        with open(config_file, "w") as f:
            json.dump(data, f)

        store = ColorStore()

        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_load_corrupted_config(self, temp_config_dir):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        with open(config_file, "w") as f:
            f.write("invalid json{")

        from ddnet_change_color.widget import ColorStore

        store = ColorStore()

        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_load_colors_not_list(self, temp_config_dir):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        data = {
            "colors": "not a list",
            "settings": {"bind_key": "t", "output_folder": "./test"},
        }
        with open(config_file, "w") as f:
            json.dump(data, f)

        from ddnet_change_color.widget import ColorStore

        store = ColorStore()

        assert store.colors == []
        assert store.bind_key == "w"
        assert store.output_folder == "./change-colors"

    def test_load_success_logging(self, temp_config_dir, caplog):
        config_dir, config_file = temp_config_dir
        config_dir.mkdir(parents=True)

        data = {
            "colors": ["#123456"],
            "settings": {"bind_key": "a", "output_folder": "./test"},
        }
        with open(config_file, "w") as f:
            json.dump(data, f)

        from ddnet_change_color.widget import ColorStore
        import logging

        caplog.set_level(logging.INFO)

        store = ColorStore()

        assert store.colors == ["#123456"]
        assert store.bind_key == "a"
        assert store.output_folder == "./test"
        assert f"Config loaded from {config_file}" in caplog.text


class TestSettingsDialog:
    def test_settings_dialog_accept(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import ColorStore, SettingsDialog

        store = ColorStore()
        store.bind_key = "x"
        store.output_folder = "./test-folder"

        dialog = SettingsDialog(store)
        qtbot.addWidget(dialog)

        dialog.bind_edit.setText("y")
        dialog.folder_edit.setText("/tmp/output")

        dialog.accept()

        assert store.bind_key == "y"
        assert store.output_folder == "/tmp/output"

    def test_settings_dialog_cancel(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import ColorStore, SettingsDialog

        store = ColorStore()
        store.bind_key = "x"
        store.output_folder = "./test-folder"

        dialog = SettingsDialog(store)
        qtbot.addWidget(dialog)

        dialog.bind_edit.setText("y")

        dialog.reject()

        assert store.bind_key == "x"

    def test_settings_dialog_default_bind_key(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import ColorStore, SettingsDialog

        store = ColorStore()

        dialog = SettingsDialog(store)
        qtbot.addWidget(dialog)

        dialog.bind_edit.setText("")
        dialog.accept()

        assert store.bind_key == "w"

    def test_settings_dialog_choose_folder(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import ColorStore, SettingsDialog

        store = ColorStore()
        store.output_folder = "./initial"

        dialog = SettingsDialog(store)
        qtbot.addWidget(dialog)

        with patch(
            "ddnet_change_color.widget.QFileDialog.getExistingDirectory"
        ) as mock_get_dir:
            mock_get_dir.return_value = "/selected/folder"
            dialog.choose_folder()

            mock_get_dir.assert_called_once_with(dialog, "选择输出目录", "./initial")
            assert dialog.folder_edit.text() == "/selected/folder"


class TestMainWindow:
    def test_main_window_init(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        assert window.store is not None
        assert len(window.store.colors) == 0

    def test_add_color(self, temp_config_dir, qtbot):
        from PySide6.QtGui import QColor
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        initial_count = window.list_widget.count()

        with patch("ddnet_change_color.widget.QColorDialog.getColor") as mock_get_color:
            mock_color = QColor("#ff0000")
            mock_get_color.return_value = mock_color

            window.add_color()

        assert window.list_widget.count() == initial_count + 1

    def test_export_config_empty_colors(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.widget.QMessageBox.warning") as mock_warning:
            window.export_config()
            mock_warning.assert_called_once()

    def test_export_config_success(self, temp_config_dir, qtbot, tmp_path):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff", "#12231a"]
        window.store.output_folder = str(tmp_path / "output")
        window.store.save()

        window._load_colors()

        with patch("ddnet_change_color.widget.QMessageBox.information") as mock_info:
            window.export_config()
            mock_info.assert_called_once()

        output_dir = tmp_path / "output"
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.cfg"))) == 2

    def test_add_color_at_index(self, temp_config_dir, qtbot):
        from PySide6.QtGui import QColor
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QColorDialog.getColor") as mock_get_color:
            mock_color = QColor("#ff0000")
            mock_get_color.return_value = mock_color

            window._add_color_item("#ff0000", index=0)

        assert window.list_widget.count() == 2

    def test_show_settings(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.widget.SettingsDialog") as mock_dialog:
            mock_dialog_instance = mock_dialog.return_value
            mock_dialog_instance.exec.return_value = 1

            window.show_settings()

            mock_dialog.assert_called_once()

    def test_context_menu_copy(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        with patch(
            "ddnet_change_color.widget.QGuiApplication.clipboard"
        ) as mock_clipboard:
            window.copy_color(0)
            mock_clipboard.return_value.setText.assert_called_once_with("#66ccff")

    def test_context_menu_modify(self, temp_config_dir, qtbot):
        from PySide6.QtGui import QColor
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QColorDialog.getColor") as mock_get_color:
            mock_color = QColor("#ff0000")
            mock_get_color.return_value = mock_color

            window.modify_color(0)

        assert window.store.colors[0] == "#FF0000"

    def test_modify_color_type_error(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QColorDialog.getColor") as mock_get_color:
            mock_get_color.return_value.isValid.return_value = True
            mock_get_color.return_value.name.return_value = "#FF0000"

            with patch.object(window.list_widget, "itemWidget", return_value=None):
                try:
                    window.modify_color(0)
                except TypeError as e:
                    assert "Expected ColorItemWidget" in str(e)
                else:
                    assert False, "Expected TypeError not raised"

    def test_context_menu_delete(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff", "#12231a"]
        window.store.save()
        window._load_colors()

        window.delete_color(0)

        assert window.store.colors == ["#12231a"]
        assert window.list_widget.count() == 1

    def test_close_event_saves_order(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow
        from unittest.mock import MagicMock

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        event = MagicMock()
        window.closeEvent(event)

        event.accept.assert_called_once()

    def test_show_context_menu(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        item = window.list_widget.item(0)
        pos = window.list_widget.visualItemRect(item).center()

        with patch("ddnet_change_color.widget.QMenu") as mock_menu:
            mock_menu_instance = mock_menu.return_value
            mock_menu_instance.exec.return_value = None
            mock_menu_instance.addAction = MagicMock()

            window.show_context_menu(pos)

            mock_menu.assert_called_once()
            assert mock_menu_instance.addAction.call_count == 3

    def test_show_context_menu_no_item(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.save()
        window._load_colors()

        pos = window.list_widget.visualItemRect(window.list_widget.item(0)).center()
        pos.setY(pos.y() + 100)

        with patch("ddnet_change_color.widget.QMenu") as mock_menu:
            window.show_context_menu(pos)
            mock_menu.assert_not_called()

    def test_show_context_menu_empty_list(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.widget.QMenu") as mock_menu:
            window.show_context_menu(QPoint(10, 10))
            mock_menu.assert_not_called()

    def test_export_config_with_existing_folder(self, temp_config_dir, qtbot, tmp_path):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "existing.cfg").write_text("old content")

        window.store.colors = ["#66ccff"]
        window.store.output_folder = str(output_dir)
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QMessageBox.question") as mock_question:
            # mock_question.return_value = window.Store.StandardButton.No
            mock_question.return_value = QMessageBox.StandardButton.No

            window.export_config()

            mock_question.assert_called_once()

    def test_export_config_with_error(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff"]
        window.store.output_folder = "/invalid/path/that/does/not/exist"
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QMessageBox.critical") as mock_critical:
            window.export_config()
            mock_critical.assert_called_once()

    def test_on_item_clicked(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        window.on_item_clicked(None)

    def test_export_config_clear_folder(self, temp_config_dir, qtbot, tmp_path):
        from ddnet_change_color.widget import MainWindow
        from PySide6.QtWidgets import QMessageBox

        window = MainWindow()
        qtbot.addWidget(window)

        output_dir = tmp_path / "output"
        output_dir.mkdir()
        (output_dir / "existing.cfg").write_text("old content")
        (output_dir / "another.cfg").write_text("another")

        window.store.colors = ["#66ccff", "#12231a"]
        window.store.output_folder = str(output_dir)
        window.store.save()
        window._load_colors()

        with patch("ddnet_change_color.widget.QMessageBox.question") as mock_question:
            mock_question.return_value = QMessageBox.StandardButton.Yes

            with patch(
                "ddnet_change_color.widget.QMessageBox.information"
            ) as mock_info:
                window.export_config()

                mock_question.assert_called_once()
                mock_info.assert_called_once()

                assert output_dir.exists()
                assert len(list(output_dir.glob("*.cfg"))) == 2

    def test_close_event_saves_new_order(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow
        from unittest.mock import MagicMock

        window = MainWindow()
        qtbot.addWidget(window)

        window.store.colors = ["#66ccff", "#12231a"]
        window.store.save()
        window._load_colors()

        item0 = window.list_widget.item(0)
        item1 = window.list_widget.item(1)
        item0.setData(Qt.ItemDataRole.UserRole, "#12231a")
        item1.setData(Qt.ItemDataRole.UserRole, "#66ccff")

        event = MagicMock()
        window.closeEvent(event)

        event.accept.assert_called_once()
        assert window.store.colors == ["#12231a", "#66ccff"]


class TestConstant:
    def test_is_valid_color(self):
        from ddnet_change_color.constant import is_valid_color

        assert is_valid_color("#FFFFFF")
        assert is_valid_color("#ffffff")
        assert is_valid_color("#123456")
        assert is_valid_color("#ABCDEF")

        assert not is_valid_color("#FFF")
        assert not is_valid_color("#fffffff")
        assert not is_valid_color("FFFFFF")
        assert not is_valid_color("#GGGGGG")
        assert not is_valid_color("")
        assert not is_valid_color("#12345")
        assert not is_valid_color("#1234567")

    def test_is_valid_bind_key(self):
        from ddnet_change_color.constant import is_valid_bind_key

        assert is_valid_bind_key("a")
        assert is_valid_bind_key("z")
        assert is_valid_bind_key("1")
        assert is_valid_bind_key("f1")
        assert is_valid_bind_key("space")

        assert is_valid_bind_key("ctrl+a")
        assert is_valid_bind_key("shift+b")
        assert is_valid_bind_key("alt+c")

        assert not is_valid_bind_key("")
        assert not is_valid_bind_key("invalid")
        assert not is_valid_bind_key("ctrl+")
        assert not is_valid_bind_key("+a")
        assert not is_valid_bind_key("ctrl+shift+a")
        assert not is_valid_bind_key("ctrl+invalid")
        assert not is_valid_bind_key("ctrl+ctrl")
        assert not is_valid_bind_key("alt+shift")
