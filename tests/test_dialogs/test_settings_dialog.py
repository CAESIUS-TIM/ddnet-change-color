import pytest
from unittest.mock import patch


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
            "ddnet_change_color.dialogs.settings_dialog.QFileDialog.getExistingDirectory"
        ) as mock_get_dir:
            mock_get_dir.return_value = "/selected/folder"
            dialog.choose_folder()

            mock_get_dir.assert_called_once_with(dialog, "选择输出目录", "./initial")
            assert dialog.folder_edit.text() == "/selected/folder"


