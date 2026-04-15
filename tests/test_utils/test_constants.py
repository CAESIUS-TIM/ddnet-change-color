import pytest


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
