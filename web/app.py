from flask import Flask, jsonify, render_template, request
from unsplashed_wallpaper import UnsplashedWallpaper

app = Flask(__name__)
app.config.from_object('web.config')

DEFAULT_LOCATION="San Francisco,California"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_wallpaper")
def get_wallpaper():
    uw = UnsplashedWallpaper()
    # Get IP and pass it in as a parameter
    if request.remote_addr in ("localhost", "127.0.0.1"):
        location = DEFAULT_LOCATION
    else:
        location = uw.get_location(request.remote_addr)
        location = DEFAULT_LOCATION if location is None else location

    width = request.args.get("width", 1000)
    height = request.args.get("height", 1000)
    wallpaper = uw.get_wallpaper(DEFAULT_LOCATION, width, height)
    return jsonify(wallpaper)
