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

class UnsplashUbuntu(object):

    def __init__(self, interval):
        print "Initializing"
        self.myScreen = tk.Tk()
        self.screen_width = self.myScreen.winfo_screenwidth()
        self.screen_height = self.myScreen.winfo_screenheight()
        self.res = "/"+str(self.screen_width)+"x"+str(self.screen_height)
        self.cwd = os.getcwd()
        self.filename = "unsplash_wallpaper.png"
        self.interval = interval

    def getWallpaper(self, location):
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

    def setWallpaper(self):
        try:
            self.setCmd = "gsettings set org.gnome.desktop.background picture-uri file:///"+self.cwd+"/"+self.filename
            os.system(self.setCmd)
        except:
            print "Exception"

    def removeWallpaper(self):
        self.filePath = self.cwd+"/"+self.filename
        if os.path.exists(self.filePath):
            os.remove(self.filePath)

    def chkNetwork(self):
        try:
            res=urllib2.urlopen('http://www.google.com',timeout=1)
            return True
        except urllib2.URLError as err:
            pass
        return False

    def run(self):
        while True:
            sleep_time = self.interval/60
            if self.chkNetwork():
                print("Daemon Running....")
                # get location (from ip)
                r = requests.get("http://ipinfo.io/json")
                j = r.json()
                location = ", ".join([j['city'], j['region']])
                self.removeWallpaper()
                self.getWallpaper(location)
                self.setWallpaper()
                sleep_time = self.interval
            for _ in xrange(sleep_time):
                time.sleep(1)

thisWallpaper = UnsplashUbuntu(3600)
thisWallpaper.run()
