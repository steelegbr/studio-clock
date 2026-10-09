from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from studioclock.forms.clock import ClockForm
from studioclock.models import Clock, Font, FontWeight, NowPlayingSource
from studioclock.services.weather import weather_payload


class ClockPermissionTests(TestCase):
    def setUp(self):
        self.clock = Clock.objects.create(name="Test Clock")
        self.user = User.objects.create_user(username="clock-user", password="password")
        self.mutation_views = [
            (reverse("clock:create"), "add_clock"),
            (reverse("clock:edit", args=[self.clock.pk]), "change_clock"),
            (reverse("clock:delete", args=[self.clock.pk]), "delete_clock"),
        ]

    def test_clock_list_is_public(self):
        response = self.client.get(reverse("clock:list"))

        self.assertEqual(response.status_code, 200)

    def test_mutation_views_require_login(self):
        for url, _ in self.mutation_views:
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 302)

    def test_mutation_views_require_their_model_permission(self):
        self.client.force_login(self.user)

        for url, codename in self.mutation_views:
            with self.subTest(permission=codename):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

                permission = Permission.objects.get(
                    content_type__app_label="studioclock",
                    codename=codename,
                )
                self.user.user_permissions.add(permission)
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.user.user_permissions.clear()


class ClockRenderTests(TestCase):
    def test_render_uses_clock_colours_and_name_without_logo(self):
        clock = Clock.objects.create(
            name="Studio Clock",
            background_colour="#123456",
            foreground_colour="#ABCDEF",
        )

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertRegex(
            response.content.decode(),
            r'style="background-color: #123456;\s*color: #ABCDEF"',
        )
        self.assertContains(
            response,
            '<span class="clock-branding-name">Studio Clock</span>',
            html=True,
        )
        self.assertNotContains(response, "clock-branding-logo")

    def test_render_loads_and_applies_selected_font_and_weight(self):
        font = Font.objects.create(name="Share Tech Mono", family="Share Tech Mono")
        weight = FontWeight.objects.create(font=font, weight=700, name="Bold")
        clock = Clock.objects.create(name="Studio Clock", font=weight)

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(
            response,
            "https://fonts.googleapis.com/css2?family=Share%20Tech%20Mono:wght@700&display=swap",
        )
        self.assertRegex(
            response.content.decode(),
            r"font-family: 'Share Tech Mono';\s*font-weight: 700",
        )

    def test_render_displays_clock_logo_when_present(self):
        clock = Clock.objects.create(name="Studio Clock")
        Clock.objects.filter(pk=clock.pk).update(logo="logos/studio-clock.png")

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(response, 'class="clock-branding-logo"')
        self.assertNotContains(response, "clock-branding-name")

    @patch(
        "studioclock.services.now_playing._lookup_artwork",
        return_value="https://art.example/cover.jpg",
    )
    @patch(
        "studioclock.services.now_playing._fetch_json",
        return_value={
            "isPlayingASong": True,
            "song": {"artist": "Bon Jovi", "title": "Livin' on a Prayer"},
        },
    )
    def test_render_displays_cached_now_playing_song_and_artwork(
        self, fetch_json, lookup_artwork
    ):
        source = NowPlayingSource.objects.create(
            name="Test Radio",
            endpoint_url="https://radio.example/nowplaying",
        )
        clock = Clock.objects.create(name="Studio Clock", now_playing_source=source)

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(response, "Bon Jovi")
        self.assertContains(response, "Livin&#x27; on a Prayer")
        self.assertContains(response, 'src="https://art.example/cover.jpg"')
        fetch_json.assert_called_once_with(source.endpoint_url)
        lookup_artwork.assert_called_once_with("Bon Jovi", "Livin' on a Prayer")

    @patch("studioclock.services.now_playing._fetch_json")
    def test_now_playing_is_not_polled_until_cache_expires(self, fetch_json):
        source = NowPlayingSource.objects.create(
            name="Test Radio",
            endpoint_url="https://radio.example/nowplaying",
            artist="Bon Jovi",
            title="Livin' on a Prayer",
            is_playing=True,
            last_polled_at=timezone.now() - timedelta(seconds=10),
        )
        clock = Clock.objects.create(name="Studio Clock", now_playing_source=source)

        response = self.client.get(reverse("clock:render", args=[clock.pk]))

        self.assertContains(response, "Bon Jovi")
        fetch_json.assert_not_called()

    @patch(
        "studioclock.services.now_playing._lookup_artwork",
        return_value="https://art.example/cover.jpg",
    )
    @patch(
        "studioclock.services.now_playing._fetch_json",
        return_value={
            "isPlayingASong": True,
            "song": {"artist": "Bon Jovi", "title": "Livin' on a Prayer"},
        },
    )
    def test_now_playing_status_endpoint_returns_source_data(
        self, fetch_json, lookup_artwork
    ):
        source = NowPlayingSource.objects.create(
            name="Test Radio",
            endpoint_url="https://radio.example/nowplaying",
        )
        clock = Clock.objects.create(name="Studio Clock", now_playing_source=source)

        response = self.client.get(reverse("clock:now-playing", args=[clock.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "is_playing": True,
                "artist": "Bon Jovi",
                "title": "Livin' on a Prayer",
                "artwork_url": "https://art.example/cover.jpg",
                "poll_interval_seconds": 30,
            },
        )
        fetch_json.assert_called_once_with(source.endpoint_url)
        lookup_artwork.assert_called_once_with("Bon Jovi", "Livin' on a Prayer")


class ClockUploadFormTests(TestCase):
    def test_create_and_edit_forms_use_multipart_encoding(self):
        user = User.objects.create_superuser(
            username="clock-admin",
            password="password",
        )
        self.client.force_login(user)
        clock = Clock.objects.create(name="Studio Clock")

        for url in (
            reverse("clock:create"),
            reverse("clock:edit", args=[clock.pk]),
        ):
            with self.subTest(url=url):
                self.assertContains(
                    self.client.get(url),
                    'enctype="multipart/form-data"',
                )


class WeatherTests(TestCase):
    def setUp(self):
        self.clock = Clock.objects.create(
            name="Weather Clock",
            weather_location="London",
            weather_units=Clock.WeatherUnits.FAHRENHEIT,
        )

    @patch(
        "studioclock.services.weather._fetch_json",
        side_effect=[
            {"results": [{"latitude": 51.5, "longitude": -0.1}]},
            {
                "daily": {
                    "time": ["2026-10-09", "2026-10-10"],
                    "weather_code": [2, 61],
                    "temperature_2m_max": [60.8, 55.4],
                    "temperature_2m_min": [48.2, 44.6],
                }
            },
        ],
    )
    def test_weather_endpoint_geocodes_and_returns_two_day_forecast(self, fetch_json):
        response = self.client.get(reverse("clock:weather", args=[self.clock.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "available": True,
                "location": "London",
                "unit": "°F",
                "days": [
                    {
                        "label": "Today",
                        "date": "2026-10-09",
                        "condition": "Partly cloudy",
                        "icon": "bi-cloud-sun-fill",
                        "high": 60.8,
                        "low": 48.2,
                    },
                    {
                        "label": "Tomorrow",
                        "date": "2026-10-10",
                        "condition": "Light rain",
                        "icon": "bi-cloud-rain-fill",
                        "high": 55.4,
                        "low": 44.6,
                    },
                ],
                "poll_interval_seconds": 86400,
            },
        )
        self.assertEqual(fetch_json.call_count, 2)
        self.assertIn("temperature_unit=fahrenheit", fetch_json.call_args.args[0])

    @patch("studioclock.services.weather._fetch_json")
    def test_forecast_is_cached_for_one_day(self, fetch_json):
        self.clock.weather_latitude = 51.5
        self.clock.weather_longitude = -0.1
        self.clock.weather_forecast = [
            {
                "label": "Today",
                "date": "2026-10-09",
                "condition": "Clear sky",
                "icon": "bi-sun-fill",
                "high": 18,
                "low": 9,
            },
            {
                "label": "Tomorrow",
                "date": "2026-10-10",
                "condition": "Overcast",
                "icon": "bi-cloud-fill",
                "high": 15,
                "low": 8,
            },
        ]
        self.clock.weather_last_polled_at = timezone.now() - timedelta(hours=12)
        self.clock.save()

        payload = weather_payload(self.clock)

        self.assertTrue(payload["available"])
        self.assertEqual(payload["days"][0]["condition"], "Clear sky")
        fetch_json.assert_not_called()

    def test_location_and_units_are_configurable_on_clock_form(self):
        form = ClockForm()

        self.assertIn("weather_location", form.fields)
        self.assertIn("weather_units", form.fields)
        self.assertEqual(
            form.fields["weather_units"].choices,
            list(Clock.WeatherUnits.choices),
        )

    def test_changing_location_clears_cached_forecast_and_coordinates(self):
        self.clock.weather_latitude = 51.5
        self.clock.weather_longitude = -0.1
        self.clock.weather_forecast = [{"label": "Today"}]
        self.clock.weather_last_polled_at = timezone.now()
        self.clock.save()

        initial_form = ClockForm(instance=self.clock)
        data = initial_form.initial.copy()
        data["weather_location"] = "Edinburgh"
        form = ClockForm(data=data, instance=self.clock)

        self.assertTrue(form.is_valid(), form.errors)
        clock = form.save()

        self.assertIsNone(clock.weather_latitude)
        self.assertIsNone(clock.weather_longitude)
        self.assertEqual(clock.weather_forecast, [])
        self.assertIsNone(clock.weather_last_polled_at)

    def test_changing_units_with_update_fields_clears_cached_forecast(self):
        self.clock.weather_latitude = 51.5
        self.clock.weather_longitude = -0.1
        self.clock.weather_forecast = [{"label": "Today"}]
        self.clock.weather_last_polled_at = timezone.now()
        self.clock.save()

        self.clock.weather_units = Clock.WeatherUnits.CELSIUS
        self.clock.save(update_fields=["weather_units"])
        self.clock.refresh_from_db()

        self.assertEqual(self.clock.weather_units, Clock.WeatherUnits.CELSIUS)
        self.assertIsNone(self.clock.weather_latitude)
        self.assertIsNone(self.clock.weather_longitude)
        self.assertEqual(self.clock.weather_forecast, [])
        self.assertIsNone(self.clock.weather_last_polled_at)

    def test_render_includes_cached_forecast(self):
        self.clock.weather_forecast = [
            {
                "label": "Today",
                "date": "2026-10-09",
                "condition": "Clear sky",
                "icon": "bi-sun-fill",
                "high": 18,
                "low": 9,
            },
            {
                "label": "Tomorrow",
                "date": "2026-10-10",
                "condition": "Rain",
                "icon": "bi-cloud-rain-fill",
                "high": 15,
                "low": 8,
            },
        ]
        self.clock.weather_last_polled_at = timezone.now()
        self.clock.save()

        response = self.client.get(reverse("clock:render", args=[self.clock.pk]))

        self.assertContains(response, "London")
        self.assertContains(response, "Clear sky")
        self.assertContains(response, "Tomorrow")
        self.assertContains(response, "Weather data by")
