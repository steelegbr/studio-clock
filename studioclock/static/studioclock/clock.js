function clearCanvas(canvas, backgroundColour) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = backgroundColour;
    ctx.fillRect(0, 0, width, height);
}

function drawLed(ctx, x, y, colour, dotRadius, opacity = 1) {
    const glowRadius = dotRadius * 4;
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

    for (let i = 0; i < 12; i++) {
        const angle = (i * 30) * Math.PI / 180; // Convert degrees to radians
        const x = (width / 2) + (boxSize / 2 - 50) * Math.cos(angle);
        const y = (height / 2) + (boxSize / 2 - 50) * Math.sin(angle);

        drawLed(ctx, x, y, colour, dotRadius);
    }
}

function renderSeconds(canvas, boxSize, colour = 'red', dotRadius = 3) {
    const ctx = canvas.getContext('2d');
    const now = new Date();
    const seconds = now.getSeconds();
    const secondProgress = now.getMilliseconds() / 1000;
    const width = canvas.width / window.devicePixelRatio;
    const height = canvas.height / window.devicePixelRatio;

    for (let i = 0; i < seconds; i++) {
        const angle = (i * 6 - 90) * Math.PI / 180; // Convert degrees to radians

        const x = (width / 2) + (boxSize / 2 - 100) * Math.cos(angle);
        const y = (height / 2) + (boxSize / 2 - 100) * Math.sin(angle);

        drawLed(ctx, x, y, colour, dotRadius);
    }

    const angle = (seconds * 6 - 90) * Math.PI / 180;
    const x = (width / 2) + (boxSize / 2 - 100) * Math.cos(angle);
    const y = (height / 2) + (boxSize / 2 - 100) * Math.sin(angle);
    drawLed(ctx, x, y, colour, dotRadius, secondProgress);
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
    const dotRadius = 2;
    renderFives(canvas, boxSize, 'red', dotRadius);
    renderSeconds(canvas, boxSize, 'red', dotRadius);

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