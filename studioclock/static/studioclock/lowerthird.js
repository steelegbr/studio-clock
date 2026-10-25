(() => {
    "use strict";

    const POLL_INTERVAL_MS = 1000;

    function initialiseLowerThird() {
        const lowerThird = document.getElementById("lower-third");

        if (!lowerThird) {
            return;
        }

        const fontFamily = lowerThird.dataset.fontFamily;
        const fontWeight = lowerThird.dataset.fontWeight;

        if (fontFamily) {
            lowerThird.style.setProperty(
                "--lower-third-font",
                `"${fontFamily}", sans-serif`,
            );
        }

        if (fontWeight) {
            lowerThird.style.setProperty(
                "--lower-third-font-weight",
                fontWeight,
            );
        }

        const apiUrl = lowerThird.dataset.apiUrl;
        const titleElement = lowerThird.querySelector("[data-song-title]");
        const artistElement = lowerThird.querySelector("[data-song-artist]");

        if (!apiUrl || !titleElement || !artistElement) {
            console.error("Lower third is missing required configuration.");
            return;
        }

        let lastSongKey = null;

        async function update() {
            try {
                const response = await fetch(apiUrl, {
                    cache: "no-store",
                    headers: {
                        "Accept": "application/json",
                    },
                });

                if (!response.ok) {
                    throw new Error(`Now Playing request failed: ${response.status}`);
                }

                const data = await response.json();
                const song = data.song;

                if (song) {
                    const songKey = JSON.stringify([
                        song.artist ?? "",
                        song.title ?? "",
                        song.year ?? null,
                    ]);

                    if (songKey !== lastSongKey) {
                        titleElement.textContent = song.title ?? "";
                        artistElement.textContent =
                            (song.artist ?? "") +
                            (song.year ? ` (${song.year})` : "");

                        lastSongKey = songKey;
                    }

                    lowerThird.classList.replace(
                        "lower-third--off",
                        "lower-third--on",
                    );
                } else {
                    lowerThird.classList.replace(
                        "lower-third--on",
                        "lower-third--off",
                    );
                }
            } catch (error) {
                console.error("Unable to update lower third:", error);
            } finally {
                window.setTimeout(update, POLL_INTERVAL_MS);
            }
        }

        update();
    }

    document.addEventListener("DOMContentLoaded", initialiseLowerThird);
})();