# Studio Clock

A studio clock for broadcast radio.

## Now playing

Clock displays can be linked to a now-playing source when creating or editing a
clock. The Solid Radio source is created by the database migration and is
polled by the open display, with its latest song and artwork cached for 30
seconds.
Cover art is looked up from the iTunes Search API when the song changes.
Additional REST sources can be configured in the Django admin using the same
response shape: `isPlayingASong` and a `song` object containing `artist` and
`title`.

## Weather

Each clock can show a two-day forecast for a city or place entered in its
settings. Temperature units (Celsius or Fahrenheit) are configurable per clock.
Forecasts are provided by Open-Meteo, cached by the app for one day, and
refreshed automatically while a clock display remains open. No API key is
required.
