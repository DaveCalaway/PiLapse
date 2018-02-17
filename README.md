# PiLapse
Transform your Raspberry Pi in a Timelapse machine!  
**Status**: Beta

### Install & Run
#### Preliminal steps
Run this command on terminal: "vcgencmd get_camera"
**Supported** and **Detected** must be **1**, or the script does not run.   
IF Supported is 0, run this command on terminal "sudo raspi-config" and enable the camera.   
If Detected is 0, the camera is not connected to the Raspi.   

**Download** the script folder from GitHub or run this command: "git clone https://github.com/DaveCalaway/PiLapse"   
**Install** The folder "PiLapse" MUST stay at "/home/pi/" and you can install the script by running the "Install.py".  
The script will start autonomously every time the RPi boot.


### Terminal
This terminal version help you to control the period and frequency for a timelapse.
You can run it by run the "PiLapse_terminal.py" and follow the guide.   


### Button
The Daemon version help you to control the TimeLapse with an external button.  
The Daemon run continuously.
<img src="https://github.com/DaveCalaway/PiLapse/blob/master/image/button.png" width="400">


----------
*DaveCalaway*
