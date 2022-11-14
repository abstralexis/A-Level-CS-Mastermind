// When the window loads, do this:
window.onload = function() {
    main();
}

function canvasInit() {
    /*
    Initialise the canvas
    Returns a list of [canvas, ctx] where
    ctx is the canvas context.
    */
    var canvas = document.getElementById("gameCanvas");
    var ctx = canvas.getContext("2d");
    return [canvas, ctx];
}

function main() {

    var board = [
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null]
    ]

    draw();
    setInterval(draw, 10);
}

function draw() {
    // Init canvas
    var [canvas, ctx] = canvasInit();

    fillCanvas();
}

function fillCanvas() {
    // Init canvas
    var [canvas, ctx] = canvasInit();

    var w = canvas.width;
    var h = canvas.height;

    var gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, "darkslateblue");
    gradient.addColorStop(1, "black");

    // Fill with gradient
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, w, h); 
}

function drawSquare(x, y, colour) {
    // Init canvas
    var [canvas, ctx] = canvasInit();

    ctx.fillStyle = colour;
    ctx.fillRect(x, y, 50, 50);
}

function tmpDrawRed() {
    drawSquare(10, 10, 'red');
}

function tmpDrawBlue() {
    drawSquare(50, 50, 'blue');
}