#!/usr/bin/env python3.7

import subprocess
import os

_x_screen = "0"


def call_xdotools(keystroke):
    os.environ['DISPLAY'] = ":0." + _x_screen
    os.environ['XAUTHORITY'] = "/run/lightdm/pi/xauthority"
    try:
        subprocess.call(['xdotool', 'search', '--sync', '--onlyvisible', '--screen', _x_screen, '--class', 'Firefox', 'key', keystroke])
        return "xdotool succeeded in stroking " + keystroke
    except:
        return "xdotool threw an error, maybe it is not installed on the IoTBox"


        
def update_url(url=None):
    os.environ['DISPLAY'] = ":0." + _x_screen
    os.environ['XAUTHORITY'] = '/run/lightdm/pi/xauthority'
    firefox_env = os.environ.copy()
    firefox_env['HOME'] = '/tmp/' + _x_screen
    new_window = subprocess.call(['xdotool', 'search', '--onlyvisible', '--screen', _x_screen, '--class', 'Firefox'])
    subprocess.Popen(['firefox', url], env=firefox_env)

    if new_window:
        print("coucou")
        call_xdotools('F11')


update_url(url="github.com")


print("salut")


