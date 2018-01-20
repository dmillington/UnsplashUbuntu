#!/usr/bin/env python

import os
import Tkinter as tk
import time
import urllib2
import requests

# The unsplash client_id parameter is read from here
try:
    from settings_secret import *
except ImportError:
    pass

class UnsplashedWallpaper(object):

    def __init__(self):
        self.my_screen = tk.Tk()
        self.screen_width = self.my_screen.winfo_screenwidth()
        self.screen_height = self.my_screen.winfo_screenheight()
        self.res = "/"+str(self.screen_width)+"x"+str(self.screen_height)
        self.cwd = os.getcwd()
        self.file_name = "unsplash_wallpaper.png"

    def get_location(self):
        r = requests.get("http://ipinfo.io/json")
        j = r.json()
        return ", ".join([j['city'], j['region']])

    def get_wallpaper(self, location):
        try:
            r = requests.get("https://api.unsplash.com/photos/random",
                params={
                'client_id': client_id,
                'query': location,
                'w': self.screen_width,
                'h': self.screen_height,
            })
            j = r.json()
            r = requests.get(j['urls']['custom'])
            with open("unsplash_wallpaper.png", 'wb') as f:
                f.write(r.content)
        except:
            print "Exception"

    def set_wallpaper(self):
        try:
            self.set_cmd = "gsettings set org.gnome.desktop.background picture-uri file:///" + self.cwd + "/" + self.file_name
            os.system(self.set_cmd)
        except:
            print "Exception"

    def remove_wallpaper(self):
        self.file_path = self.cwd+"/"+self.file_name
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def check_network(self):
        try:
            res=urllib2.urlopen('http://www.google.com',timeout=1)
            return True
        except urllib2.URLError as err:
            pass
        return False

if __name__ == "__main__":
    interval = 3600
    uw = UnsplashedWallpaper()
    while True:
        sleep_time = interval/60
        if uw.check_network():
            print "Getting new wallpaper..."
            uw.remove_wallpaper()
            location = uw.get_location()
            uw.get_wallpaper(location)
            uw.set_wallpaper()
            sleep_time = interval
        for _ in xrange(sleep_time):
            time.sleep(1)
