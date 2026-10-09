function clearCanvas(canvas, backgroundColour) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    ctx.clearRect(0, 0, width, height);

    if (backgroundColour) {
        ctx.fillStyle = backgroundColour;
        ctx.fillRect(0, 0, width, height);
    }
}

const LED_FONT = {
    '0': ['01110', '10001', '10011', '10101', '11001', '10001', '01110'],
    '1': ['00100', '01100', '00100', '00100', '00100', '00100', '01110'],
    '2': ['01110', '10001', '00001', '00010', '00100', '01000', '11111'],
    '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
    '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'],
    '5': ['11111', '10000', '10000', '11110', '00001', '00001', '11110'],
    '6': ['01110', '10000', '10000', '11110', '10001', '10001', '01110'],
    '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
    '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'],
    '9': ['01110', '10001', '10001', '01111', '00001', '00001', '01110'],
    ':': ['00000', '00100', '00100', '00000', '00100', '00100', '00000'],
};

function drawLed(ctx, x, y, colour, dotRadius, opacity = 1, glowRadius = dotRadius * 4) {
    const glow = ctx.createRadialGradient(x, y, dotRadius * 0.4, x, y, glowRadius);
    glow.addColorStop(0, colour);
    glow.addColorStop(0.25, colour);
    glow.addColorStop(1, 'transparent');

    ctx.globalAlpha = opacity;
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, glowRadius, 0, 2 * Math.PI);
    ctx.fill();

    ctx.fillStyle = colour;
    ctx.beginPath();
    ctx.arc(x, y, dotRadius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.globalAlpha = 1;
}

function renderLedFives(canvas, boxSize, colour = 'red', dotRadius = 3) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const ringSpacing = Math.min(dotRadius * 24, boxSize / 8);
    const radius = boxSize / 2 - ringSpacing;

    for (let i = 0; i < 12; i++) {
        const angle = (i * 30) * Math.PI / 180; // Convert degrees to radians
        const x = (width / 2) + radius * Math.cos(angle);
        const y = (height / 2) + radius * Math.sin(angle);

        drawLed(ctx, x, y, colour, dotRadius);
    }
}

function renderLedSeconds(canvas, boxSize, colour = 'red', dotRadius = 3, now = new Date()) {
    const ctx = canvas.getContext('2d');
    const seconds = now.getSeconds();
    const secondProgress = now.getMilliseconds() / 1000;
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const ringSpacing = Math.min(dotRadius * 24, boxSize / 8);
    const radius = boxSize / 2 - ringSpacing * 1.6;

    for (let i = 0; i < seconds; i++) {
        const angle = (i * 6 - 90) * Math.PI / 180; // Convert degrees to radians

        const x = (width / 2) + radius * Math.cos(angle);
        const y = (height / 2) + radius * Math.sin(angle);

        drawLed(ctx, x, y, colour, dotRadius);
    }

    const angle = (seconds * 6 - 90) * Math.PI / 180;
    const x = (width / 2) + radius * Math.cos(angle);
    const y = (height / 2) + radius * Math.sin(angle);
    drawLed(ctx, x, y, colour, dotRadius, secondProgress);
}

function renderDigitalTime(canvas, boxSize, now, colour = 'red', dotRadius = 3) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const time = [now.getHours(), now.getMinutes(), now.getSeconds()]
        .map((value) => String(value).padStart(2, '0'))
        .join(':');
    const columns = time.length * 5 + time.length - 1;
    const ringSpacing = Math.min(dotRadius * 24, boxSize / 8);
    const innerRadius = boxSize / 2 - ringSpacing * 1.85;
    const pitch = Math.min(dotRadius * 4.5, (innerRadius * 1.5) / columns);
    const textWidth = (columns - 1) * pitch;
    const textHeight = 6 * pitch;
    const startX = width / 2 - textWidth / 2;
    const startY = height / 2 - textHeight / 2;
    const textDotRadius = Math.min(dotRadius * 1.5, pitch / 3);

    for (let characterIndex = 0; characterIndex < time.length; characterIndex++) {
        const glyph = LED_FONT[time[characterIndex]];

        for (let row = 0; row < glyph.length; row++) {
            for (let column = 0; column < glyph[row].length; column++) {
                if (glyph[row][column] !== '1') {
                    continue;
                }

                const x = startX + (characterIndex * 6 + column) * pitch;
                const y = startY + row * pitch;
                const glowRadius = Math.min(textDotRadius * 4, pitch * .8);
                drawLed(ctx, x, y, colour, textDotRadius, 1, glowRadius);
            }
        }
    }
}

