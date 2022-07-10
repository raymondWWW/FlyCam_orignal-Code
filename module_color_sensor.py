"""
Module for Color Sensor

To be used by the GUI
"""
import csv
import json
import pandas as pd
import PySimpleGUI as sg

# TODO: Uncomment when actually running module in GUI
# import RPi.GPIO as GPIO
import time

import os
from os.path import join

# Sensor Pins, Broadcom (BCM) Numbering System
# Use the number after GPIO
S2 = 23
S3 = 24
OUT = 25
SIGNAL = OUT

S0 = 16
S1 = 20
# Note: OE is Output Enable
# OE

color_keys = ['red', 'green', 'blue', 'clear']
prf_keys = ["number_of_cycles", "external_time", "internal_time", "freq_ext", "freq_int", "freq_expected"]

TIME_TO_WAIT = 1 # 1 second to count cycles

# Save CSV Constants

# Create Temp file to store locations into
TEMP_FOLDER = r"/home/pi/Projects/3dprinter_sampling/temp"
TEMP_FILE = r"temp_loc_color.csv"
TEMP_FULL_PATH = os.path.join(TEMP_FOLDER, TEMP_FILE)

# GUI CONSTANTS
# [sg.Button("Setup Color Sensor"), sg.Button("Get Color")],
# [sg.Button("Save Color"), sg.Button("Stop Color Sensor")]
SETUP_COLOR_SENSOR = "Setup Color Sensor"
GET_COLOR = "Get Color"
SAVE_COLOR = "Save Color"
STOP_COLOR_SENSOR = "Stop Color Sensor"

# Loop Control GUI Keys and Button
X_LOOP_BUTTON = "Start X Loop"
X_START_KEY = "-X START-"
X_END_KEY = "-X END-"
X_INC_KEY = "-X INC-"

Y_LOOP_BUTTON = "Start Y Loop"
Y_START_KEY = "-Y START-"
Y_END_KEY = "-Y END-"
Y_INC_KEY = "-Y INC-"

# For choosing save folder location for colors/printerLocations CSV
COLOR_SAVE_FOLDER_KEY = "-Color Save Folder-"

# Non-Printer Events
COLOR_SENSOR_NON_PRINTER_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, STOP_COLOR_SENSOR]

# Printer Events (Events requiring printer control)
COLOR_SENSOR_PRINTER_EVENT_LIST = [SAVE_COLOR, X_LOOP_BUTTON, Y_LOOP_BUTTON]

# Color Sensor Event List for checking if a button is pressed
COLOR_SENSOR_ALL_EVENT_LIST = []


def populate_color_sensor_all_event_list():
    global COLOR_SENSOR_ALL_EVENT_LIST

    for non_printer in COLOR_SENSOR_NON_PRINTER_EVENT_LIST:
        COLOR_SENSOR_ALL_EVENT_LIST.append(non_printer)

    for printer in COLOR_SENSOR_PRINTER_EVENT_LIST:
        COLOR_SENSOR_ALL_EVENT_LIST.append(printer)

    # print(COLOR_SENSOR_ALL_EVENT_LIST)


# ------- COLOR SENSOR FUNCTIONS -------
def color_sensor_setup():
    print("Setting up Color Sensor Pins")
    
    # Set GPIO Mode as Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SIGNAL,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(S2,GPIO.OUT)
    GPIO.setup(S3,GPIO.OUT)
    
    # Output Frequency
    GPIO.setup(S0,GPIO.OUT)
    GPIO.setup(S1,GPIO.OUT)
    
    print("\n")


# Output Frequency Settings
def set_100_output():
    print("Setting 100% Output Frequency")
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 100% Output:
    GPIO.output(S0,GPIO.HIGH)
    GPIO.output(S1,GPIO.HIGH)


def set_20_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 20% Output:
    GPIO.output(S0,GPIO.HIGH)
    GPIO.output(S1,GPIO.LOW)


def set_2_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    
    # Setup 2% Output:
    GPIO.output(S0,GPIO.LOW)
    GPIO.output(S1,GPIO.HIGH)


