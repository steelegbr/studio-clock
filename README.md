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
