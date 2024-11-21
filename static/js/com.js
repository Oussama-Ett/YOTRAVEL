// static/script.js

function displayImageFullScreen(imageUrl) {
    var overlay = document.getElementById("fullscreen-overlay");
    var image = document.getElementById("fullscreen-image");

    image.src = imageUrl;
    overlay.style.display = "block";
    document.body.style.overflow = "hidden";
}

function closeFullscreen() {
    var overlay = document.getElementById("fullscreen-overlay");
    overlay.style.display = "none";
    document.body.style.overflow = "auto";
}
