"""
Graphical User Interface for using the 3D Printer to take picture/video samples
Author: Johnny Duong
Projects: Cell Sensor and MHT
San Francisco State University

Current Features:
-Has Camera Feed
-Can move X, Y, Z of 3D Printer in various relative direction and increments
-Can get Current Location of Extruder Nozzle
-Input Custom GCode

Future Features:
-Smart Movement: Only take a picture or video if current location is
                 the destination (+/- 1 mm)
-Be able to take picture/video without interferring with camera feed
-Save/Open CSV Option for locations
-Preview Sample Locations
-Run Experiment (photo or video, maybe use a radio button)
   -Run for x iterations
-Camera Settings (white balance, sharpness, and so on)
-Display Current Location in GUI

Current TODO List:
-Get Current Location Mananger (runs it twice to get location)
-Put GUI Keys/Text as Constants
-Experiment with Tabs
 Source: https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Tabs_Simple.py
         https://csveda.com/creating-tabbed-interface-using-pysimplegui/

Changelog
27 Apr 2022: Fixed "restart" bug. Get Current Location automatically loops until actual current location shows up.
06 Jun 2021: Can take pictures in Experiment Thread. No video yet. Can't change resolution, bugs out. Buffer issue?
05 Jun 2021: Added in Experiment Thread, can now run GUI and Experiment at the same time.
28 Apr 2021: Changed Experiment variables into CONSTANTS
26 Apr 2021: Added in 2 Tabs: Start Experiment and Movement
18 Apr 2021: Started Changelog, Allow user to input their own GCode.

"""

# Import PySimpleGUI, cv2, numpy, time libraries
# Import picamera libraries

from picamera.array import PiRGBArray
from picamera import PiCamera
import PySimpleGUI as sg
import cv2
import numpy as np
import time
import threading

# Import modules
import settings as C
import get_current_location_m114 as GCL
import printer_connection as printer
import prepare_experiment as P

# ==== USER CONSTANTS - GUI ====
# TODO: Put these in a YAML GUI Settings File?

# ---- EXPERIMENT CONSTANTS ----
OPEN_CSV_PROMPT = "Open CSV:"
OPEN_CSV_FILEBROWSE_KEY = "-CSV_INPUT-"
START_EXPERIMENT = "Start Experiment"
STOP_EXPERIMENT = "Stop Experiment"
MAX_NUMBER_EXPERIMENTAL_RUNS = 1

# TODO: Create RADIO BUTTON Constants for picture, video, or preview
#       Create 3 KEYs, 3 Text, and Radio Group (RADIO_EXP)
EXP_RADIO_PIC_KEY = "-RADIO_PIC-"
EXP_RADIO_VID_KEY = "-RADIO_VID-"
EXP_RADIO_PREVIEW_KEY = "-RADIO_PREVIEW-"
EXP_RADIO_GROUP = "RADIO_EXP"
EXP_RADIO_PIC_TEXT = "Picture"
EXP_RADIO_VID_TEXT = "Video"
EXP_RADIO_PREVIEW_TEXT = "Preview"
EXP_RADIO_PROMPT = "For the experiment, choose to take Pictures, Videos, or Preview Only"

# --- MOVEMENT CONSTANTS ----
# Radio Keys
RELATIVE_TENTH_KEY = "-REL_TENTH-"
RELATIVE_ONE_KEY = "-REL_ONE-"
RELATIVE_TEN_KEY = "-REL_TEN-"
RADIO_GROUP = "RADIO1"
RELATIVE_TENTH_TEXT = "0.10mm"
RELATIVE_ONE_TEXT = "1.00mm"
RELATIVE_TEN_TEXT = "10.00mm"
DEFAULT_DISTANCE = "0.00"

# X+, X-, Y+, Y-, Z+, or Z-
X_PLUS = "X+"
X_MINUS = "X-"
Y_PLUS = "Y+"
Y_MINUS = "Y-"
Z_PLUS = "Z+"
Z_MINUS = "Z-"
# WINDOW_GUI_TIMEOUT
WINDOW_GUI_TIMEOUT = 10 # in ms
# TODO: Put in Constants for GCODE Input

