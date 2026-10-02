function clearCanvas(canvas, backgroundColour) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = backgroundColour;
    ctx.fillRect(0, 0, width, height);
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

function renderFives(canvas, boxSize, colour = 'red', dotRadius = 3) {
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

function renderSeconds(canvas, boxSize, colour = 'red', dotRadius = 3, now = new Date()) {
    const ctx = canvas.getContext('2d');
    const seconds = now.getSeconds();
    const secondProgress = now.getMilliseconds() / 1000;
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const ringSpacing = Math.min(dotRadius * 24, boxSize / 8);
    const radius = boxSize / 2 - ringSpacing * 2;

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

function renderDigitalTime(canvas, boxSize, now, colour = 'red', dotRadius = 3, fontScale = 1.5) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    const time = [now.getHours(), now.getMinutes(), now.getSeconds()]
        .map((value) => String(value).padStart(2, '0'))
        .join(':');
    const columns = time.length * 5 + time.length - 1;
    const ringSpacing = Math.min(dotRadius * 24, boxSize / 8);
    const innerRadius = boxSize / 2 - ringSpacing * 2;
    const pitch = Math.min(dotRadius * 3 * fontScale, (innerRadius * 1.5) / columns);
    const textWidth = (columns - 1) * pitch;
    const textHeight = 6 * pitch;
    const startX = width / 2 - textWidth / 2;
    const startY = height / 2 - textHeight / 2;
    const textDotRadius = Math.min(dotRadius * fontScale, pitch / 3);

    for (let characterIndex = 0; characterIndex < time.length; characterIndex++) {
        const glyph = LED_FONT[time[characterIndex]];

        for (let row = 0; row < glyph.length; row++) {
            for (let column = 0; column < glyph[row].length; column++) {
                if (glyph[row][column] !== '1') {
                    continue;
                }

                const x = startX + (characterIndex * 6 + column) * pitch;
                const y = startY + row * pitch;
                const glowRadius = Math.min(textDotRadius * 4, pitch * 0.45);
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
    const canvas = document.getElementById('clockCanvas');
    syncCanvasSize(canvas);
    clearCanvas(canvas, 'black');

    const boxSize = Math.min(canvas.width, canvas.height) / window.devicePixelRatio;
    const now = new Date();
    const dotRadius = 2;
    renderFives(canvas, boxSize, 'red', dotRadius);
    renderSeconds(canvas, boxSize, 'red', dotRadius, now);
    renderDigitalTime(canvas, boxSize, now, 'red', dotRadius);

    requestAnimationFrame(renderLedClock);
}

const clockSettings = JSON.parse(document.getElementById('clock-settings').textContent);
switch (clockSettings.clock_type) {
    case 'LED':
        requestAnimationFrame(renderLedClock);
        break;
    default:
        console.error('Unknown clock type:', clockSettings.clock_type);
}