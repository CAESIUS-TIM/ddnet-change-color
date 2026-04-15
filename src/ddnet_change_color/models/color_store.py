"""数据模型：颜色存储和管理"""

import json
import logging
from pathlib import Path
from typing import override

from ..config import CONFIG_DIR, CONFIG_FILE
from ..constant import is_valid_color, is_valid_bind_key

logger = logging.getLogger(__name__)


class ColorStore:
    def __init__(self):
        self.colors: list[str] = []
        self.bind_key: str = "w"
        self.output_folder: str = "./change-colors"
        self.load()

    def load(self):
        if not CONFIG_FILE.exists():
            return
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)  # pyright: ignore[reportAny]
            # 1. colors
            colors_raw = data.get("colors", [])  # pyright: ignore[reportAny]
            logger.debug(f"'colors_raw': {colors_raw}")
            if not isinstance(colors_raw, list):
                raise ValueError("'colors' must be a list")
            valid_colors: list[str] = []
            for color in colors_raw:  # pyright: ignore[reportUnknownVariableType]
                if not isinstance(color, str) or not is_valid_color(color):
                    raise ValueError(f"invalid color format: '{color}'")
                else:
                    logger.debug(f"Color '{color}' is valid")
                    valid_colors.append(color)

            # 2. bind_key
            bind_key = data.get("settings", {}).get("bind_key", "w")  # pyright: ignore[reportAny]
            logger.debug(f"'bind_key': {bind_key}")
            if not isinstance(bind_key, str) or not is_valid_bind_key(bind_key):
                raise ValueError(f"invalid bind key: '{bind_key}'")

            # 3. output_folder
            output_folder = data.get("settings", {}).get(  # pyright: ignore[reportAny]
                "output_folder", "./change-colors"
            )
            logger.debug(f"'output_folder': {output_folder}")
            if not isinstance(output_folder, str):
                raise ValueError(f"invalid output path: '{output_folder}'")

            # 4. atomic update
            self.colors = valid_colors
            self.bind_key = bind_key
            self.output_folder = output_folder
            logger.info(f"Config loaded from {CONFIG_FILE}")

        except (json.JSONDecodeError, IOError, ValueError) as e:
            logger.warning(f"Failed to load config from {CONFIG_FILE}: {e}")

    def save(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "colors": self.colors,
            "settings": {
                "bind_key": self.bind_key,
                "output_folder": self.output_folder,
            },
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add_color(self, hex_color: str):
        if hex_color not in self.colors:
            self.colors.append(hex_color)
            self.save()

    def remove_color(self, index: int):
        if 0 <= index < len(self.colors):
            self.colors.pop(index)  # pyright: ignore[reportUnusedCallResult]
            self.save()

    def update_color(self, index: int, hex_color: str):
        if 0 <= index < len(self.colors):
            self.colors[index] = hex_color
            self.save()

    def move_color(self, from_idx: int, to_idx: int):
        if 0 <= from_idx < len(self.colors) and 0 <= to_idx < len(self.colors):
            color = self.colors.pop(from_idx)
            self.colors.insert(to_idx, color)
            self.save()