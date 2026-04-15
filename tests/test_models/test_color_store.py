import json

from ddnet_change_color.models.color_store import ColorStore


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

        import logging

        from ddnet_change_color.widget import ColorStore

        caplog.set_level(logging.INFO)

        store = ColorStore()

        assert store.colors == ["#123456"]
        assert store.bind_key == "a"
        assert store.output_folder == "./test"
        assert f"Config loaded from {config_file}" in caplog.text
