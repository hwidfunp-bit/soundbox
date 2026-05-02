"""Click-based CLI for soundbox."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from soundbox import __version__
from soundbox.presets import DEFAULT_PRESET, get_preset, list_preset_names
from soundbox.sources import Source, detect_source

console = Console()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, prog_name="soundbox")
def main() -> None:
    """soundbox — download audio/video from YouTube, SoundCloud and Spotify."""


@main.command("download")
@click.argument("url", required=True)
@click.option(
    "-q",
    "--quality",
    "preset_name",
    default=DEFAULT_PRESET,
    show_default=True,
    type=click.Choice(list_preset_names(), case_sensitive=False),
    help="Quality preset to use.",
)
@click.option(
    "-o",
    "--output",
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path("downloads"),
    show_default=True,
    help="Directory to write downloaded files into.",
)
@click.option(
    "--playlist/--no-playlist",
    default=False,
    help="If the URL points at a playlist, download every entry (yt-dlp/SoundCloud only).",
)
@click.option("--quiet", is_flag=True, help="Suppress progress output.")
def download(
    url: str,
    preset_name: str,
    output_dir: Path,
    playlist: bool,
    quiet: bool,
) -> None:
    """Download URL using the chosen quality preset."""
    preset = get_preset(preset_name)
    src = detect_source(url)

    if src is Source.UNKNOWN:
        console.print(
            f"[red]error:[/] could not recognise the source for [bold]{url}[/]. "
            "Supported: YouTube, SoundCloud, Spotify."
        )
        sys.exit(2)

    if src in (Source.YOUTUBE, Source.SOUNDCLOUD):
        from soundbox import ytdlp_backend

        rc = ytdlp_backend.download(
            url,
            preset,
            output_dir,
            download_playlist=playlist,
            quiet=quiet,
        )
    else:  # Spotify
        from soundbox import spotify_backend

        rc = spotify_backend.download(url, preset, output_dir, quiet=quiet)

    if rc != 0:
        console.print(f"[red]download failed[/] (exit code {rc})")
        sys.exit(rc)
    if not quiet:
        console.print(f"[bold green]done[/] → {output_dir}")


@main.command("info")
@click.argument("url")
def info_cmd(url: str) -> None:
    """Print metadata for URL without downloading."""
    src = detect_source(url)
    console.print(f"source: [cyan]{src.value}[/]")

    if src in (Source.YOUTUBE, Source.SOUNDCLOUD):
        from soundbox import ytdlp_backend

        meta = ytdlp_backend.info(url)
        for key in ("title", "uploader", "duration", "view_count", "webpage_url"):
            if key in meta:
                console.print(f"{key}: {meta[key]}")
    elif src is Source.SPOTIFY:
        console.print("[yellow]info: spotify metadata lookup not yet implemented[/]")
    else:
        console.print("[red]error:[/] unknown source.")
        sys.exit(2)


@main.command("presets")
def presets_cmd() -> None:
    """List available quality presets."""
    table = Table(title="soundbox presets")
    table.add_column("name", style="cyan")
    table.add_column("codec", style="magenta")
    table.add_column("bitrate", style="green")
    table.add_column("video", style="yellow")
    from soundbox.presets import PRESETS

    for preset in PRESETS.values():
        table.add_row(
            preset.name,
            preset.codec or "—",
            f"{preset.bitrate_kbps} kbps" if preset.bitrate_kbps else "—",
            "yes" if preset.is_video else "no",
        )
    console.print(table)


if __name__ == "__main__":
    main()
