# Unsplash Ubuntu

## What does it do?
A simple utility written in python that picks a high resolution random image from [unsplash.com](https://unsplash.com) and puts it as your wallpaper; updates it every hour with a new wallpaper.    

It has been modified from the original author's (PseudoAj) intent to pull a random image based on the computer's location as well.

Note: This assumes you're using Gnome, as that's the desktop manager utility that is used to set the wallpaper.

## How do I run it?
1. Install the dependencies:
    1. python-requests
    2. python-tk (Tkinter)
    3. python-urllib3

3. Open terminal and change directory:
    1. `cd UnsplashUbuntu`
    2. add permissions: `chmod +x unsplashubuntu.py`
    3. Run the program: `./unsplashubuntu.py`

4. (optional) Add the program on startup by going into launcher->startup applications
