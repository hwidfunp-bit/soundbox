import pytest

from soundbox.sources import Source, detect_source


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", Source.YOUTUBE),
        ("https://youtu.be/dQw4w9WgXcQ", Source.YOUTUBE),
        ("https://music.youtube.com/watch?v=dQw4w9WgXcQ", Source.YOUTUBE),
        ("https://m.youtube.com/watch?v=dQw4w9WgXcQ", Source.YOUTUBE),
        ("https://soundcloud.com/forss/flickermood", Source.SOUNDCLOUD),
        ("https://on.soundcloud.com/abcdef", Source.SOUNDCLOUD),
        ("https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC", Source.SPOTIFY),
        ("spotify:track:4uLU6hMCjMI75M1A2tKUQC", Source.SPOTIFY),
        ("https://example.com/song", Source.UNKNOWN),
        ("not a url", Source.UNKNOWN),
        ("", Source.UNKNOWN),
    ],
)
def test_detect_source(url: str, expected: Source) -> None:
    assert detect_source(url) is expected
