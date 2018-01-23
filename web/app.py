from flask import Flask, render_template, request
from unsplashed_wallpaper import UnsplashedWallpaper

app = Flask(__name__)
app.config.from_object('web.config')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_wallpaper")
def get_wallpaper():
   uw = UnsplashedWallpaper()
   # TODO: Get IP and pass it in as a parameter
   # uw.get_location()
   # FOR NOW:... just give back the image URL to display
   width = request.args.get("width", 1000)
   height = request.args.get("height", 1000)
   url = uw.get_wallpaper("San Francisco, California", width, height)
   return url
