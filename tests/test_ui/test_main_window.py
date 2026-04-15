from unittest.mock import MagicMock, patch

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QMessageBox


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

        with patch("ddnet_change_color.ui.main_window.QColorDialog.getColor") as mock_get_color:
            mock_color = QColor("#ff0000")
            mock_get_color.return_value = mock_color

            window.add_color()

        assert window.list_widget.count() == initial_count + 1

    def test_export_config_empty_colors(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.ui.main_window.QMessageBox.warning") as mock_warning:
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

        with patch("ddnet_change_color.ui.main_window.QMessageBox.information") as mock_info:
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

        with patch("ddnet_change_color.ui.main_window.QColorDialog.getColor") as mock_get_color:
            mock_color = QColor("#ff0000")
            mock_get_color.return_value = mock_color

            window._add_color_item("#ff0000", index=0)

        assert window.list_widget.count() == 2

    def test_show_settings(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.ui.main_window.SettingsDialog") as mock_dialog:
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
            "ddnet_change_color.ui.main_window.QGuiApplication.clipboard"
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

        with patch("ddnet_change_color.ui.main_window.QColorDialog.getColor") as mock_get_color:
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

        with patch("ddnet_change_color.ui.main_window.QColorDialog.getColor") as mock_get_color:
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
        from unittest.mock import MagicMock

        from ddnet_change_color.widget import MainWindow

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

        with patch("ddnet_change_color.ui.main_window.QMenu") as mock_menu:
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

        with patch("ddnet_change_color.ui.main_window.QMenu") as mock_menu:
            window.show_context_menu(pos)
            mock_menu.assert_not_called()

    def test_show_context_menu_empty_list(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)

        with patch("ddnet_change_color.ui.main_window.QMenu") as mock_menu:
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

        with patch("ddnet_change_color.ui.main_window.QMessageBox.question") as mock_question:
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

        with patch("ddnet_change_color.ui.main_window.QMessageBox.critical") as mock_critical:
            window.export_config()
            mock_critical.assert_called_once()

    def test_on_item_clicked(self, temp_config_dir, qtbot):
        from ddnet_change_color.widget import MainWindow

        window = MainWindow()
        qtbot.addWidget(window)
        window.on_item_clicked(None)

    def test_export_config_clear_folder(self, temp_config_dir, qtbot, tmp_path):
        from PySide6.QtWidgets import QMessageBox

        from ddnet_change_color.widget import MainWindow

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

        with patch("ddnet_change_color.ui.main_window.QMessageBox.question") as mock_question:
            mock_question.return_value = QMessageBox.StandardButton.Yes

            with patch(
                "ddnet_change_color.ui.main_window.QMessageBox.information"
            ) as mock_info:
                window.export_config()

                mock_question.assert_called_once()
                mock_info.assert_called_once()

                assert output_dir.exists()
                assert len(list(output_dir.glob("*.cfg"))) == 2

    def test_close_event_saves_new_order(self, temp_config_dir, qtbot):
        from unittest.mock import MagicMock

        from ddnet_change_color.widget import MainWindow

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


