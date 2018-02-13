#!/usr/bin/env python

import os
import time
import urllib2
import requests

class UnsplashedWallpaper(object):

    def __init__(self):
        self.cwd = os.getcwd()
        self.file_name = "unsplash_wallpaper.png"

    def get_location(self, ip=None):
        if ip:
            r = requests.get("http://ipinfo.io/%s/json" % (ip))
        else:
            r = requests.get("http://ipinfo.io/json")
        j = r.json()
        if j['bogon']:
            return None
        else:
            return ",".join([j['city'], j['region']])

    def get_wallpaper(self, location, width, height, write_to_file=False):
        try:
            request_url = "https://source.unsplash.com/%sx%s/?%s" % (width, height, location)

            # return json, if we're not writing to local disk
            if write_to_file == False:
                return {'url': request_url}

            r = requests.get(request_url)
            with open(self.file_name, 'wb') as f:
                f.write(r.content)

            return None
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
    import Tkinter as tk
    interval = 3600
    my_screen = tk.Tk()
    screen_width = my_screen.winfo_screenwidth()
    screen_height = my_screen.winfo_screenheight()
    uw = UnsplashedWallpaper()
    while True:
        sleep_time = interval/60
        if uw.check_network():
            print "Getting new wallpaper..."
            uw.remove_wallpaper()
            location = uw.get_location()
            uw.get_wallpaper(location, screen_width, screen_height, write_to_file=True)
            uw.set_wallpaper()
            sleep_time = interval
        for _ in xrange(sleep_time):
            time.sleep(1)
