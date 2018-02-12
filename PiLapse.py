#!/usr/bin/python3

# Welcome to PiLaps deamon

# Only need this pacages on Raspbian Jessie:
#   sudo apt-get install libav-tools
# Git: DaveCalaway: https://goo.gl/9r6bwz
import os
#import os.path
import sys
import json
import time
import threading
from time import sleep
from picamera import PiCamera  # https://goo.gl/s8qhDZ
from gpiozero import LED, Button  # https://goo.gl/VLH86f


led = LED(17)
the_lock = threading.Lock()
camera = PiCamera(resolution=(1280, 720))

b_status = False
old_status = False

#---- BUTTON THREAD ----
def button(): # https://goo.gl/S4miRc
    global b_status, led
    button = Button(3)  # IN PULL UP BY DEFAULT
    while True:
        button.wait_for_press() # Pause the script until the device is activated
        the_lock.acquire()
        b_status = not(b_status)
        the_lock.release()
        led.on()
        sleep(2)
        led.off()


# button thread GO!
button_thread = threading.Thread(target=button)
button_thread.start()

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


# ---- MAIN PROGRAM ----
while True:
    terminal = False
    print("GO")
    # BUTTON OR TERMINAL?
    while True:
        sleep(1)
        # BUTTON
        #print(button_state())
        if button_state():
            print("Button mode")
            freq = 1
            break

        # TERMINAL
        if os.path.isfile('workfile.json'):  # does the json file exist?
            print("terminal mode")
            # LOAD INFO FROM THE FILE
            data_file = json.load(open('workfile.json'))
            period = int(data_file["period"])
            # print(period)
            freq = int(data_file["freq"])
            # print(freq)
            preview = int(data_file["preview"])
            terminal = True
            # CLEAR FILE
            os.remove('workfile.json')
            break

    # Preview & COUNTDOWN
    if terminal:
        if preview:
            print ('preview')
            camera.start_preview()
            input('Press any key to start.')
            camera.stop_preview()
        num = [3, 2, 1]
        for i in range(len(num)):
            print (num[i])
            sleep(1)
    else:
        for c in range(0,3):
            led.on()
            sleep(1)
            led.off()
            sleep(1)

    # CAPTURE
    previousSec = 0
    if terminal:
        currentTime = int(round(time.time())) # seconds
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
            led.off()
            break

    # MAKE A VIDEO THIS PICS
    # https://goo.gl/UDfCHz
    avconv = "avconv -y -r 1 -i img%03d.jpg -r 1 -vcodec libx264 -q:v 3  -vf crop=1280:720,scale=iw:ih tlfullhiqual.mp4"
    os.system(avconv)
    if terminal:
        print("Video done.")
    else:
        # blink color
        led.off()
