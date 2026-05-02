# soundbox

`soundbox` is a small command-line tool that wraps [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [spotdl](https://github.com/spotDL/spotify-downloader) behind a single interface, with sane quality presets and automatic source detection.

It supports:

- **YouTube** (incl. `youtu.be`, `music.youtube.com`, `m.youtube.com`)
- **SoundCloud** (incl. `on.soundcloud.com`)
- **Spotify** (via `spotdl` — Spotify metadata + audio downloaded from YouTube, since Spotify itself is DRM-protected)

## Features

- One CLI for all three sources.
- Quality presets: `mp3-320`, `mp3-192`, `mp3-128`, `m4a`, `opus`, `flac`, `best-audio`, `best-video`.
- Automatic source detection from the URL (no flags needed).
- Embeds cover art and metadata via FFmpeg postprocessors.
- Playlist mode for YouTube/SoundCloud, with `Playlist/NN - Title` filenames.
- Standard `yt-dlp` retry / concurrent-fragment behaviour out of the box.

## Install

Requirements: **Python 3.10+** and **ffmpeg** on PATH.

```bash
# from a clone of this repo
pip install .

# with Spotify support
pip install '.[spotify]'

# with dev tooling
pip install -e '.[dev]'
```

`ffmpeg` install hints:

- macOS (Homebrew): `brew install ffmpeg`
- Debian / Ubuntu: `sudo apt-get install ffmpeg`
- Windows (winget): `winget install Gyan.FFmpeg`

## Usage

```bash
# Default: mp3-320 into ./downloads
soundbox download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Pick a preset
soundbox download "https://soundcloud.com/forss/flickermood" -q opus

# Download a YouTube playlist
soundbox download "https://www.youtube.com/playlist?list=PL..." --playlist -q mp3-192

# Spotify (requires `pip install '.[spotify]'`)
soundbox download "https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC"

# Custom output directory + best-quality video
soundbox download "https://youtu.be/dQw4w9WgXcQ" -q best-video -o ~/Videos/clips

# List presets
soundbox presets

# Get metadata only (no download)
soundbox info "https://youtu.be/dQw4w9WgXcQ"
```

### Available presets

| name         | codec | bitrate   | video |
|--------------|-------|-----------|-------|
| `mp3-320`    | mp3   | 320 kbps  | no    |
| `mp3-192`    | mp3   | 192 kbps  | no    |
| `mp3-128`    | mp3   | 128 kbps  | no    |
| `m4a`        | m4a   | source    | no    |
| `opus`       | opus  | source    | no    |
| `flac`       | flac  | lossless  | no    |
| `best-audio` | —     | source    | no    |
| `best-video` | —     | source    | yes   |

## Development

```bash
git clone https://github.com/hwidfunp-bit/soundbox.git
cd soundbox
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev,spotify]'

ruff check .
pytest -q
```

## How it works

| URL host                                | Backend           |
|-----------------------------------------|-------------------|
| `youtube.com`, `youtu.be`, `music.youtube.com` | `yt-dlp`     |
| `soundcloud.com`, `on.soundcloud.com`   | `yt-dlp`          |
| `open.spotify.com`, `spotify:` URIs     | `spotdl` (which itself uses YouTube as the audio source) |

`soundbox` translates its preset into the right `yt-dlp` format expression / postprocessor chain, or the right `spotdl` flags. The same preset name therefore works regardless of which source you're downloading from.

## Notes

- **Spotify is not DRM-broken** by this tool. It works the same way `spotdl` works: matches each Spotify track to a YouTube/YouTube Music search result and downloads that.
- Always respect the terms of service of the platforms you're downloading from. This tool is intended for content you have the right to download (your own uploads, public-domain works, content explicitly licensed for download, etc.).
