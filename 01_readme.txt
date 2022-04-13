3D Printer Sampler GUI
Author: Johnny Duong
Note: Extended from Adrian's code (hardcoded locations and no GUI).
readme creation date: 9-1-2021

Overview: Control a 3D printer using a GUI interface and take pictures/video of certain locations

Project Goals: A user with no programming experience can run experiments.

===================================
Files included:
3dprinter_sampler_gui.py [Main GUI]

get_current_location_m114.py
prepare_experiment.py
printer_connection.py

settings.py
connection_settings.yaml
path_list_2x3_all.yaml

cell_sensor_1.csv

===================================

Hardware Requirements:
Raspberry Pi 3 or higher [Will control the camera and 3D printer]
Raspberry Pi Camera, or camera interface [Connected via ribbon cable]
USB Printer Cable (USB-A Male to USB-B Male) [For printer to Raspberry Pi]

Software Requirements:
Python Libraries:
picamera
PySimpleGUI
cv2
numpy
time
threading
parse
os
pandas
datetime
serial
yaml

*Note: The code is run locally from the Raspberry Pi, so all code must be there.
I used an IDE there to run and stop the code (crashes may happen, so stopping the code is important).

===================================
Current Architecture:

3dprinter_sampler_gui.py
This is the Main GUI file.
Think of it as the manager that calls in modules to do work. Additionally, it sets up the GUI.
The current logic is: run GUI as long as the camera is working. The camera is constantly streaming video
data on screen, if the stream breaks, the GUI breaks.
More Details:
-Threading: The experiment/sampling is a thread. The goal was to have streaming video
 while the pictures are taken, allowing a user to tell if the camera is going to the correct locations.
 However, this is a buggy implementation where I have to pause the stream to take pictures with custom
 camera settings (e.g. changing red/blue gain values, different resolution, etc.).
 If no custom camera settings are in place, streaming and taking a picture would work fine.
 The goal here is being user friendly, so custom camera settings will be in place. I just have to figure out
 a good way to implement. Possible idea: treat the camera as an object with its own thread and window.

get_current_location_m114.py
Get current location of the extruder.
Useful for getting well locations.
Since only one connection is allowed to the printer, so this only receives input from the printer and
attempts to search for the location information, parse that information, then print that information to
console.
M114 is the GCode that requests from the printer the current location of the extruder.

prepare_experiment.py
Prepares for experiment (or sampling) by converting X/Y/Z coordinates in a CSV file to a GCode string list.
This list is then run by the printer object (only one printer and one camera object is allowed to exist,
or it crashes). This module creates a unique folder name for the video or image data to prevent accidental
overwriting of important data; unique is current date and time.

printer_connection.py
This module creates the printer object, controls the 3D printer, and sends GCode to the 3D printer.
There is outdated code that uses the YAML format for well locations, but CSV is recommended for easier editing.
This module also requests serial data (for location information) and prints it.
The algorithm first gets the byte size of the incoming data, then decodes it. My testing shows this method
works best since it doesn't delete any input. However, it may be causing the bug where location request
needs to be called twice to actually get the current location of the extruder. Refer to cell_sensor_1.csv
for a sample locations file.
Alternatively, you can see path_list_2x3_all.yaml for an outdated sample locations file;
you will see that CSV is the better option for readability.

settings.py
This is the settings module for 3D printer specific information. This loads up the connection_settings.yaml
file that allows you to actually connect to a 3D printer. Only tested on 2 3D printers, but these two variables
are THE most important in allowing a connection: BAUDRATE and DEVICE_PATH. Without these, you get no connection.
Since the GUI is used for 2 projects, I created a section where a programmer must choose which project (line 53 and 54). This will tell the code which settings to use with the correct baudrate and device_path.


===================================================================

Current Bugs:
1. Run experiment once, then have to close and open GUI again.
2. Get Current Location needs to run twice
3. Video Creation not supported yet (default record time does work)
4. Video freezes when taking photos (should turn into a class/object)


Future Features:
-Fix bug 1 and 4, high priority
-Refactor architecture to allow easy addition of features, such as camera settings and printer settings.
-Have 2 separate GUI windows: one for camera streaming, the other for general GUI.
-Auto Detect connected 3D printers.