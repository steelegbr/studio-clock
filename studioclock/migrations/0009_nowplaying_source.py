import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

SOURCE_ID = uuid.UUID("f3f2a30e-4b54-4bc7-b30b-1e6961c76320")


def create_solid_radio_source(apps, schema_editor):
    NowPlayingSource = apps.get_model("studioclock", "NowPlayingSource")
    Clock = apps.get_model("studioclock", "Clock")
    source = NowPlayingSource.objects.create(
        id=SOURCE_ID,
        name="Solid Radio",
        endpoint_url="https://nowplaying.solidradio.co.uk/api/station/Solid%20Radio/nowplaying",
    )
    Clock.objects.filter(now_playing_source__isnull=True).update(
        now_playing_source=source
    )


def remove_solid_radio_source(apps, schema_editor):
    NowPlayingSource = apps.get_model("studioclock", "NowPlayingSource")
    Clock = apps.get_model("studioclock", "Clock")
    Clock.objects.filter(now_playing_source_id=SOURCE_ID).update(
        now_playing_source=None
    )
    NowPlayingSource.objects.filter(id=SOURCE_ID).delete()


class Migration(migrations.Migration):
    dependencies = [("studioclock", "0008_font_fontweight_clock_font")]

    operations = [
        migrations.CreateModel(
            name="NowPlayingSource",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("endpoint_url", models.URLField()),
                (
                    "poll_interval_seconds",
                    models.PositiveSmallIntegerField(
                        default=30,
                        validators=[django.core.validators.MinValueValidator(5)],
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("artist", models.CharField(blank=True, max_length=255)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("artwork_url", models.URLField(blank=True)),
                ("is_playing", models.BooleanField(default=False)),
                (
                    "last_polled_at",
                    models.DateTimeField(blank=True, null=True),
                ),
            ],
            options={
                "verbose_name": "Now Playing Source",
                "verbose_name_plural": "Now Playing Sources",
                "ordering": ["name"],
            },
        ),
        migrations.AddField(
            model_name="clock",
            name="now_playing_source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="clocks",
                to="studioclock.nowplayingsource",
            ),
        ),
        migrations.RunPython(create_solid_radio_source, remove_solid_radio_source),
    ]
