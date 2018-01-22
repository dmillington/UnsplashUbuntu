from flask import Flask, render_template
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
   url = uw.get_wallpaper("San Francisco, California", 1000, 1000)
   return url
