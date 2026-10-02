function clearCanvas(canvas, backgroundColour) {
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = backgroundColour;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function renderFives(canvas, boxSize, colour = 'red') {
    const ctx = canvas.getContext('2d');

    for (let i = 0; i < 12; i++) {
        const angle = (i * 30) * Math.PI / 180; // Convert degrees to radians
        const x = (canvas.width / 2) + (boxSize / 2 - 10) * Math.cos(angle);
        const y = (canvas.height / 2) + (boxSize / 2 - 10) * Math.sin(angle);

        ctx.fillStyle = colour;
        ctx.beginPath();
        ctx.arc(x, y, 1, 0, 2 * Math.PI);
        ctx.fill();
    }
}

function renderSeconds(canvas, boxSize, colour = 'red') {
    const ctx = canvas.getContext('2d');
    const now = new Date();
    const seconds = now.getSeconds();

    for (let i = 0; i <= seconds; i++) {
        const angle = (i * 6 - 90) * Math.PI / 180; // Convert degrees to radians

        const x = (canvas.width / 2) + (boxSize / 2 - 20) * Math.cos(angle);
        const y = (canvas.height / 2) + (boxSize / 2 - 20) * Math.sin(angle);

        ctx.fillStyle = colour;
        ctx.beginPath();
        ctx.arc(x, y, 1, 0, 2 * Math.PI);
        ctx.fill();
    }
}

function renderLedClock() {
    const canvas = document.getElementById('clockCanvas');
    clearCanvas(canvas, 'black');

    const boxSize = Math.min(canvas.width, canvas.height);
    renderFives(canvas, boxSize);
    renderSeconds(canvas, boxSize);

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