# Restart Bug Fix
is_running_experiment = False

# ==== CONSTANTS ====

# Exposure Mode time to wait
expo_wait_time = 3 # in seconds

# Still Picture Resolution
# Sensor resolution (Pi Camera 2, 3280x2464)
pic_width = 3280
pic_height = 2464

# Video Streaming Dimensions
stream_width = 640
stream_height = 480

# ==== USER DEFINED FUNCTIONS =====

# Define function, run_relative(direction, values)
def run_relative(direction, values):
    # Converts input buttons (direction) into GCODE String,
    #  then calls run_gcode from printer module (not implemented in this demo)
    # Inputs: takes string direction (X+, X-, Y+, Y-, Z+, or Z-)
    #         values from window.read()

    # For debugging, uncomment to see if the direction (event) and values are being passed correctly
    # print("direction:", direction)
    # print("values:", values)

    # Initialize move_amount to 0.00
    move_amount = DEFAULT_DISTANCE

    # Initialize relative_coordinates variable to direction and 0.00 (example: G0X0.00, no movements)
    relative_coordinates = "{}{}".format(direction, move_amount)

    # For debugging, uncomment to see if the formatting matches the example
    # print("relative_coordinates:", relative_coordinates)

    # For debugging, uncomment to see the move_amount before the if/elif chain
    # print("move_amount (before):", move_amount)

    # Use if/elif chain to check which radio button is true (0.1, 1, or 10)
    # If values[-REL_TENTH-] == True
    #  Example If 0.1 true, change relative coordinates to X-0.10
    # else if the values of relative one is True
    #  Make movement amount into 1.00
    # else if the values of relative ten is True
    #  Make movement amount into 1.00
    if values[RELATIVE_TENTH_KEY] == True:
        # print(RELATIVE_TENTH_KEY, "is active")
        # Extract only the float number, ignoring the "mm"
        move_amount = RELATIVE_TENTH_TEXT[0:-2]
    elif values[RELATIVE_ONE_KEY] == True:
        # print(RELATIVE_ONE_KEY, "is active")
        move_amount = RELATIVE_ONE_TEXT[0:-2]
    elif values[RELATIVE_TEN_KEY] == True:
        # print(RELATIVE_TEN_KEY, "is active")
        move_amount = RELATIVE_TEN_TEXT[0:-2]

    # For debugging, uncomment to see the move_amount after the if/elif chain. Did it change?
    # print("move_amount (after):", move_amount)

    #  Use string formatting to create GCode string (example: G0X-1.00)
    relative_coordinates = "G0{}{}".format(direction, move_amount)

    print("relative_coordinates:", relative_coordinates)

    # This is where you would run the GCode
    # Run Relative Mode
    printer.run_gcode("G91")
            
    # Run relative_coordinates GCODE created in this function
    printer.run_gcode(relative_coordinates)
#   TODO: Extruder Speed Adjustment


# define get_current_location_manager()
# print("===================================")
# print("You pressed Get Current Location!")
# printer.run_gcode("M114")
# serial_string = printer.get_serial_data()
# if GCL.does_location_exist_m114(serial_string) == True:
    # current_location_dictionary, is_location_found = GCL.parse_m114(serial_string)
    # print(current_location_dictionary)
    # printer.printer.flush()
# else:
    # print("Location Not Found, Try Again")
    # printer.printer.flush()
# TODO: Test out flush, then M114, will this prevent having to do it twice?
#       Update: No, it doesn't help.
# Algorithm:
#  Flush, run M114, set serial data, check, make it run twice
#   if location not found, run again?

# TODO: Include picamera settings

