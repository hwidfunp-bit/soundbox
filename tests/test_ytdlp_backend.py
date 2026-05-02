from pathlib import Path

from soundbox.presets import get_preset
from soundbox.ytdlp_backend import build_options


def test_build_options_mp3_320(tmp_path: Path) -> None:
    preset = get_preset("mp3-320")
    opts = build_options(preset, tmp_path, download_playlist=False, quiet=True)

    assert opts["format"] == "bestaudio/best"
    assert opts["noplaylist"] is True
    assert str(tmp_path) in opts["outtmpl"]

    extract = next(p for p in opts["postprocessors"] if p["key"] == "FFmpegExtractAudio")
    assert extract["preferredcodec"] == "mp3"
    assert extract["preferredquality"] == "320"


def test_build_options_best_video(tmp_path: Path) -> None:
    preset = get_preset("best-video")
    opts = build_options(preset, tmp_path, download_playlist=True, quiet=False)

    assert opts["format"] == "bestvideo*+bestaudio/best"
    assert opts["noplaylist"] is False
    assert "%(playlist_title" in opts["outtmpl"]
    pp_keys = [p["key"] for p in opts["postprocessors"]]
    assert "FFmpegVideoConvertor" in pp_keys
    assert "FFmpegExtractAudio" not in pp_keys


def test_build_options_opus_no_bitrate(tmp_path: Path) -> None:
    preset = get_preset("opus")
    opts = build_options(preset, tmp_path, download_playlist=False, quiet=True)
    extract = next(p for p in opts["postprocessors"] if p["key"] == "FFmpegExtractAudio")
    assert extract["preferredcodec"] == "opus"
    assert "preferredquality" not in extract
