#!/usr/bin/python3

#Auto install program

#Only need this pacages on Raspbian Jessie:
#   sudo apt-get install libav-tools
#Git: DaveCalaway: https://goo.gl/9r6bwz
import os
import shutil

#COPY THE ENTIRE FOLDER
shutil.copytree(os.getcwd() + "PiLapse","/home/pi/")

#ADD PERMISSION
permission = ("sudo chmod 755 -R /home/pi/PiLapse")
os.system(permission)
