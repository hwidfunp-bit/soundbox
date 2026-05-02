import pytest

from soundbox.presets import (
    DEFAULT_PRESET,
    PRESETS,
    get_preset,
    list_preset_names,
)


def test_default_preset_exists() -> None:
    assert DEFAULT_PRESET in PRESETS


def test_get_preset_case_insensitive() -> None:
    p = get_preset("MP3-320")
    assert p.name == "mp3-320"
    assert p.codec == "mp3"
    assert p.bitrate_kbps == 320
    assert p.is_video is False


def test_get_preset_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown preset"):
        get_preset("ultra-hd-9000")


def test_best_video_preset_marked_as_video() -> None:
    p = get_preset("best-video")
    assert p.is_video is True


def test_list_preset_names_sorted_and_complete() -> None:
    names = list_preset_names()
    assert names == sorted(names)
    assert set(names) == set(PRESETS.keys())
