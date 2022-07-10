"""
Module for Color Sensor

To be used by the GUI

Code Sources:
https://www.geeksforgeeks.org/how-to-set-the-spacing-between-subplots-in-matplotlib-in-python/
https://matplotlib.org/stable/gallery/pyplots/fig_axes_labels_simple.html
https://www.geeksforgeeks.org/numpy-arrange-in-python/

"""
import csv
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PySimpleGUI as sg

import random

# TODO: Uncomment when actually running module in GUI
# import RPi.GPIO as GPIO
import time

import os
from os.path import join

from datetime import datetime

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
loc_keys = ["x", "y", "z"]
prf_keys = ["number_of_cycles", "external_time", "internal_time", "freq_ext", "freq_int", "freq_expected"]
RED = color_keys[0]; GRN = color_keys[1]; BLU = color_keys[2]; CLR = color_keys[3]
X = loc_keys[0]; Y = loc_keys[1]; Z = loc_keys[2]
NUM_CYCLES = prf_keys[0]
FREQ_EXP = prf_keys[5]

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
COLOR_SAVE_DEFAULT_FOLDER = r'D:\Projects\3dprinter_sampling\testing\Color Sensor'

# Non-Printer Events
COLOR_SENSOR_NON_PRINTER_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, STOP_COLOR_SENSOR]

# Printer Events (Events requiring printer control)
COLOR_SENSOR_PRINTER_EVENT_LIST = [SAVE_COLOR, X_LOOP_BUTTON, Y_LOOP_BUTTON]

# Color Sensor Event List for checking if a button is pressed
COLOR_SENSOR_ALL_EVENT_LIST = []

# For Plots
MAX_ROW = 2
MAX_COL = 2


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
    elif event in [X_LOOP_BUTTON, Y_LOOP_BUTTON]:
        printer_loop(event, values, window)


def printer_loop(event, values, window):
    # Assumes X_LOOP and Y_LOOP events were already checked

    # Create only 1 figure (num=1), and clear the plot so it can be reused
    # Helps prevent memory leaks, but may be annoying since you may want to see previous plots.
    fig, axs = plt.subplots(MAX_ROW, MAX_COL, constrained_layout=True, num=1, clear=True)

    if event == X_LOOP_BUTTON:
        printer_x_loop(event, values, window, fig, axs)
    elif event == Y_LOOP_BUTTON:
        printer_y_loop(event, values, window, fig, axs)
    # May need a Z_LOOP_BUTTON in the future
    pass


def printer_x_loop(event, values, window, fig, axs):
    print(f"You pressed: {X_LOOP_BUTTON}")
    # TODO: Add in plot function for both
    # Algorithm:
    start = float(values[X_START_KEY])
    end = float(values[X_END_KEY])
    inc = float(values[X_INC_KEY])
    # Take start/end/inc
    # TODO: Get Current Location
    # Dummy Data for y/z
    y = 0
    z = 0
    # TODO: Move to first location
    # initialize_data_dict()
    data_dict = initialize_data_dict()
    # Run for loop going through that
    for x in np.arange(start, end+inc, inc):
        # print(x)
        # TODO: Move Printer to location
        # TODO: Wait sleep time
        # Get Color
        # Get current location?
        # Append color and location to dictionary lists.
        data_dict[X].append(x)
        data_dict[Y].append(y)
        data_dict[Z].append(z)

        # Dummy data
        data_dict[RED].append(random.randint(8000, 24000))
        data_dict[BLU].append(random.randint(8000, 24000))
        data_dict[GRN].append(random.randint(8000, 24000))
        data_dict[CLR].append(random.randint(8000, 24000))

    # At end of loop, create dataframe, save to file
    df = pd.DataFrame.from_dict(data_dict)
    # print(df)

    # Get Save Folder
    save_folder = values[COLOR_SAVE_FOLDER_KEY]
    save_file_name = f"color_loc_{get_unique_id()}.csv"

    # Create save full path
    save_full_path = join(save_folder, save_file_name)
    print(f"save_full_path: {save_full_path}")

    # Save to CSV
    df.to_csv(save_full_path)

    # Show 4 RGBC Freq plots on on plot

    # Get x-axis data, will always to x location
    x_axis = df[X]

    # Init counter variable for getting color key
    counter = 0

    # Populate each of the subplots (should be a 2x2)
    for i in range(MAX_ROW):
        # Plot dataframe
        for j in range(MAX_COL):
            # Grab Color Key
            color = color_keys[counter]

            # Grab frequency values from the color column
            # Note: Is different from how the results is outputted!
            y_axis = df[color]

            # Create scatter plot
            axs[i, j].scatter(x_axis, y_axis)
            axs[i, j].set_title(f"{color} freq")
            xlabel_text = f"x loc (mm)"
            axs[i, j].set_xlabel(xlabel_text)
            counter += 1

    plt.suptitle("RGBC Location vs Color Frequency")
    # Show plot, but allow GUI to continue to work.
    plt.show(block=False)


