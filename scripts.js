// When the window loads, do this:
window.onload = function() {
    main();
}

function main() {
    var canvas = document.getElementById("gameCanvas"); // Canvas object
    var ctx = canvas.getContext("2d");                  // Image rendering context

    draw(canvas, ctx);
    setInterval(draw, 10);
}

function draw(canvas, ctx) {
    fillCanvas(canvas, ctx);
}

function fillCanvas(canvas, ctx) {
    var w = canvas.width;
    var h = canvas.height;

    var gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, "darkslateblue");
    gradient.addColorStop(1, "black");

    // Fill with gradient
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, w, h); 
}

function drawSquare(canvas, ctx, x, y, colour) {
    ctx.fillStyle = colour;
    ctx.fillRect(x, y, 50, 50);
}