# Non-Thread Version
def run_experiment_gui(main_values, camera):
    # Inputs: values or csv_filename?
    
    # Get paths from CSV file
    print("run_experiment")
    
    
    
    
    # Get CSV Filename
    csv_filename = main_values[OPEN_CSV_FILEBROWSE_KEY]
    
    # Get Path List from CSV
    path_list = P.get_path_list_csv(csv_filename)
    
    # Get GCODE Location List from path_list
    gcode_string_list = P.convert_list_to_gcode_strings(path_list)
    gcode_string_list_len = len(gcode_string_list)
    print(f"gcode_string_list_len: {gcode_string_list_len}")
    
    # Go into Absolute Positioning Mode
    printer.run_gcode(C.ABSOLUTE_POS)
    
    # Move to first well
    print("Moving to first well and waiting a few seconds")
    printer.run_gcode(gcode_string_list[0])
    
    # Wait to go to well
    time.sleep(8)
    print("Done waiting to go to WELL")
    
    
    # setup_picture_camera_settings(camera)
    setup_default_camera_settings(camera)
    
    
    # Change camera resolution
    # Sensor resolution (Pi Camera 2, 3280x2464)
    # Change resolution to largest resolution for taking pictures
    # camera.resolution = (pic_width, pic_height)
    
    # Sleep time for exposure mode
    # time.sleep(expo_wait_time)
    
    
    # Setup separate GUI
    # setup theme
    sg.theme("Light Brown 3")
    
    # setup layout of new GUI (one window with a single button)
    layout_exp = [[sg.Button("Stop Experiment", size=(20,20))]]

    # setup window for new GUI
    window_exp = sg.Window("Experiment GUI Window", layout_exp, finalize=True)
    
    # Create New Folder If not in "Preview" Mode
    if main_values[EXP_RADIO_PREVIEW_KEY] == False:
        folder_path = P.create_and_get_folder_path()
        print("Not in Preview Mode, creating folder:", folder_path)
    
    # Setup how long to wait before moving to next well (and GUI loop)
    time_to_wait = 2000 # in millisec
    
    # Initialize index for going through gcode_string_list
    index = 0
    # ---- EVENT LOOP ----
    while True:
        event, values = window_exp.read(timeout=time_to_wait)
        
        # Run Experiment
        # print(f"Index: {index}")
        # print(gcode_string_list[index])
        
        well_number = index + 1
        print(f"Well Number: {well_number}")
        
        printer.run_gcode(gcode_string_list[index])
        # Wait to go to well
        time.sleep(1)
        
        if main_values[EXP_RADIO_PREVIEW_KEY] == True:
            print("Preview Mode is On, only showing preview camera \n")
            # camera.start_preview(fullscreen=False, window=(30, 30, 500, 500))
            # time.sleep(5)
            
            # camera.stop_preview()
        elif main_values[EXP_RADIO_VID_KEY] == True:
            print("Recording Video Footage")
            file_full_path = P.get_file_full_path(folder_path, well_number)
            # TODO: Change to Video Captures
            # camera.capture(file_full_path)
        elif main_values[EXP_RADIO_PIC_KEY] == True:
            print("Taking Pictures Only")
            file_full_path = P.get_file_full_path(folder_path, well_number)
            # print(file_full_path)
            
            
            camera.capture(file_full_path)
            # TODO: Look up Camera settings to remove white balance (to deal with increasing brightness)
            
            
        
        
        # If index is at the end of the list, reset it. else increment it.
        if index == (gcode_string_list_len - 1):
            index = 0
        else:
            index += 1
            
        
        
        if event.startswith("Stop"):
            print("You pressed Stop. Stopping experiment")
            break
    
    window_exp.close()
    
    # Change resolution back to video stream
    # camera.resolution = (stream_width, stream_height)
    # time.sleep(expo_wait_time)
    
    # setup_default_camera_settings(camera)

    
    # 
    pass


