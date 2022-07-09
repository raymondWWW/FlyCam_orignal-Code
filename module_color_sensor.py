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

# Color Sensor Event List for checking if a button is pressed
COLOR_SENSOR_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, SAVE_COLOR, STOP_COLOR_SENSOR]


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
    tab_layout = [
                    [sg.Button("Setup Color Sensor"), sg.Button("Get Color")],
                    [sg.Button("Save Color"), sg.Button("Stop Color Sensor")]
                  ]
    return tab_layout


def color_sensor_event_manager(event, values, window):

    # COLOR_SENSOR_EVENT_LIST = [SETUP_COLOR_SENSOR, GET_COLOR, SAVE_COLOR, STOP_COLOR_SENSOR]

    # TODO: Add in x and y color saver. Go in x direction from start to finish, collecting color. Similar to z Stack creator
    # TODO: Choose folder location to save CSV file?
    # TODO: How to save moving 3D printer if this module is for color sensor only.

    pass


def main():

    sg.theme("LightGreen")

    layout = get_gui_tab_layout()

    window = sg.Window("Color Sensor", layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event in COLOR_SENSOR_EVENT_LIST:
            print("Found a Color Sensor Event")

    pass


if __name__ == "__main__":
    main()
