#!/usr/bin/python3

# Terminal program for PiLaps

import json
# Only need this pacages on Raspbian Jessie:
#   sudo apt-get install libav-tools
# Git: DaveCalaway: https://goo.gl/9r6bwz

print ('Welcome to PiLaps terminal mode!\n')

period = input('The period of a Timelaps in minuts: ')
freq = input('The frequency of capture in seconds: ')
preview = input('Do you want a preview? Y/N  -  You need a monitor! ')

if (preview == 'y' or preview == 'Y'):
    preview = 1
else:
    preview = 0

# crate a json file
with open('workfile.json', 'w') as outfile:
    json_string = {"period": int(period), "freq": int(
        freq), "preview": int(preview)}
    json.dump(json_string, outfile)
    outfile.close()