function syncCanvasSize(canvas) {
    const rect = canvas.getBoundingClientRect();
    const pixelRatio = window.devicePixelRatio || 1;
    const width = Math.round(rect.width * pixelRatio);
    const height = Math.round(rect.height * pixelRatio);

    if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
    }

    canvas.getContext('2d').setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
}

function renderLedClock() {
    const canvas = document.getElementById('clock-canvas');
    syncCanvasSize(canvas);
    clearCanvas(canvas, clockSettings.led_background_colour);

    const boxSize = Math.min(canvas.width, canvas.height) / window.devicePixelRatio;
    const now = new Date();
    const dotRadius = boxSize * 0.004;
    renderLedFives(canvas, boxSize, clockSettings.led_colour, dotRadius);
    renderLedSeconds(canvas, boxSize, clockSettings.led_colour, dotRadius, now);
    renderDigitalTime(canvas, boxSize, now, clockSettings.led_colour, dotRadius);

    requestAnimationFrame(renderLedClock);
}

function renderSweepingStrokes(canvas, boxSize) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const ringSpacing = boxSize / 12;
    const radius = boxSize / 2 - ringSpacing;

    for (let i = 0; i < 60; i++) {
        const isHourMark = i % 5 === 0;
        const angle = (i * 6 - 90) * Math.PI / 180;
        const x1 = (width / 2) + radius * Math.cos(angle);
        const y1 = (height / 2) + radius * Math.sin(angle);
        const tickLength = isHourMark ? ringSpacing * 0.5 : ringSpacing * 0.22;
        const x2 = (width / 2) + (radius - tickLength) * Math.cos(angle);
        const y2 = (height / 2) + (radius - tickLength) * Math.sin(angle);

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineWidth = isHourMark ? 2 : 1;
        ctx.strokeStyle = clockSettings.sweeping_stroke_colour;
        ctx.stroke();
    }
}

function renderSweepingClockFace(canvas, boxSize) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    
    ctx.beginPath();
    ctx.arc(width / 2, height / 2, boxSize * .45, 0, 2 * Math.PI);
    ctx.fillStyle = clockSettings.sweeping_background_colour;
    ctx.fill();
}

function renderSweepingClockHands(canvas, boxSize, now) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const ringSpacing = boxSize / 10;
    const radius = boxSize / 2 - ringSpacing;

    const hour = now.getHours() % 12 + now.getMinutes() / 60;
    const minute = now.getMinutes() + now.getSeconds() / 60;
    const second = now.getSeconds() + now.getMilliseconds() / 1000;

    const hourAngle = (hour * 30 - 90) * Math.PI / 180; // Convert degrees to radians
    const minuteAngle = (minute * 6 - 90) * Math.PI / 180; // Convert degrees to radians
    const secondAngle = (second * 6 - 90) * Math.PI / 180; // Convert degrees to radians

    // Hour hand
    const hourX = (width / 2) + (radius * 0.5) * Math.cos(hourAngle);
    const hourY = (height / 2) + (radius * 0.5) * Math.sin(hourAngle);
    ctx.beginPath();
    ctx.moveTo(width / 2, height / 2);
    ctx.lineTo(hourX, hourY);
    ctx.lineWidth = 12;
    ctx.strokeStyle = clockSettings.sweeping_hour_hand_colour;
    ctx.stroke();

    // Minute hand
    const minuteX = (width / 2) + (radius * 0.75) * Math.cos(minuteAngle);
    const minuteY = (height / 2) + (radius * 0.75) * Math.sin(minuteAngle);
    ctx.beginPath();
    ctx.moveTo(width / 2, height / 2);
    ctx.lineTo(minuteX, minuteY);
    ctx.lineWidth = 8;
    ctx.strokeStyle = clockSettings.sweeping_minute_hand_colour;
    ctx.stroke();

    // Second hand
    const secondX = (width / 2) + radius * Math.cos(secondAngle);
    const secondY = (height / 2) + radius * Math.sin(secondAngle);
    const secondTailX = (width / 2) - (radius * 0.12) * Math.cos(secondAngle);
    const secondTailY = (height / 2) - (radius * 0.12) * Math.sin(secondAngle);
    ctx.beginPath();
    ctx.moveTo(secondTailX, secondTailY);
    ctx.lineTo(secondX, secondY);
    ctx.lineWidth = 4;
    ctx.strokeStyle = clockSettings.sweeping_second_hand_colour;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(width / 2, height / 2, ringSpacing * 0.18, 0, 2 * Math.PI);
    ctx.fillStyle = clockSettings.sweeping_second_hand_colour;
    ctx.fill();
}

function renderSweepingClock() {
    const canvas = document.getElementById('clock-canvas');
    syncCanvasSize(canvas);
    clearCanvas(canvas, null);

    const boxSize = Math.min(canvas.width, canvas.height) / window.devicePixelRatio;
    renderSweepingClockFace(canvas, boxSize);
    renderSweepingStrokes(canvas, boxSize);
    renderSweepingClockHands(canvas, boxSize, new Date());

    requestAnimationFrame(renderSweepingClock);
}

