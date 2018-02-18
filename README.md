# PiLapse
Transform your Raspberry Pi in a Timelapse machine!  

**Status**: Beta

## Install & Run
#### Preliminal steps
You need only this package on Raspbian Jessie: `sudo apt-get install libav-tools`  

Run this command on terminal: `vcgencmd get_camera`  


**Supported** and **Detected** must be **1**, or the script does not run.   
IF Supported is 0, run this command on terminal `sudo raspi-config` and enable the camera.   
If Detected is 0, the camera is not connected to the Raspi.   

**Download** the script folder from GitHub or run this command: `git clone https://github.com/DaveCalaway/PiLapse`   
**Install** The folder "PiLapse" MUST stay at "/home/pi/" and you can install the script by running the `python3 Install.py`.  
The script will start autonomously every time the RPi boot.

## Operation Mode:
### Terminal mode
This terminal version help you to control the period, frequency and folder name for a timelapse.  
You can run it by run the `python3 PiLapse_terminal.py` and follow the guide.   


### Button mode
The Daemon version help you to control the TimeLapse with an external button, it takes 1 pic every 10 second by default.   
You can change this default period by opening the `PiLapse.py` file and edit the *VARIABLES* -> freq_button.  
It creates a folder called "year-month-day time".  
The Daemon run continuously.  
<p align="center">
<img src="https://raw.githubusercontent.com/DaveCalaway/PiLapse/master/image/schematic_bb.jpg" width="400">
</p>

## Standard file size
The RPi Camera has a resolution of 1280, 720. This is a default size for photos and Timelapse:  
<p align="center">
<img src="https://github.com/DaveCalaway/PiLapse/blob/master/image/output_dimension.png" width="400">  
</p>
If you want to change those, open the `PiLapse.py` file and edit the *VARIABLES*.  

----------
*DaveCalaway*
