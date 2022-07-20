"""
Module for setting how long to run experiment

TODO:
Two Different Times to keep track of:
-How long to keep collecting images (24 hours?)
-How much time to wait in between runs?

"""

import PySimpleGUI as sg


DEFAULT_HOURS = "1"
DEFAULT_MIN = "10"

HOURS_KEY = "-HOURS-"
MIN_KEY = "-MIN-"

TIME_KEY_LIST = [HOURS_KEY, MIN_KEY]

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
                    [sg.Text("Experiment Run Time:")],
                    [sg.Text("Hour(s):"), sg.InputText(DEFAULT_HOURS, size=time_size, enable_events=True, key=HOURS_KEY)],
                    [sg.Text("Min (s): "), sg.InputText(DEFAULT_MIN, size=time_size, enable_events=True, key=MIN_KEY)],
                  ]
    return time_layout


def get_hour_min(event, values, window):
    hours = int(values[HOURS_KEY])
    minutes = int(values[MIN_KEY])
    print(f"Experiment will run for {hours} hours and {minutes} minutes")
    
    # Convert to seconds for time.sleep()
    seconds = hours*60*60 + minutes*60
    print(f"or experiment will run for {seconds} seconds")


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