const TIME_NUMBER_WORDS = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen',
];
const TIME_HOUR_WORDS = [
    'twelve', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
    'nine', 'ten', 'eleven',
];

function numberToWords(number) {
    if (number < 20) {
        return TIME_NUMBER_WORDS[number];
    }

    const remainder = number % 10;
    return `twenty${remainder ? ` ${TIME_NUMBER_WORDS[remainder]}` : ''}`;
}

function getSpokenTime(now) {
    const minutes = now.getMinutes();
    const hour = TIME_HOUR_WORDS[now.getHours() % 12];
    const nextHour = TIME_HOUR_WORDS[(now.getHours() + 1) % 12];

    if (minutes === 0) {
        return `${hour[0].toUpperCase()}${hour.slice(1)} o'clock`;
    }
    if (minutes === 15) {
        return `Quarter past ${hour}`;
    }
    if (minutes === 30) {
        return `Half past ${hour}`;
    }
    if (minutes === 45) {
        return `Quarter to ${nextHour}`;
    }

    const isPast = minutes < 30;
    const minuteCount = isPast ? minutes : 60 - minutes;
    const minuteUnit = minuteCount === 1 ? 'minute' : 'minutes';
    const direction = isPast ? 'past' : 'to';
    const targetHour = isPast ? hour : nextHour;
    const minuteWords = numberToWords(minuteCount);

    return `${minuteWords[0].toUpperCase()}${minuteWords.slice(1)} ${minuteUnit} ${direction} ${targetHour}`;
}

function renderTimeText() {
    const timeDisplay = document.getElementById('time-display');
    if (!timeDisplay) {
        return;
    }

    const now = new Date();
    timeDisplay.textContent = getSpokenTime(now);
    const millisecondsUntilNextMinute = (60 - now.getSeconds()) * 1000 - now.getMilliseconds();
    window.setTimeout(renderTimeText, millisecondsUntilNextMinute);
}

function updateNowPlaying(data) {
    const widget = document.querySelector('.clock-now-playing');
    if (!widget) {
        return;
    }

    widget.replaceChildren();
    if (!data.is_playing) {
        const idleMessage = document.createElement('div');
        idleMessage.className = 'now-playing-idle';
        idleMessage.textContent = 'Nothing playing';
        widget.append(idleMessage);
        return;
    }

    if (data.artwork_url) {
        const artwork = document.createElement('img');
        artwork.className = 'now-playing-artwork';
        artwork.src = data.artwork_url;
        artwork.alt = `Cover art for ${data.title} by ${data.artist}`;
        widget.append(artwork);
    } else {
        const placeholder = document.createElement('div');
        placeholder.className = 'now-playing-artwork now-playing-artwork-placeholder';
        placeholder.setAttribute('aria-hidden', 'true');
        const icon = document.createElement('i');
        icon.className = 'bi bi-disc';
        placeholder.append(icon);
        widget.append(placeholder);
    }

    const details = document.createElement('div');
    details.className = 'now-playing-details';
    const label = document.createElement('div');
    label.className = 'now-playing-label';
    label.textContent = 'NOW PLAYING';
    const title = document.createElement('div');
    title.className = 'now-playing-title';
    title.textContent = data.title;
    const artist = document.createElement('div');
    artist.className = 'now-playing-artist';
    artist.textContent = data.artist;
    details.append(label, title, artist);
    widget.append(details);
}

async function pollNowPlaying() {
    const widget = document.querySelector('.clock-now-playing[data-status-url]');
    if (!widget) {
        return;
    }

    let interval = 30_000;
    try {
        const response = await fetch(widget.dataset.statusUrl, {
            headers: { Accept: 'application/json' },
            cache: 'no-store',
        });
        if (!response.ok) {
            throw new Error(`Now playing request failed: ${response.status}`);
        }
        const data = await response.json();
        updateNowPlaying(data);
        interval = Math.max(5, data.poll_interval_seconds) * 1000;
    } catch (error) {
        console.error('Unable to update now playing display', error);
    }
    window.setTimeout(pollNowPlaying, interval);
}

const clockSettings = JSON.parse(document.getElementById('clock-settings').textContent);
renderTimeText();
pollNowPlaying();

switch (clockSettings.clock_type) {
    case 'LED':
        requestAnimationFrame(renderLedClock);
        break;
    case 'SWEEPING':
        requestAnimationFrame(renderSweepingClock);
        break;
    default:
        console.error('Unknown clock type:', clockSettings.clock_type);
}