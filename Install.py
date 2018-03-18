#!/usr/bin/python3

#Auto install program

#You need only this package on Raspbian Jessie:
#   sudo apt-get install libav-tools
#Git: DaveCalaway: https://goo.gl/9r6bwz
import os
import shutil

#COPY THE SERVICE
shutil.copy(os.getcwd() + "/PiLapse.service","/etc/systemd/system/")

#ADD PERMISSION
permission = ["sudo systemctl start PiLapse.service",
              "sudo systemctl enable PiLapse.service",
              "sudo chmod 755 -R /home/pi/PiLapse",
              "sudo mkdir /home/pi/PiLapse/SigleShot"]

for i in range(len(permission)):
    os.system(permission[i])
