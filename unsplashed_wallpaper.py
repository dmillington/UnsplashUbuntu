#!/usr/bin/env python

import os
import sys
import time
import threading
import signal
import requests
import ConfigParser
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
from requests.exceptions import ConnectionError, Timeout

curr_path = os.path.dirname(os.path.realpath(__file__))
APPINDICATOR_ID = 'myappindicator'

CONFIG_FILE = os.path.expanduser('~/.config/unsplashed_wallpaper/config.conf')

# Options Dialog global vars
USE_LOCATION = False
SEARCH_TERMS = 'San Francisco'
REFRESH_INT_LIST = [1800, 3600, 7200] # 30, 60, or 120 minutes
REFRESH_INTERVAL = 1 # 3600 seconds by default

class UnsplashedWallpaper(object):

    def __init__(self):
        self.cwd = os.getcwd()
        self.file_name = "unsplash_wallpaper.png"
        self.change_now = False

    def get_location(self, ip=None):
        if ip:
            r = requests.get("http://ipinfo.io/%s/json" % (ip))
        else:
            r = requests.get("http://ipinfo.io/json")
        j = r.json()
        if 'bogon' in j and j['bogon']:
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
            requests.get('http://www.google.com',timeout=1)
            return True
        except (ConnectionError, Timeout) as err:
            pass
        return False

    def should_change_now(self):
        return self.change_now

    def reset_change_now(self):
        self.change_now = False

    def set_change_now(self):
        self.change_now = True

class MenuHandler:
    def menu_change_wallpaper(self, *args):
        uw.set_change_now()

    def menu_about(self, *args):
        about_dialog = builder.get_object("ABOUT_DIALOG")
        about_dialog.run()
        about_dialog.hide()

    def menu_options(self, *args):
        options_dialog = builder.get_object("OPTIONS_DIALOG")
        options_dialog.run()
        options_dialog.hide()

    def options_cancel_btn_clicked(self, *args):
        options_dialog = builder.get_object("OPTIONS_DIALOG")
        options_dialog.hide()

    def options_save_btn_clicked(self, *args):
        global SEARCH_TERMS
        global USE_LOCATION
        global REFRESH_INTERVAL

        SEARCH_TERMS = builder.get_object("OPTIONS_SEARCH_TERMS").get_text()
        USE_LOCATION = builder.get_object("OPTIONS_LOCATION_SWITCH").get_active()
        REFRESH_INTERVAL = builder.get_object("OPTIONS_WALLPAPER_INTERVAL_COMBOBOX").get_active()

        save_config()

        options_dialog = builder.get_object("OPTIONS_DIALOG")
        options_dialog.hide()

    def menu_quit(self, *args):
        Gtk.main_quit()

def load_config():
    global SEARCH_TERMS
    global USE_LOCATION
    global REFRESH_INTERVAL

    config = ConfigParser.RawConfigParser(
        {'use_location': 'False',
         'search_terms': 'San Francisco',
         'refresh_interval': '1',
        })
    config.add_section('general')
    config.read(CONFIG_FILE)
    USE_LOCATION = config.getboolean('general', 'use_location')
    SEARCH_TERMS = config.get('general', 'search_terms')
    REFRESH_INTERVAL = config.getint('general', 'refresh_interval')

def save_config():
    global SEARCH_TERMS
    global USE_LOCATION
    global REFRESH_INTERVAL

    config = ConfigParser.RawConfigParser()
    config.add_section('general')
    config.set('general', 'use_location', USE_LOCATION)
    config.set('general', 'search_terms', SEARCH_TERMS)
    config.set('general', 'refresh_interval', REFRESH_INTERVAL)

    dirname = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(CONFIG_FILE, 'wb+') as configfile:
        config.write(configfile)

def unsplashed_thread():
    import Tkinter as tk
    my_screen = tk.Tk()
    screen_width = my_screen.winfo_screenwidth()
    screen_height = my_screen.winfo_screenheight()

    while True:
        if uw.check_network():
            print "Getting new wallpaper..."
            uw.remove_wallpaper()
            if USE_LOCATION:
                location = uw.get_location()
            else:
                location = SEARCH_TERMS
            uw.get_wallpaper(location, screen_width, screen_height, write_to_file=True)
            uw.set_wallpaper()
        for _ in xrange(REFRESH_INT_LIST[REFRESH_INTERVAL]):
            if uw.should_change_now():
                uw.reset_change_now()
                break
            time.sleep(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    load_config()

    builder = Gtk.Builder()
    builder.add_from_file("unsplashed_menu.glade")
    builder.connect_signals(MenuHandler())

    builder.get_object("OPTIONS_SEARCH_TERMS").set_text(SEARCH_TERMS)
    builder.get_object("OPTIONS_LOCATION_SWITCH").set_active(USE_LOCATION)

    list_store = Gtk.ListStore(GObject.TYPE_STRING)
    list_store.append(("30 minutes",))
    list_store.append(("1 hour",))
    list_store.append(("2 hours",))

    cell = Gtk.CellRendererText()

    refresh_combobox = builder.get_object("OPTIONS_WALLPAPER_INTERVAL_COMBOBOX")
    refresh_combobox.set_model(list_store)
    refresh_combobox.pack_start(cell, True)
    refresh_combobox.set_active(REFRESH_INTERVAL)
    refresh_combobox.add_attribute(cell, "text", 0)

    indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, Gtk.STOCK_INFO, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(builder.get_object("THE_MENU"))

    uw = UnsplashedWallpaper()

    thread = threading.Thread(target=unsplashed_thread)
    thread.daemon = True
    thread.start()

    Gtk.main()
