import json
import logging
from datetime import timedelta
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.utils import timezone

from studioclock.models import NowPlayingSource

logger = logging.getLogger(__name__)
REQUEST_TIMEOUT_SECONDS = 3


def _fetch_json(url):
    request = Request(url, headers={"User-Agent": "StudioClock/1.0"})
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.load(response)


def _lookup_artwork(artist, title):
    query = urlencode({"term": f"{artist} {title}", "entity": "song", "limit": 1})
    try:
        results = _fetch_json(f"https://itunes.apple.com/search?{query}").get(
            "results", []
        )
        if results:
            return results[0].get("artworkUrl100", "")
    except URLError, TimeoutError, OSError, ValueError, AttributeError:
        logger.warning(
            "Unable to look up cover art for %s - %s", artist, title, exc_info=True
        )
    return ""


def refresh_now_playing(source: NowPlayingSource) -> NowPlayingSource:
    if not source.enabled:
        return source

    now = timezone.now()
    if source.last_polled_at and now < source.last_polled_at + timedelta(
        seconds=source.poll_interval_seconds
    ):
        return source

    try:
        response = _fetch_json(source.endpoint_url)
        song = response.get("song") or {}
        if not isinstance(song, dict):
            raise TypeError("Now playing response song must be an object")

        is_playing = bool(response.get("isPlayingASong")) and bool(
            song.get("artist") and song.get("title")
        )
        artist = str(song.get("artist", ""))[:255] if is_playing else ""
        title = str(song.get("title", ""))[:255] if is_playing else ""
        changed_song = (artist, title) != (source.artist, source.title)

        artwork_url = ""
        if is_playing:
            artwork_url = song.get("artwork_url") or song.get("artworkUrl") or ""
            if not artwork_url:
                artwork_url = (
                    _lookup_artwork(artist, title)
                    if changed_song or not source.artwork_url
                    else source.artwork_url
                )

        source.artist = artist
        source.title = title
        source.artwork_url = artwork_url
        source.is_playing = is_playing
    except URLError, TimeoutError, OSError, ValueError, AttributeError, TypeError:
        logger.warning(
            "Unable to poll now playing source %s", source.name, exc_info=True
        )

    source.last_polled_at = now
    source.save(
        update_fields=[
            "artist",
            "title",
            "artwork_url",
            "is_playing",
            "last_polled_at",
        ]
    )
    return source
