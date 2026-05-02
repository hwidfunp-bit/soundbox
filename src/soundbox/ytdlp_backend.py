"""yt-dlp backend used for YouTube and SoundCloud."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console

from soundbox.presets import Preset

console = Console()


def _build_postprocessors(preset: Preset) -> list[dict[str, Any]]:
    """Return the FFmpeg postprocessor chain for the given preset."""
    pps: list[dict[str, Any]] = []
    if preset.is_video:
        # Make sure the merged container is mp4 for portability.
        pps.append({"key": "FFmpegVideoConvertor", "preferedformat": "mp4"})
        pps.append({"key": "FFmpegMetadata"})
        pps.append({"key": "EmbedThumbnail"})
        return pps

    if preset.codec is not None:
        pp: dict[str, Any] = {
            "key": "FFmpegExtractAudio",
            "preferredcodec": preset.codec,
        }
        if preset.bitrate_kbps is not None:
            pp["preferredquality"] = str(preset.bitrate_kbps)
        pps.append(pp)

    pps.append({"key": "FFmpegMetadata"})
    pps.append({"key": "EmbedThumbnail"})
    return pps


def build_options(
    preset: Preset,
    output_dir: Path,
    *,
    download_playlist: bool,
    quiet: bool,
) -> dict[str, Any]:
    """Build a yt-dlp options dict matching the preset."""
    output_dir.mkdir(parents=True, exist_ok=True)

    template = "%(title)s [%(id)s].%(ext)s"
    if download_playlist:
        template = "%(playlist_title|Playlist)s/%(playlist_index)s - " + template

    return {
        "format": preset.format_code,
        "outtmpl": str(output_dir / template),
        "noplaylist": not download_playlist,
        "quiet": quiet,
        "no_warnings": quiet,
        "writethumbnail": True,
        "embedthumbnail": True,
        "postprocessors": _build_postprocessors(preset),
        "restrictfilenames": False,
        "ignoreerrors": "only_download",
        "concurrent_fragment_downloads": 4,
        "retries": 5,
        "fragment_retries": 5,
    }


def download(
    url: str,
    preset: Preset,
    output_dir: Path,
    *,
    download_playlist: bool = False,
    quiet: bool = False,
) -> int:
    """Download ``url`` via yt-dlp using ``preset``.

    Returns the yt-dlp exit code (``0`` on success).
    """
    try:
        from yt_dlp import YoutubeDL  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - import-time failure
        raise RuntimeError(
            "yt-dlp is not installed. Run `pip install soundbox` or `pip install yt-dlp`."
        ) from exc

    opts = build_options(
        preset,
        output_dir,
        download_playlist=download_playlist,
        quiet=quiet,
    )

    if not quiet:
        console.print(
            f"[bold cyan]soundbox[/] · downloading [green]{url}[/] "
            f"→ preset [magenta]{preset.name}[/] → [yellow]{output_dir}[/]"
        )

    with YoutubeDL(opts) as ydl:
        return ydl.download([url])


def info(url: str) -> dict[str, Any]:
    """Fetch metadata for ``url`` without downloading anything."""
    try:
        from yt_dlp import YoutubeDL  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("yt-dlp is not installed.") from exc

    with YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
        data = ydl.extract_info(url, download=False)
    return data or {}
