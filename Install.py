#!/usr/bin/python3

#Auto install program

#Only need this pacages on Raspbian Jessie:
#   sudo apt-get install libav-tools
#Git: DaveCalaway: https://goo.gl/9r6bwz
import os
import shutil

#COPY THE ENTIRE FOLDER
shutil.copytree(os.getcwd() + "PiLapse","/home/pi/")

#COPY THE SERVICE
shutil.copy(os.getcwd() + "PiLaps.service","/etc/systemd/system/")

#ADD PERMISSION
permission = ["sudo systemctl start PiLapse.service",
              "sudo systemctl enable PiLapse.service",
              "sudo chmod 755 -R /home/pi/PiLapse"]

for i in range(len(permission)):
    os.system(permission[i])