# Run Experiment in a new Thread
# Define function start_experiment(event, values)
def run_experiment(event, values, thread_event, camera):
    """
    Description: Runs experiment to take a picture, video, or preview (do nothing)
    
    Input: PySimpleGUI window event and values
    """
    # global camera
    global is_running_experiment
    
    print("run_experiment")
    
    # Get CSV Filename
    csv_filename = values[OPEN_CSV_FILEBROWSE_KEY]
    
    # Get Path List from CSV
    path_list = P.get_path_list_csv(csv_filename)
    
    # Get GCODE Location List from path_list
    gcode_string_list = P.convert_list_to_gcode_strings(path_list)
    
    # Go into Absolute Positioning Mode
    printer.run_gcode(C.ABSOLUTE_POS)
    
    # Move to first well
    print("Moving to first well and waiting a few seconds")
    printer.run_gcode(gcode_string_list[0])
    
    # Wait to go to well
    time.sleep(8)
    print("Done waiting to go to WELL")
    
    
    # setup_picture_camera_settings(camera)
    setup_default_camera_settings(camera)
    
    # Create New Folder If not in "Preview" Mode
    if values[EXP_RADIO_PREVIEW_KEY] == False:
        folder_path = P.create_and_get_folder_path()
        print("Not in Preview Mode, creating folder:", folder_path)
    
    # Create While loop to check if thread_event is not set (closing)
    count_run = 0
    # while not thread_event.isSet():
    while is_running_experiment:
        
        # TODO: Put in the rest of the code for Pic, Video, Preview from 3dprinter_start_experiment or prepare_experiment
        print("=========================")
        print("Run #", count_run)
        
        well_number = 1
        for location in gcode_string_list:
            # print(gcode_string)
            printer.run_gcode(location)
            print("Going to Well Number:", well_number)
            time.sleep(4)
            if values[EXP_RADIO_PREVIEW_KEY] == True:
                print("Preview Mode is On, only showing preview camera \n")
                # camera.start_preview(fullscreen=False, window=(30, 30, 500, 500))
                # time.sleep(5)
                
                # camera.stop_preview()
            elif values[EXP_RADIO_VID_KEY] == True:
                print("Recording Video Footage")
                file_full_path = P.get_file_full_path(folder_path, well_number)
                # TODO: Change to Video Captures
                # camera.capture(file_full_path)
            elif values[EXP_RADIO_PIC_KEY] == True:
                print("Taking Pictures Only")
                file_full_path = P.get_file_full_path(folder_path, well_number)
                # print(file_full_path)
                camera.capture(file_full_path)
                # TODO: Look up Camera settings to remove white balance (to deal with increasing brightness)
            well_number += 1
        
        count_run += 1
        
        # Use For Loop to go through each location
        # TODO: Preview doesn't show preview camera
        # Original
        # for location in gcode_string_list:
            # # print(location)
            # printer.run_gcode(location)
            # time.sleep(5)
        
        
    print("=========================")
    print("Experiment Stopped")
    print("=========================")
    
# Takes in event and values to check for radio selection (Pictures, Videos, or Preview)
# Takes in CSV filename or location list generated from opening CSV file
#    Use get_path_list_csv(csv_filename) and convert_list_to_gcode_strings(path_list) from prepare_experiment module
# Create section for camera setup (or create another function to set camera settings)
#  Create function to return camera settings to default (for preview?)
# Create section for video camera setup (length of time to record)
# Goes to each location in list and takes picture, video, or nothing
#   Use for loop to go through each location list
#     Use if statement chain for radio buttons
#       If Picture, take picture. If Video, take video. If Preview, only go there.
# TODO: Include input for number of runs or length of time to run? (Use my Arduino strategy, put in the camera for loop
#       Recommend number of runs first, then implement countdown algorithm?
# TODO: Test picture/video capabilities while camera feed is running. Update, picture works


# Define function get_gcode_string_list(values)

def get_gcode_string_list(values):
    """
    Description: Takes CSV File from values (GUI Data), returns gcode_string_list
    Input: values, a dictionary from PySimpleGUI Window Reads
    Return/Output: GCode String List for well location.
    """
    # Get CSV Filename
    csv_filename = values[OPEN_CSV_FILEBROWSE_KEY]
    
    # Get Path List from CSV
    path_list = P.get_path_list_csv(csv_filename)
    
    # Get GCODE Location List from path_list
    gcode_string_list = P.convert_list_to_gcode_strings(path_list)
    
    # Return gcode_string_list
    
    pass


# Define function, get_sample(folder_path_sample, values)