def set_power_down_output():
    # 100% Output Frequency Scaling: S0: High, S1: High
    # 20%  Output Frequency Scaling: S0: High, S1: Low
    # 2%   Output Frequency Scaling: S0: Low,  S1: High
    # Power Down Output Frequency Scaling: S0: Low,  S1: Low
    
    # Setup Power Down Output:
    GPIO.output(S0,GPIO.LOW)
    GPIO.output(S1,GPIO.LOW)


def end_program():
    GPIO.cleanup()


# Get Color Functions, PRF
def get_red_prf(time_to_wait):
    # Set S2 and S3 to low to capture red
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_green_prf(time_to_wait):
    # GREEN: S2: HIGH, S3: HIGH
    # Set S2 and S3 to HIGH to capture green
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_blue_prf(time_to_wait):
    # BLUE: S2: LOW, S3: HIGH
    # Set S2 to LOW and S3 to HIGH to capture blue
    GPIO.output(S2,GPIO.LOW)
    GPIO.output(S3,GPIO.HIGH)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


def get_clear_prf(time_to_wait):
    # CLEAR: S2: HIGH, S3: LOW
    # Set S2 to HIGH and S3 to LOW to capture clear
    GPIO.output(S2,GPIO.HIGH)
    GPIO.output(S3,GPIO.LOW)
    
    # Sleep to let give software/hardware a chance to switch?
    time.sleep(0.3)
    
    elapsed_time = 0
    num_cycles = 0
    

    # While loop stops when time_to_wait is hit
    # Get Elapsed Time, increment num_cycles
    # Get start time.

    start = time.monotonic()

    while elapsed_time < time_to_wait:
        GPIO.wait_for_edge(SIGNAL, GPIO.FALLING)
        num_cycles += 1
        elapsed_time = time.monotonic() - start
    end = time.monotonic()
    
    duration_external = end - start
    # print(f"duration_external: {duration_external} sec")
    # print(f"elapsed_time: {elapsed_time} sec")
    return num_cycles, duration_external, elapsed_time


# Get RGBC PRF, input: time to wait.
# Manager function that grabs all RGBC colors
def get_rbgc_prf(time_to_wait):
    # print("get_rbgc_prf")

    # Real world:
    # each color would get each value separately: number_of_cycles, external_time, and internal_time

    results = {}
    # Populate dict:
    for color in color_keys:
        results[color] = {}
        for header in prf_keys:
            results[color][header] = []

    # print(json.dumps(results, indent=4))

    # Initialize number_of_cycles, external_time, internal_time to -1, if detected, then color capture failed
    number_of_cycles, external_time, internal_time = -1
    # Real Version
    for color in color_keys:
        # color_keys = ['red', 'green', 'blue', 'clear']
        print(f"Getting color: {color}")
        if color == 'red':
            number_of_cycles, external_time, internal_time = get_red_prf(time_to_wait)
        elif color == 'green':
            number_of_cycles, external_time, internal_time = get_green_prf(time_to_wait)
        elif color == 'blue':
            number_of_cycles, external_time, internal_time = get_blue_prf(time_to_wait)
        elif color == 'clear':
            number_of_cycles, external_time, internal_time = get_clear_prf(time_to_wait)
        
        freq_ext = number_of_cycles / external_time
        freq_int = number_of_cycles / internal_time
        freq_expected = number_of_cycles / time_to_wait
        # Get data for each color
        # Calculate freq_ext, freq_int, freq_expected
        results[color][prf_keys[0]] = number_of_cycles
        results[color][prf_keys[1]] = external_time
        results[color][prf_keys[2]] = internal_time
        results[color][prf_keys[3]] = freq_ext
        results[color][prf_keys[4]] = freq_int
        results[color][prf_keys[5]] = freq_expected

        if number_of_cycles == -1:
            print("***** WARNING: COLOR DETECTION FAILED ******")

    return results


# ------- GUI FUNCTIONs -------

