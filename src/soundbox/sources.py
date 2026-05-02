"""URL → source detection."""

from __future__ import annotations

from enum import Enum
from urllib.parse import urlparse


class Source(str, Enum):
    YOUTUBE = "youtube"
    SOUNDCLOUD = "soundcloud"
    SPOTIFY = "spotify"
    UNKNOWN = "unknown"


_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
    "www.youtu.be",
}

_SOUNDCLOUD_HOSTS = {
    "soundcloud.com",
    "www.soundcloud.com",
    "m.soundcloud.com",
    "on.soundcloud.com",
}

_SPOTIFY_HOSTS = {
    "open.spotify.com",
    "play.spotify.com",
    "spotify.com",
    "www.spotify.com",
}


def detect_source(url: str) -> Source:
    """Return the streaming source backing the given URL.

    Supports plain http(s) URLs as well as `spotify:` URIs.
    """
    if not url:
        return Source.UNKNOWN

    s = url.strip()

    if s.startswith("spotify:"):
        return Source.SPOTIFY

    parsed = urlparse(s)
    host = (parsed.hostname or "").lower()
    if not host:
        return Source.UNKNOWN

    if host in _YOUTUBE_HOSTS:
        return Source.YOUTUBE
    if host in _SOUNDCLOUD_HOSTS:
        return Source.SOUNDCLOUD
    if host in _SPOTIFY_HOSTS:
        return Source.SPOTIFY

    return Source.UNKNOWN