def get_sample(folder_path_sample, well_number, values):
    """
    Description: Takes Pic/Vid/Preview Radio Values, then takes a
                 picture, video, or preview (do nothing), stores into
                 folder_path_sample
    Inputs:
      - values, a dictionary from PySimpleGUI Window Reads. The main focus are the Radio values for the Pic/Vid/Preview.
      - folder_path_sample, a string holding the unique folder path for the samples (prevents accidental overwrite)
    Return/Output: Doesn't return anything. TODO: Return True/False if failed or successful?
    """
    
    # Create Unique Filename, call get_file_full_path(folder_path, well_number)
    # Check Experiment Radio Buttons
    #  If Picture is True, take a picture. Save with unique filename
    #  If Video is True, take a video. Save with unique filename
    #  If Preview is True, do nothing or print "Preview Mode"
    
    pass
    

def setup_picture_camera_settings(camera):
    print("Setting up picture camera settings")
    
    # Turn Exposure mode back on so camera can adjust to new light
    camera.exposure_mode = "auto"
    
    # Turn off camera led
    camera.led = False
    
    # Camera Framerate
    camera.framerate = 30
    time.sleep(1)
    
    # Setup default resolution
    # Sensor resolution (Pi Camera 2, 3280x2464)
    # width = 640
    # height = 480
    camera.resolution = (pic_width, pic_height)
    
    # ISO: Image Brightness
    # 100-200 (daytime), 400-800 (low light)
    iso_number = 100
    camera.iso = iso_number
    
    time.sleep(10)
    
    # Contrast
    # Takes values between 0-100
    contrast_number = 50
    camera.contrast = contrast_number
    
    # Automatic White Balance
    camera.awb_mode = "off"
    red_gain = 1.5
    blue_gain = 1.8
    camera.awb_gains = (red_gain, blue_gain)
    
    
    
    # Exposure Mode
    # camera.framerate = 30
    # camera.shutter_speed = 33164
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = "off"
    # Must let camera sleep so exposure mode can settle on certain values, else black screen happens
    time.sleep(2)
    print("Done setting picture camera settings")
    

def setup_default_camera_settings(camera):
    print("Setting default camera settings")
    
    # Turn Exposure mode back on so camera can adjust to new light
    camera.exposure_mode = "auto"
    
    # Turn off camera led
    camera.led = False
    
    # Camera Framerate
    camera.framerate = 30
    time.sleep(1)
    
    # Setup default resolution
    # Sensor resolution (Pi Camera 2, 3280x2464)
    width = 640
    height = 480
    camera.resolution = (width, height)
    
    # ISO: Image Brightness
    # 100-200 (daytime), 400-800 (low light)
    iso_number = 100
    camera.iso = iso_number
    
    time.sleep(10)
    
    # Contrast
    # Takes values between 0-100
    contrast_number = 50
    camera.contrast = contrast_number
    
    # Automatic White Balance
    camera.awb_mode = "off"
    red_gain = 1.5
    blue_gain = 1.8
    camera.awb_gains = (red_gain, blue_gain)
    
    
    
    # Exposure Mode
    # camera.framerate = 30
    # camera.shutter_speed = 33164
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = "off"
    # Must let camera sleep so exposure mode can settle on certain values, else black screen happens
    time.sleep(2)
    
    print("Done setting default camera settings")
    
    pass


# Define function to get current location
def get_current_location():
    printer.run_gcode("M114")
    serial_string = printer.get_serial_data()
    if GCL.does_location_exist_m114(serial_string) == True:
        current_location_dictionary, is_location_found = GCL.parse_m114(serial_string)
        print(current_location_dictionary)
        # printer.printer.flush()
    else:
        print("Location Not Found, Try Again")
    pass
    