def printer_y_loop(event, values, window, fig, axs):
    print(f"You pressed: {Y_LOOP_BUTTON}")
    # Algorithm:
    start = float(values[Y_START_KEY])
    end = float(values[Y_END_KEY])
    inc = float(values[Y_INC_KEY])
    # Take start/end/inc
    # TODO: Get Current Location
    # Dummy Data for y/z
    x = 0
    z = 0
    # TODO: Move to first location
    # initialize_data_dict()
    data_dict = initialize_data_dict()
    # Run for loop going through that
    for y in np.arange(start, end+inc, inc):
        # print(x)
        # TODO: Move Printer to location
        # TODO: Wait sleep time
        # Get Color
        # Get current location?
        # Append color and location to dictionary lists.
        data_dict[X].append(x)
        data_dict[Y].append(y)
        data_dict[Z].append(z)

        # Dummy data
        data_dict[RED].append(random.randint(8000, 24000))
        data_dict[BLU].append(random.randint(8000, 24000))
        data_dict[GRN].append(random.randint(8000, 24000))
        data_dict[CLR].append(random.randint(8000, 24000))

    # At end of loop, create dataframe, save to file
    df = pd.DataFrame.from_dict(data_dict)
    # print(df)

    # Get Save Folder
    save_folder = values[COLOR_SAVE_FOLDER_KEY]
    save_file_name = f"color_loc_{get_unique_id()}.csv"

    # Create save full path
    save_full_path = join(save_folder, save_file_name)
    print(f"save_full_path: {save_full_path}")

    # Save to CSV
    df.to_csv(save_full_path)

    # Show 4 RGBC Freq plots on on plot

    # Get x-axis data, will always to x location
    x_axis = df[Y]

    # Init counter variable for getting color key
    counter = 0

    # Populate each of the subplots (should be a 2x2)
    for i in range(MAX_ROW):
        # Plot dataframe
        for j in range(MAX_COL):
            # Grab Color Key
            color = color_keys[counter]

            # Grab frequency values from the color column
            # Note: Is different from how the results is outputted!
            y_axis = df[color]

            # Create scatter plot
            axs[i, j].scatter(x_axis, y_axis)
            axs[i, j].set_title(f"{color} freq")
            xlabel_text = f"y loc (mm)"
            axs[i, j].set_xlabel(xlabel_text)
            counter += 1

    plt.suptitle("RGBC Location vs Color Frequency")
    # Show plot, but allow GUI to continue to work.
    plt.show(block=False)


# For saving color and location data
def initialize_data_dict():
    # Initialize Data Dictionart to store location and color data
    # Format: data_dict = {"x": [], "y": [], "z": [], "red": [], "green": [], "blue": [], "clear": []}
    data_dict = {}
    for loc in loc_keys:
        data_dict[loc] = []

    for color in color_keys:
        data_dict[color] = []

    # print(data_dict)
    return data_dict


# Define function to create unique text string using date and time.
def get_unique_id():
    current_time = datetime.now()
    unique_id = current_time.strftime("%Y-%m-%d_%H%M%S")
    # print(f"unique_id: {unique_id}")
    return unique_id


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
                       sg.In(COLOR_SAVE_DEFAULT_FOLDER, size=save_input_folder_size, enable_events=True, key=save_folder_key),
                       sg.FolderBrowse()
                       ]
    return save_folder_row


def main():

    # Sample GUI for testing

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