# Setup temp CSV file to save location and colors to.
def setup_temp_folder_and_csv():
    print("Setting up Color Temp Folder/CSV")
    if not os.path.isdir(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)
        print(f"Folder does not exist, making directory: {TEMP_FOLDER}")

    # Make newline be blank, prevents extra empty lines from happening
    f = open(TEMP_FULL_PATH, 'w', newline="")
    writer = csv.writer(f)

    # Create headers
    headers = ["X", "Y", "Z"]
    # Write Colors Headers (temporary for now, will add more later)
    for color in color_keys:
        headers.append(color)
    writer.writerow(headers)
    f.close()


# Save loc/color to CSV
def save_color_to_csv(loc_dict):
    print("Saving Color and Location to CSV")
    results = get_rbgc_prf(TIME_TO_WAIT)
    
    row = []
    
    # Add x/y/z location to csv row
    for key, value in loc_dict.items():
        print(key, value)
        row.append(value)
    
    for color in color_keys:
        temp = results[color][prf_keys[0]]
        print(f"{color}: {temp} Hz")
        row.append(temp)
    
    print(f"row: {row}")
    
    # Ready to save data to CSV
    # Make newline be blank, prevents extra empty lines from happening
    f = open(TEMP_FULL_PATH, 'a', newline="")
    writer = csv.writer(f)
    
    writer.writerow(row)

    f.close()
    print("File Saved")
    
    pass


def get_gui_tab_layout():

    x_loop_controls_dict = {
                                "title": "Input X Range Color Capture Parameters (Units are in mm):",
                                "size": (5, 1),
                                "button": X_LOOP_BUTTON,
                                "start": {
                                    "text": "X Start:",
                                    "key": X_START_KEY,
                                    "default": "0"
                                },
                                "end": {
                                    "text": "X End:",
                                    "key": X_END_KEY,
                                    "default": "2"
                                },
                                "inc": {
                                    "text": "X Inc:",
                                    "key": X_INC_KEY,
                                    "default": "0.5"
                                }
                           }

    y_loop_controls_dict = {
                                "title": "Input Y Range Color Capture Parameters (Units are in mm):",
                                "size": (5, 1),
                                "button": Y_LOOP_BUTTON,
                                "start": {
                                    "text": "Y Start:",
                                    "key": Y_START_KEY,
                                    "default": "0"
                                },
                                "end": {
                                    "text": "Y End:",
                                    "key": Y_END_KEY,
                                    "default": "2"
                                },
                                "inc": {
                                    "text": "Y Inc:",
                                    "key": Y_INC_KEY,
                                    "default": "0.5"
                                }
                           }

    tab_layout = [
                    [sg.Button(SETUP_COLOR_SENSOR), sg.Button(GET_COLOR)],
                    [sg.Button(SAVE_COLOR), sg.Button(STOP_COLOR_SENSOR)],
                    get_loop_controls_layout(x_loop_controls_dict),
                    get_loop_controls_layout(y_loop_controls_dict),
                    get_save_folder_row()
                 ]
    return tab_layout


def color_sensor_event_manager_non_printer(event, values, window):
    print("color_sensor_event_manager_non_printer")
    # COLOR_SENSOR_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, SAVE_COLOR, STOP_COLOR_SENSOR]

    # TODO: Add in x and y color saver. Go in x direction from start to finish, collecting color. Similar to z Stack creator
    # TODO: Choose folder location to save CSV file?
    # TODO: How to save moving 3D printer if this module is for color sensor only.

    # Color Sensor stuff
    if event == SETUP_COLOR_SENSOR:
        print("You pressed Setup Color Sensor")
        # color_sensor_setup()
        # set_100_output()
        # setup_temp_folder_and_csv()
    elif event == GET_COLOR:
        print("You pressed Get Color")
        # colors = get_rbgc_prf(TIME_TO_WAIT)
        # print(colors)
    elif event == STOP_COLOR_SENSOR:
        print("You pressed Stop Color Sensor")
        # end_program()
    pass


