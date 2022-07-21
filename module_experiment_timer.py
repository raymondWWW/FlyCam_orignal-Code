"""
Module for setting how long to run experiment

TODO:
-Create sample loop like Arduino?
-Create sample loop using time.sleep?
- Display time left until next run and time left until experiment is done.

Changelog:
7-19-2022: Added in functions to create layout, check for digits, and to collect time values.
"""

import PySimpleGUI as sg
import time

DEFAULT_TOTAL_HOURS = "0"
DEFAULT_TOTAL_MIN = "3"
DEFAULT_RUN_MIN = "1"

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
    run_seconds = run_minutes * 60
    print(f"After collecting data from wells, will wait {run_minutes} (or {run_seconds} seconds) minutes before collecting data again")

    # Dummy values for fasting code testing
    total_seconds = 16
    run_seconds = 5
    demo_start_experiment_1(total_seconds, run_seconds)


def demo_start_experiment_1(total_seconds, run_seconds):
    print("demo_start_experiment_1")
    # Practice function to practice
    # While loop using time.sleep to pause the script

    # TODO: Display time left until end of experiment and time left until next run.

    # demo location list init
    location_list = [1, 2, 3, 4]

    # Init start time variable
    start = time.monotonic()

    # Init location index to zero
    location_index = 0

    elapsed_seconds = -1

    counter = 0

    # While elapsed time is less than total time
    while elapsed_seconds < total_seconds:
        #  Go to location (print it out)
        # print(location_list[location_index])
        # time.sleep(1)
        # location_index += 1

        print(f"Run #{counter}")
        for loc in location_list:
            print(loc)
            time.sleep(1)

        #  Get current time
        current_time = time.monotonic()

        #  Calculate elapsed time (current - start)
        elapsed_seconds = current_time - start

        print(f"elapsed_seconds: {elapsed_seconds:.2f}")

        # if location_index >= len(location_list):
        #     location_index = 0
            # break  # temp

        #  time.sleep and wait run_seconds

        # Note: Caused GUI to pause and you can't interact with it!
        #       May need threading, which is what my GUI does.

        # TODO: Figure out how to avoid putting this if statement here.
        if elapsed_seconds < total_seconds:
            print(f"Will wait {run_seconds} seconds until collecting data again")
            time.sleep(run_seconds)

        counter += 1

    print("Done running experiment")


    #  iterate location index by one or reset to zero if hit end of list.


    pass


def demo_start_experiment_2():
    # While loop using time.monotonic to activate certain conditions the script
    pass


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