def get_current_location2():
    print("Getting Current Location...")
    
    # Init result with negative values for error checking
    # If negative value, then location was not found
    result = {"X": -1.00, "Y": -1.00, "Z": -1.00}
    
    # Number of attempts to check for location (how many times to run for loop)
    num_location_checks = 10
    
    # Number of location grabs until that one is accepted (in case of outdated location)
    num_until_location_accepted = 1
    
    # Init location_found_counter (want loc to be found at least once since old one is stored)
    location_found_counter = 0
    
    num_searches = 0
    for i in range(num_location_checks):
        num_searches += 1
        # Uncomment print statement for debugging
        # print(f"Location Search Attempt: {i}")
        # Run M114 GCODE
        printer.run_gcode("M114")
        serial_string = printer.get_serial_data2()
        if GCL.does_location_exist_m114(serial_string) == True:
            
            current_location_dictionary, is_location_found = GCL.parse_m114(serial_string)
            
            if location_found_counter == 0:
                location_found_counter += 1
                # Uncomment print statement for debugging
                # print("Location Found, but might be outdated. Trying again")
                continue
            elif location_found_counter >= num_until_location_accepted:
                result = current_location_dictionary
                print("Location Found, Stopping Search.")
                break
        else:
            print("Location Not Found, Trying Again...")
            # If location not found, wait a second in case there is a buffer issue?
            # If no data found, get_serial_data2 ran at least 20 times, so used default empty string
            #   Should try again
            """
            print(f"Data Found: {serial_string}")
            if len(serial_string) == 0:
                print("No data found")
            """
            time.sleep(1)
            continue
        
        # Get Serial Data
        # If location exist in serial string, increment location_found_counter by 1, start while loop again
        #   If loc exist and counter is 1, save location
        # If location does not exist, don't increment, start while loop again
    
    print(f"Number of Location Retrieval Attempts: {num_searches}")
    print("**Note: If all coord are -1.00, then location was not found")
    print(f"Location: {result}")
    return result
    

