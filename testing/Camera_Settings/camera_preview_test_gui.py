"""
Test Preview Script for PiCamera

Ideas:
-Turn on/off Fullscreen Mode?
-Use Linux Window management to allow user to move Camera Preview?

Allow float or int in InputText idea:
-Search for non-integer, delete
-Search for all periods, delete all except for one?
  -Float idea: or use two InputText boxes, example: [  ].[  ]
-How to limit to only x number of numbers?
-How to auto select all text when clicking in InputText the first time?

Changelog:
12 May 2022: Can control PiCamera Preview Window: Location, Preview Size, and Alpha (Opacity).
             Turns off fullscreen mode.
"""

from picamera import PiCamera

import cv2
import PySimpleGUI as sg
import time


# GUI KEYS
PREVIEW_LOC_X_KEY = "-PREVIEW LOC X KEY-"
PREVIEW_LOC_Y_KEY = "-PREVIEW LOC Y KEY-"
PREVIEW_WIDTH_KEY = "-PREVIEW WIDTH KEY-"
PREVIEW_HEIGHT_KEY = "-PREVIEW HEIGHT KEY-"
ALPHA_KEY = "-ALPHA KEY-"
PREVIEW_KEY_LIST = [PREVIEW_LOC_X_KEY, PREVIEW_LOC_Y_KEY, PREVIEW_WIDTH_KEY, PREVIEW_HEIGHT_KEY, ALPHA_KEY]

# Button Text
START_PREVIEW = "Start Preview"
STOP_PREVIEW = "Stop Preview"


# Define function to check an InputText key for digits only
def check_for_digits_in_key(key_str, window, event, values):
    
    if event == key_str and len(values[key_str]) and values[key_str][-1] not in ('0123456789'):
            # delete last char from input
            # print("Found a letter instead of a number")
            window[key_str].update(values[key_str][:-1])


def main2():
    print("Main2")
    
    # Setup PiCamera
    width = 640
    height = 480
    
    camera = PiCamera()
    camera.resolution = (width, height)
    camera.framerate = 32
    
    # Setup PySimpleGUI theme
    sg.theme("LightGreen")
    
    # Setup layout
    layout = [[sg.Text("Preview Location (e.g. x = 0, y = 0):")],
               [sg.Text("x:"), sg.InputText("0", size=(8, 1), enable_events=True, key=PREVIEW_LOC_X_KEY),
                 sg.Text("y:"), sg.InputText("36", size=(8, 1), enable_events=True, key=PREVIEW_LOC_Y_KEY)],
               [sg.Text("Preview Video Size (e.g. width = 640, height = 480):")],
               [sg.Text("width:"), sg.InputText("640", size=(8, 1), enable_events=True, key=PREVIEW_WIDTH_KEY),
                 sg.Text("height:"), sg.InputText("480", size=(8, 1), enable_events=True, key=PREVIEW_HEIGHT_KEY)],
               [sg.Text("Opacity, or Alpha (range 0 (invisible) to 255 (opaque)):"), sg.InputText("255", size=(5, 1), enable_events=True, key=ALPHA_KEY)],
               [sg.Button(START_PREVIEW), sg.Button(STOP_PREVIEW)]
                ]
    
    # Setup window
    window = sg.Window("PiCamera Preview Test", layout, location=(500, 50))
    
    # Setup while loop for GUI
    while True:
        event, values = window.read(timeout=1)
        
        # Check Input Text for integers only
        
        for preview_key in PREVIEW_KEY_LIST:
            check_for_digits_in_key(preview_key, window, event, values)
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        elif event == START_PREVIEW:
            print("Starting Preview With Settings")
            if camera.preview:
                camera.stop_preview()
            prev_width = int(values[PREVIEW_WIDTH_KEY])
            prev_height = int(values[PREVIEW_HEIGHT_KEY])
            prev_loc_x = int(values[PREVIEW_LOC_X_KEY])
            prev_loc_y = int(values[PREVIEW_LOC_Y_KEY])
            alpha_val = int(values[ALPHA_KEY])
            camera.start_preview(alpha=alpha_val, fullscreen=False, window=(prev_loc_x, prev_loc_y, prev_width, prev_height))
        elif event == STOP_PREVIEW:
            print("Stopping Preview")
            camera.stop_preview()
    
    #   If close, break GUI
    #   elif Update Button
    #   elif Start Button
    #   elif Stop Button
    
    window.close()
    camera.close()
    
    
    pass


def main():
    
    width = 640
    height = 480
    
    camera = PiCamera()
    camera.resolution = (width, height)
    camera.framerate = 32
    # rawCapture = PiRGBArray(camera, size=(width, height))
    
    """
    camera.start_preview()
    camera.preview.fullscreen = False
    camera.preview.window = (0, 0, 640, 480)
    """
    
    camera.start_preview(fullscreen=False, window=(0, 0, 640, 480))
    
    time.sleep(5)
    
    camera.stop_preview()
    
    
    pass


if __name__ == "__main__":
    main2()
