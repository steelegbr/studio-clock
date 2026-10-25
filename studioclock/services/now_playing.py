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


def lookup_artwork(artist, title):
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