# define main function
def main():
    
    global is_running_experiment

    # Setup Camera
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    setup_default_camera_settings(camera)
    
    # MHT: 270
    # camera.rotation = 270

    # Cell Sensor, at home, 90
    # camera.rotation = 90
    
    # MHT: 270, Cell Sensor: 90
    camera.rotation = C.CAMERA_ROTATION_ANGLE
    
    rawCapture = PiRGBArray(camera, size=(640, 480))
    
    #
    # allow the camera to warmup
    time.sleep(0.1)
    
    # Setup 3D Printer
    csv_filename = "testing/file2.csv"
    path_list = printer.get_path_list_csv(csv_filename)
    printer.initial_setup(path_list)
    
    # Move Extruder Out Of The Way
    x_start = 0
    y_start = C.Y_MAX
    z_start = 50
    printer.move_extruder_out_of_the_way(x_start, y_start, z_start)

    sg.theme("LightGreen")

    # Create tabs layout:
    # Tab 1: Start Experiment (Pic, vid, or Preview), Open CSV File. Disable Start Experiment if no CSV loaded
    # Tab 2: Movement Tab, with input GCODE (temp), Future: Move specific coordinates
    #
    
    # Tab 1: Start Experiment Tab
    # TODO: Create 3 Radio Buttons for Picture, Video, Preview (Default), and Prompt "Choose to take Pictures, Video, or only preview locations"
    # TODO: Create User Input for number of Trials (use placeholder)
    tab_1_layout = [ [sg.Text(OPEN_CSV_PROMPT), sg.Input(), sg.FileBrowse(key=OPEN_CSV_FILEBROWSE_KEY)],
                     [sg.Text(EXP_RADIO_PROMPT)],
                     [sg.Radio(EXP_RADIO_PIC_TEXT, EXP_RADIO_GROUP, default=False, key=EXP_RADIO_PIC_KEY),
                        sg.Radio(EXP_RADIO_VID_TEXT, EXP_RADIO_GROUP, default=False, key=EXP_RADIO_VID_KEY),
                        sg.Radio(EXP_RADIO_PREVIEW_TEXT, EXP_RADIO_GROUP, default=True, key=EXP_RADIO_PREVIEW_KEY)],
                     [sg.Button(START_EXPERIMENT, disabled=True), sg.Button(STOP_EXPERIMENT, disabled=True)]
                   ]
    
    # Tab 2: Movement Tab
    tab_2_layout = [ [sg.Text("", size=(3, 1)), sg.Button("Get Current Location", size=(20, 1))],
                     [sg.Radio(RELATIVE_TENTH_TEXT, RADIO_GROUP, default=False, key=RELATIVE_TENTH_KEY),
                        sg.Radio(RELATIVE_ONE_TEXT, RADIO_GROUP, default=True, key=RELATIVE_ONE_KEY),
                        sg.Radio(RELATIVE_TEN_TEXT, RADIO_GROUP, default=False, key=RELATIVE_TEN_KEY)
                     ],
                     [sg.Text("", size=(5, 1)), sg.Button(Y_PLUS, size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button(Z_MINUS, size=(5, 1))],
                     [sg.Button(X_MINUS, size=(10, 1)), sg.Button(X_PLUS, size=(10, 1))],
                     [sg.Text("", size=(5, 1)), sg.Button(Y_MINUS, size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button(Z_PLUS, size=(5, 1))],
                     [sg.HorizontalSeparator()],
                     [sg.Text("Input GCODE (e.g. G0X0Y50):")],
                     [sg.InputText(size=(30, 1), key="-GCODE_INPUT-"), sg.Button("Run", size=(5, 1)), sg.Button("Clear", size=(5, 1))]
                   ]
    
    # TABs Layout (New, Experimental
    # TODO: Put in Pic/Video Button, test them out.
    layout = [ [sg.Image(filename='', key='-IMAGE-')],
               [sg.TabGroup([[sg.Tab("Tab 1 (Exp)", tab_1_layout, key="-TAB_1_KEY"),
                              sg.Tab("Tab 2 (Mvmt)", tab_2_layout)]])
               ],
               [sg.Button("Pic"), sg.Button("Vid")]
             ]
    
    
    # Define Window Layout (Original)
    # layout = [
        # [sg.Image(filename='', key='-IMAGE-')],
        # [sg.Text("", size=(3, 1)), sg.Button("Get Current Location", size=(20, 1))],
        # [sg.Radio(RELATIVE_TENTH_TEXT, RADIO_GROUP, default=False, key=RELATIVE_TENTH_KEY),
            # sg.Radio(RELATIVE_ONE_TEXT, RADIO_GROUP, default=True, key=RELATIVE_ONE_KEY),
            # sg.Radio(RELATIVE_TEN_TEXT, RADIO_GROUP, default=False, key=RELATIVE_TEN_KEY)],
        # [sg.Text("", size=(5, 1)), sg.Button(Y_PLUS, size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button(Z_MINUS, size=(5, 1))],
        # [sg.Button(X_MINUS, size=(10, 1)), sg.Button(X_PLUS, size=(10, 1))],
        # [sg.Text("", size=(5, 1)), sg.Button(Y_MINUS, size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button(Z_PLUS, size=(5, 1))],
        # [sg.HorizontalSeparator()],
        # [sg.Text("Input GCODE (e.g. G0X0Y50):")],
        # [sg.InputText(size=(30, 1), key="-GCODE_INPUT-"), sg.Button("Run", size=(5, 1)), sg.Button("Clear", size=(5, 1))]
    # ]
    # Have Camera Feed Window
    # To the right, xy, and z
    # Below camera Feed: Show Current Location, Get Current Location Button
    
    # Threading Setup
    # Initialize empty experiment_thread object, will be used with "Start Experiment" is pushed
    experiment_thread = threading.Thread()
    
    # Initialize threading event (Allows you to stop the thread)
    thread_event = threading.Event()
    

    # Create window and show it without plot
    window = sg.Window("3D Printer GUI Test", layout, location=(800, 40))
    
    
    # Create experiment_run_counter
    experiment_run_counter = 0
    # Create Boolean is_running_experiment, default False
    # is_running_experiment = False
    # Initialize well_counter to 0 (used for running experiment, going through GCode location list)
    
    # Initialize current_location_dictionary to X=0, Y=0, Z=0
    
    # Initialize folder_path_sample to "" ("Start Experiment" will create unique folder name)
    # **** Note: This for loop may cause problems if the camera feed dies, it will close everything? ****
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # while True:
        event, values = window.read(timeout=1)
        
        # Call Get Current Location Manager Function
        # Print Current Location
        
        # TODO: Create new thread for Current Location display?
        
        frame = frame.array
        
        # ---- CSV File Checker and "Start Experiment" Enable/Disable If/Else logic
        # Check if CSV file Exists (length is 0 if CSV not loaded)
        #  Enable "Start Experiment" if true, else disable "Start Experiment"
        if len(values[OPEN_CSV_FILEBROWSE_KEY]) != 0 and is_running_experiment == False:
            # print("CSV File Exists")
            # Enable "Start Experiment" button
            window[START_EXPERIMENT].update(disabled=False)
            # print("values[OPEN_CSV_FILEBROWSE_KEY]:", values[OPEN_CSV_FILEBROWSE_KEY])
            # print(len(values[OPEN_CSV_FILEBROWSE_KEY]))
        else:
            # print("CSV File Does Not Exist")
            # Disable "Start Experiment" button
            window[START_EXPERIMENT].update(disabled=True)
        
        # ---- Main GUI Window If/elif chain ----
        if event == sg.WIN_CLOSED:
            break
        # Tab 1 (Experiment):
        elif event == START_EXPERIMENT:
            print("You pressed Start Experiment")
            
            # Set is_running_experiment to True, we are now running an experiment
            is_running_experiment = True
            
            # Run experiment without thread. Pauses video stream.
            # run_experiment_gui(values, camera)
            
            # Uncomment to see your CSV File (is it the correct path?)
            # print("CSV File:", values[OPEN_CSV_FILEBROWSE_KEY])
            
            # Disable "Start Experiment" Button
            window[START_EXPERIMENT].update(disabled=True)
            # Enable "Stop Experiment" Button
            window[STOP_EXPERIMENT].update(disabled=False)
            
            # Create actual experiment_thread
            experiment_thread = threading.Thread(target=run_experiment, args=(event, values, thread_event, camera,), daemon=True)
            experiment_thread.start()
            
            # Create Unique Folder, Get that Unique Folder's Name
            
        elif event == STOP_EXPERIMENT:
            print("You pressed Stop Experiment")
            print("Ending experiment after current run")
            experiment_run_counter = 0
            is_running_experiment = False
            # Enable "Start Experiment" Button
            window[START_EXPERIMENT].update(disabled=False)
            # Disable "Stop Experiment" Button
            window[STOP_EXPERIMENT].update(disabled=True)
            
            # Stop thread, set prepares stopping
            thread_event.set()
            
            # Stop experiemnt_thread
            experiment_thread.join(timeout=1)
            
        elif event == "Pic":
            print("You Pushed Pic Button")
            # Take a Picture
            # camera.resolution = (800, 600)
            camera.resolution = (2592, 1944)
            camera.capture("test001.jpg")
            
            camera.resolution = (640, 480)
        elif event == "Vid":
            print("You Pushed Vid Button")
            # Take a Video
        # Tab 2 (Movement)
        elif event == "Get Current Location":
            print("===================================")
            print("You pressed Get Current Location!")
            # get_current_location()
            get_current_location2()
            """
            printer.run_gcode("M114")
            serial_string = printer.get_serial_data()
            if GCL.does_location_exist_m114(serial_string) == True:
                current_location_dictionary, is_location_found = GCL.parse_m114(serial_string)
                print(current_location_dictionary)
                # printer.printer.flush()
            else:
                print("Location Not Found, Try Again")
                # printer.printer.flush()
            """
        elif event in [X_PLUS, X_MINUS, Y_PLUS, Y_MINUS, Z_PLUS, Z_MINUS]:
            # If any of the direction buttons are pressed, move extruder
            #  in that direction using the increment radio amounts
            run_relative(event, values)
        elif event == "Run":
            # Run GCODE found in the GCode  InputText box
            printer.run_gcode(values["-GCODE_INPUT-"])
        elif event == "Clear":
            # Clear GCode InputText box
            window.FindElement("-GCODE_INPUT-").Update("")

        
        # print("You entered ", values[0])
        
        # Original
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        
        # Update GUI Window with new image
        window['-IMAGE-'].update(data=imgbytes)
        
        # clear the stream in preparation for the next frame
        # Must do this, else it won't work
        rawCapture.truncate(0)

    # Out of While Loop
    
    # Closing Window
    window.close()
    
    # Closing 3D Printer Serial Connection
    printer.printer.close()
    
    # For loop to show camera feed
    pass

main()
# call main function
