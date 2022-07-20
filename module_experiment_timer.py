"""
Module for setting how long to run experiment

TODO:
-Create sample loop like Arduino?
-Create sample loop using time.sleep?

Changelog:
7-19-2022: Added in functions to create layout, check for digits, and to collect time values.
"""

import PySimpleGUI as sg


DEFAULT_TOTAL_HOURS = "1"
DEFAULT_TOTAL_MIN = "10"
DEFAULT_RUN_MIN = "5"

TOTAL_HOURS_KEY = "-HOURS-"
TOTAL_MIN_KEY = "-MIN-"
RUN_MIN_KEY = "-RUN_MIN-"

TIME_KEY_LIST = [TOTAL_HOURS_KEY, TOTAL_MIN_KEY, RUN_MIN_KEY]


# Define function to check an InputText key for digits only
def check_for_digits_in_key(key_str, window, event, values):
    
    # TODO: Add in character check in all of number string.
    if event == key_str and len(values[key_str]) and values[key_str][-1] not in ('0123456789'):
            # delete last char from input
            # print("Found a letter instead of a number")
            window[key_str].update(values[key_str][:-1])


def get_time_layout():
    time_size = (3, 1)
    
    time_layout = [
                    [sg.Text("How long will I collect pictures?")],
                    [sg.Text("Hour(s):"), sg.InputText(DEFAULT_TOTAL_HOURS, size=time_size, enable_events=True, key=TOTAL_HOURS_KEY)],
                    [sg.Text("Min(s) : "), sg.InputText(DEFAULT_TOTAL_MIN, size=time_size, enable_events=True, key=TOTAL_MIN_KEY)],
                    [sg.Text("How long will I wait between each run?")],
                    [sg.Text("Min(s) : "), sg.InputText(DEFAULT_RUN_MIN, size=time_size, enable_events=True, key=RUN_MIN_KEY)]
                  ]
    return time_layout


def get_hour_min(event, values, window):
    # Assumes values found in the InputText are integers.
    # Demonstrates that the time values are collected.

    total_hours = int(values[TOTAL_HOURS_KEY])
    total_minutes = int(values[TOTAL_MIN_KEY])
    print(f"Experiment will run for {total_hours} hours and {total_minutes} minutes")
    
    # Convert to seconds for time.sleep()
    total_seconds = total_hours*60*60 + total_minutes*60
    print(f"or experiment will run for {total_seconds} seconds")

    run_minutes = int(values[RUN_MIN_KEY])
    print(f"After collecting data from wells, will wait {run_minutes} minutes before collecting data again")


def main():
    print("main")
    
    # Set up theme
    sg.theme("LightGreen")
    
    time_size = (3, 1)
    
    # Set up layout
    layout = [
                get_time_layout(),
                [sg.Button("Start")]
             ]
    
    # Set up window
    window = sg.Window("Time GUI", layout)
    
    # While loop for GUI
    while True:
        event, values = window.read()
        
        for time_key in TIME_KEY_LIST:
            check_for_digits_in_key(time_key, window, event, values)
        
        if event == sg.WIN_CLOSED:
            break
        elif event == "Start":
            print("Pressed Start")
            get_hour_min(event, values, window)
    
    pass


if __name__ == "__main__":
    main()
