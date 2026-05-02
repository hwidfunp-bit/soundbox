"""Spotify backend (delegates to spotdl, which uses Spotify metadata + YouTube audio)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console

from soundbox.presets import Preset

console = Console()


def _preset_to_spotdl_args(preset: Preset) -> list[str]:
    """Translate a soundbox preset into spotdl CLI flags."""
    if preset.is_video:
        # spotdl doesn't do video; fall back to lossy audio.
        return ["--format", "mp3", "--bitrate", "320k"]

    codec = preset.codec or "mp3"
    args = ["--format", codec]
    if preset.bitrate_kbps is not None:
        args += ["--bitrate", f"{preset.bitrate_kbps}k"]
    return args


def _resolve_spotdl_command() -> list[str] | None:
    """Locate a runnable spotdl entry point.

    Returns ``None`` if spotdl is not installed.
    """
    on_path = shutil.which("spotdl")
    if on_path:
        return [on_path]

    try:
        import spotdl  # type: ignore[import-not-found]  # noqa: F401
    except ImportError:
        return None

    return [sys.executable, "-m", "spotdl"]


def download(
    url: str,
    preset: Preset,
    output_dir: Path,
    *,
    quiet: bool = False,
) -> int:
    """Download a Spotify track / playlist / album via spotdl."""
    cmd = _resolve_spotdl_command()
    if cmd is None:
        raise RuntimeError(
            "Spotify support requires spotdl. Install it with:\n"
            "    pip install 'soundbox[spotify]'\n"
            "or:\n"
            "    pip install spotdl"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(output_dir / "{artist} - {title}.{output-ext}")
    args = [
        *cmd,
        "download",
        url,
        "--output",
        output_template,
        *_preset_to_spotdl_args(preset),
    ]

    if not quiet:
        console.print(
            f"[bold cyan]soundbox[/] · spotify → [green]{url}[/] "
            f"→ preset [magenta]{preset.name}[/] → [yellow]{output_dir}[/]"
        )

    return subprocess.call(args)
