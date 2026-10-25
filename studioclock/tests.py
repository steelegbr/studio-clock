from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from studioclock.models import Clock, Song, SongPlay, Station


class ClockNowPlayingTests(TestCase):
    def setUp(self):
        self.station = Station.objects.create(name="Test Radio")
        self.clock = Clock.objects.create(
            name="Studio Clock",
            station=self.station,
        )

    def create_song_play(self, artist, title, timestamp=None):
        song = Song.objects.create(
            artist=artist,
            title=title,
            artwork_url="https://art.example/cover.jpg",
        )

        return SongPlay.objects.create(
            station=self.station,
            song=song,
            timestamp=timestamp or timezone.now(),
        )

    def test_now_playing_endpoint_returns_latest_song(self):
        self.create_song_play(
            "Queen",
            "Don't Stop Me Now",
            timezone.now() - timedelta(minutes=5),
        )
        self.create_song_play(
            "Bon Jovi",
            "Livin' on a Prayer",
        )

        response = self.client.get(
            reverse("clock_api:now-playing", args=[self.clock.pk])
        )

        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["artist"], "Bon Jovi")
        self.assertEqual(payload["title"], "Livin' on a Prayer")
        self.assertEqual(
            payload["artwork_url"],
            "https://art.example/cover.jpg",
        )

    def test_now_playing_is_scoped_to_the_clocks_station(self):
        other_station = Station.objects.create(name="Other Radio")
        other_song = Song.objects.create(
            artist="The Beatles",
            title="Hey Jude",
            artwork_url="https://art.example/beatles.jpg",
        )
        SongPlay.objects.create(
            station=other_station,
            song=other_song,
            timestamp=timezone.now(),
        )

        self.create_song_play("Bon Jovi", "Livin' on a Prayer")

        response = self.client.get(
            reverse("clock_api:now-playing", args=[self.clock.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["artist"], "Bon Jovi")
