#!/usr/bin/python3

# Welcome to PiLaps deamon

# You need only this package on Raspbian Jessie:
#   sudo apt-get install libav-tools
# Git: DaveCalaway: https://goo.gl/9r6bwz
import os
import subprocess
import sys
import json
import time
import datetime
import threading
import shutil
from time import sleep
from picamera import PiCamera  # https://goo.gl/s8qhDZ
from gpiozero import LEDBoard, Button  # https://goo.gl/VLH86f

# --- VARIABLES ---
# LED rgb
Anode = 1  # long leg at 5v
# Resolution for pics / Timelap
Xresolution = 1280  # default: 1280
Yresolution = 720  # default: 720
VideoQuality = 3  # default: 3 -> from 1best to 30 worse
# default: 1 -> creates a clip with 1 frames(pic) per seconds
Frame_Timelapse = 1
# In button mode, take X pic for second
freq_button = 10  # default: 10
# Dropbox Uploader
# drop_setting:
# False = leave the video and photos on Raspberry
# True = delate the dirName with video and photos
delate_folder = True # default : False
# --- --- --- ---

led = LEDBoard(red=2, green=14, blue=4)
camera = PiCamera(resolution=(Xresolution, Yresolution))
camera.vflip = True  # vertical flip
camera.hflip = True  # horizontal flip

b_status = False
old_status = False
dropbox = 0
the_lock = threading.Lock()


# --- FUNCTIONS ---

# LEDS RGB function
def rgb(led_state):
    if led_state == "on":
        if Anode:
            led.off()
        else:
            led.on()
    elif led_state == "off":
        if Anode:
            led.on()
        else:
            led.off()
    elif led_state == "red":
        if Anode:
            led.green.on()
            led.blue.on()
            led.red.off()
        else:
            led.green.off()
            led.blue.off()
            led.red.on()
    elif led_state == "green":
        if Anode:
            led.green.off()
            led.blue.on()
            led.red.on()
        else:
            led.green.on()
            led.blue.off()
            led.red.off()
    elif led_state == "blue":
        if Anode:
            led.green.on()
            led.blue.off()
            led.red.on()
        else:
            led.green.off()
            led.blue.on()
            led.red.off()
    elif led_state == "yellow":
        if Anode:
            led.green.off()
            led.blue.on()
            led.red.off()
        else:
            led.green.on()
            led.blue.off()
            led.red.on()

rgb("off")

# COUNTDOWN function
def countdown(end, time):
        for c in range(0, end):
            rgb("green")
            sleep(time)
            rgb("off")
            sleep(time)

# button read function
def button_state():
    global old_status, b_status
    val = False
    the_lock.acquire()
    if b_status != old_status:
        val = True
    else:
        val = False
    old_status = b_status
    the_lock.release()
    #print("button_state: " + str(val))
    return val


# CAMERA CONNECTION TEST
def camera_present():
    output = str(subprocess.check_output("vcgencmd get_camera", shell=True))
    if output.find("supported=1"):
        if output.find("detected=1"):
            print("Test camera: OK")
            return 1
        else:
            return 0
    else:
        return 0

#---- BUTTON THREAD ----
def button():  # https://goo.gl/S4miRc
    global b_status, led
    button = Button(3)  # IN PULL UP BY DEFAULT

    def SingleShot():
        print("Single Shot")
        countdown(3,1)

        now = datetime.datetime.now()
        timenow = now.strftime("%Y_%m_%d-%H%M")
        camera.capture('/home/pi/PiLapse/SingleShot/%s.jpg' % timenow)
        # IS dropbox_uploader READY?
        if os.path.isfile('/home/pi/PiLapse/dropbox_uploader.sh'):
            rgb("blue")
            os.chdir("/home/pi/PiLapse/")
            dropbox_up = "./dropbox_uploader.sh upload /home/pi/PiLapse/SingleShot/" + timenow + ".jpg" + " /"
            os.system(dropbox_up)
        sleep(1)
        rgb("green")

    while True:
        button.wait_for_press() # Pause the script until the device is activated
        currentTime = int(round(time.time()))  # seconds
        button.wait_for_release()  # Pause the script until the device is activated
        DeltaTime = int(round(time.time())) -  currentTime # seconds

        if(DeltaTime>=3 or b_status): # TimeLapse in button mode
            the_lock.acquire()
            b_status = not(b_status)
            the_lock.release()
        else: # Single shot
            rgb("off")
            sleep(1)
            SingleShot()


# button thread GO!
button_thread = threading.Thread(target=button)
button_thread.start()


# ---- MAIN PROGRAM ----
while True:
    if not camera_present():
        # CAMERA NOT CONNECTED
        rgb("red")
        break
    rgb("green")

    terminal = False
    print("GO")
    # BUTTON OR TERMINAL?
    while True:
        sleep(1)

        # BUTTON
        # print(button_state())
        if button_state():
            print("Button mode")
            freq = freq_button
            now = datetime.datetime.now()
            dirName = now.strftime("%Y_%m_%d-%H%M")
            os.makedirs("/home/pi/PiLapse/" + dirName)
            # MOVE TO THE PROJECT'S FOLDER
            os.chdir("/home/pi/PiLapse/" + dirName)
            break

        # TERMINAL
        if os.path.isfile('/home/pi/PiLapse/workfile.json'):  # does the json file exist?
            terminal = True
            print("terminal mode")
            # LOAD INFO FROM THE FILE
            data_file = json.load(open('/home/pi/PiLapse/workfile.json'))
            period = int(data_file["period"])
            freq = int(data_file["freq"])
            dirName = data_file["dirName"]
            preview = int(data_file["preview"])
            dropbox = int(data_file["dropbox"])
            # CLEAR FILE
            os.remove("/home/pi/PiLapse/workfile.json")
            # JUMP IN TO THE NEW FOLDER
            os.makedirs("/home/pi/PiLapse/" + dirName)
            # MOVE TO THE PROJECT'S FOLDER
            os.chdir("/home/pi/PiLapse/" + dirName)
            break

    # Preview & COUNTDOWN
    if terminal:
        if preview:
            print ('preview')
            camera.start_preview()
            input('Press any key to start.')
            camera.stop_preview()
    countdown(3,1)

    # CAPTURE
    rgb("yellow")
    previousSec = 0
    if terminal:
        currentTime = int(round(time.time()))  # seconds
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        if terminal:
            print('Captured %s' % filename)
            currentSec = int(round(time.time()))
            # print(currentSec)
            #print( (int(period)*60)+currentTime )
            if(currentSec > (period * 60) + currentTime):
                print('End cature.')
                break
        sleep(freq)
        if button_state():
            print("End cature button")
            break

    # MAKE A VIDEO THIS PICS
    # https://goo.gl/UDfCHz
    rgb("yellow")

    avconv = "avconv -y -r " + repr(Frame_Timelapse) + " -i img%03d.jpg -r " + repr(Frame_Timelapse) + " -vcodec libx264 -q:v " + repr(
        VideoQuality) + " -vf crop=" + repr(Xresolution) + ":" + repr(Yresolution) + ",scale=iw:ih TimeLapse.mp4"
    os.system(avconv)

    countdown(5,1)


    # RETURN TO ROOT FOLDER
    os.chdir("/home/pi/PiLapse/")

    # UPLOAD TO DROPBOX
    if dropbox:
        rgb("blue")
        dropbox_up = "./dropbox_uploader.sh upload /home/pi/PiLapse/" + dirName + " /"
        os.system(dropbox_up)
        if delate_folder:
            shutil.rmtree("/home/pi/PiLapse/" + dirName)
