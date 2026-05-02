"""Quality presets shared by the yt-dlp and spotdl backends."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    """A normalized download recipe.

    Attributes:
        name: Human-readable preset id (e.g. ``mp3-320``).
        format_code: yt-dlp ``-f`` format expression.
        codec: Target audio codec for post-processing (or ``None`` to keep source).
        bitrate_kbps: Target audio bitrate in kbps (or ``None`` if codec uses VBR/lossless).
        is_video: Whether the preset keeps the video stream.
    """

    name: str
    format_code: str
    codec: str | None
    bitrate_kbps: int | None
    is_video: bool = False


PRESETS: dict[str, Preset] = {
    "mp3-320": Preset("mp3-320", "bestaudio/best", "mp3", 320),
    "mp3-192": Preset("mp3-192", "bestaudio/best", "mp3", 192),
    "mp3-128": Preset("mp3-128", "bestaudio/best", "mp3", 128),
    "opus": Preset("opus", "bestaudio/best", "opus", None),
    "m4a": Preset("m4a", "bestaudio[ext=m4a]/bestaudio/best", "m4a", None),
    "flac": Preset("flac", "bestaudio/best", "flac", None),
    "best-audio": Preset("best-audio", "bestaudio/best", None, None),
    "best-video": Preset(
        "best-video",
        "bestvideo*+bestaudio/best",
        None,
        None,
        is_video=True,
    ),
}

DEFAULT_PRESET = "mp3-320"


def get_preset(name: str) -> Preset:
    """Resolve a preset by name (case-insensitive)."""
    key = name.lower().strip()
    if key not in PRESETS:
        valid = ", ".join(sorted(PRESETS))
        raise ValueError(f"Unknown preset {name!r}. Valid options: {valid}")
    return PRESETS[key]


def list_preset_names() -> list[str]:
    return sorted(PRESETS)
