#!/usr/bin/env python

import subprocess

print("salut")

_x_screen = ":0.0"

new_window = subprocess.call(['xdotool', 'search', '--onlyvisible', '--screen', _x_screen, '--class', 'Firefox'])

print(new_window)