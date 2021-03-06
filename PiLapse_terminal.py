#!/usr/bin/python3

# Terminal program for PiLaps

import json
import os
# You need only this package on Raspbian Jessie:
#   sudo apt-get install libav-tools
# Git: DaveCalaway: https://goo.gl/9r6bwz

dropbox = 0

print ('Welcome to PiLaps terminal mode!\n')

period = input('The period of a Timelaps in minuts: ')
freq = input('The frequency of capture in seconds: ')
dirName = input('Enter name s dir: ')
preview = input('Do you want a preview? Y/N  -  You need a startx running! : ')
if os.path.isfile('/home/pi/PiLapse/dropbox_uploader.sh'):
    dropbox = input('Dropbox upload? Y/N - Dropbox-Uploader must installed : ')
    if (dropbox == 'y' or dropbox == 'Y'):
        dropbox = 1
    else:
        dropbox = 0

if (preview == 'y' or preview == 'Y'):
    preview = 1
else:
    preview = 0

# crate a json file
with open('workfile.json', 'w') as outfile:
    json_string = {"period": int(period), "freq": int(freq),"dirName": dirName, "preview": int(preview),"dropbox": int(dropbox)}
    json.dump(json_string, outfile)
    outfile.close()
