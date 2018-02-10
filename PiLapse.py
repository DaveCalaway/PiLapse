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

#---- BUTTON THREAD ----
def button():
    global b_status, led
    b_status = False
    button = Button(3) # IN PULL UP BY DEFAULT
    while True:
        if button.is_pressed:
            the_lock.acquire()
            b_status = True
            the_lock.release()
            led.on()
            delay(1)
            led.off()


# button thread GO!
button_thread = threading.Thread(target=button)
button_thread.start()

# button read function
def button_state():
    the_lock.acquire()
    # button
    if b_status:
        return True
    else:
        return False
    the_lock.release()


# ---- MAIN PROGRAM ----
while True:
    terminal = False
    print("GO")
    # BUTTON OR TERMINAL?
    while True:
        sleep(1)
        the_lock.acquire()
        # BUTTON
        if b_status:
            print("button mode")
            freq = 1
        the_lock.release()
        if b_status:
            break

        # TERMINAL
        if os.path.isfile('workfile.json'):  # does the json file exist?
            print("terminal mode")
            # LOAD INFO FROM THE FILE
            data_file = json.load(open('workfile.json'))
            period = int(data_file["period"])
            #print(period)
            freq = int(data_file["freq"])
            #print(freq)
            preview = int(data_file["preview"])
            terminal = True
            # CLEAR FILE
            os.remove('workfile.json')
            break


    # preview & COUNTDOWN
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
        led.on()
        sleep(1)
        led.off()
        led.on()
        sleep(1)
        led.off()

    # CAPTURE
    previousSec = 0
    if terminal:
        currentTime = int(round(time.time()))
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        if terminal:
            print('Captured %s' % filename)
            currentSec = int(round(time.time()))
            #print(currentSec)
            #print( (int(period)*60)+currentTime )
            if(currentSec > (int(period) * 60) + currentTime):
                print('End cature.')
                break
            sleep(int(freq) * 60)
        if not button_state:
             print("End cature button")
             #blink color
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