# Sample function to be placed into the Main GUI or anything that needs printer control
def color_sensor_event_manager_printer(event, values, window):
    print("color_sensor_event_manager_printer")
    # # Color Sensor Event List for checking if a button is pressed
    # COLOR_SENSOR_ALL_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, SAVE_COLOR, STOP_COLOR_SENSOR]
    #
    # # Non-Printer Events
    # COLOR_SENSOR_NON_PRINTER_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, STOP_COLOR_SENSOR]
    #
    # # Printer Events (Events requiring printer control)
    # COLOR_SENSOR_PRINTER_EVENT_LIST = [SAVE_COLOR, X_LOOP_BUTTON, Y_LOOP_BUTTON]

    if event == SAVE_COLOR:
        print("You pressed Save Color")
        # Need to figure out the logic here, probably put it in the main gui.
        # loc_dict = get_current_location2()
        # save_color_to_csv(loc_dict)
    pass


# Sample function to be placed into the Main GUI or anything that directs to printer and non-printer controls
def color_sensor_event_super_manager(event, values, window):
    print("color_sensor_event_super_manager")
    # # Color Sensor Event List for checking if a button is pressed
    # COLOR_SENSOR_ALL_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, SAVE_COLOR, STOP_COLOR_SENSOR]
    #
    # # Non-Printer Events
    # COLOR_SENSOR_NON_PRINTER_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, STOP_COLOR_SENSOR]
    #
    # # Printer Events (Events requiring printer control)
    # COLOR_SENSOR_PRINTER_EVENT_LIST = [SAVE_COLOR]

    if event in COLOR_SENSOR_NON_PRINTER_EVENT_LIST:
        print("Non Printer Events Detected")
        color_sensor_event_manager_non_printer(event, values, window)
    elif event in COLOR_SENSOR_PRINTER_EVENT_LIST:
        print("Printer Events Detected")
        color_sensor_event_manager_printer(event, values, window)

    pass


# Generic loop control PySimpleGUI layout
def get_loop_controls_layout(loop_controls_dict):

    loop_control_title = loop_controls_dict["title"]

    start_text = loop_controls_dict["start"]["text"]
    start_key = loop_controls_dict["start"]["key"]
    start_default = loop_controls_dict["start"]["default"]

    end_text = loop_controls_dict["end"]["text"]
    end_key = loop_controls_dict["end"]["key"]
    end_default = loop_controls_dict["end"]["default"]

    inc_text = loop_controls_dict["inc"]["text"]
    inc_key = loop_controls_dict["inc"]["key"]
    inc_default = loop_controls_dict["inc"]["default"]

    input_text_size = loop_controls_dict["size"]

    # Button Text (also works as Button Event)
    start_button = loop_controls_dict["button"]

    layout = [
                [sg.Text(loop_control_title)],
                [sg.Text(start_text), sg.InputText(start_default, size=input_text_size, enable_events=True, key=start_key),
                 sg.Text(end_text), sg.InputText(end_default, size=input_text_size, enable_events=True, key=end_key),
                 sg.Text(inc_text), sg.InputText(inc_default, size=input_text_size, enable_events=True, key=inc_key),
                 sg.Button(start_button)
                 ]
             ]
    return layout


def get_save_folder_row():

    save_folder_text = "Save Folder Location:"
    save_folder_key = COLOR_SAVE_FOLDER_KEY
    save_input_folder_size = (25, 1)
    save_folder_row = [sg.Text(save_folder_text),
                       sg.In(size=save_input_folder_size, enable_events=True, key=save_folder_key),
                       sg.FolderBrowse()
                       ]
    return save_folder_row


def main():

    populate_color_sensor_all_event_list()

    sg.theme("LightGreen")

    layout = get_gui_tab_layout()

    window = sg.Window("Color Sensor", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event in COLOR_SENSOR_ALL_EVENT_LIST:
            color_sensor_event_super_manager(event, values, window)

    pass


if __name__ == "__main__":
    main()
else:
    # Color Sensor Constants that need populating
    populate_color_sensor_all_event_list()
