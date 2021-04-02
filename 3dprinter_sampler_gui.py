"""
Graphical User Interface for using the 3D Printer to take picture/video samples

Current Goals:
-Has Camera Feed
-Can move X, Y, Z of 3D Printer
-Can get Current Location of Extruder Nozzle
"""

# Import PySimpleGUI, cv2, numpy, time libraries
# Import picamera libraries

from picamera.array import PiRGBArray
from picamera import PiCamera
import PySimpleGUI as sg
import cv2
import numpy as np
import time

# Import modules
import get_current_location_m114 as GCL
import printer_connection as printer

# define main function
def main():

    # Setup Camera
    
    
    # Setup 3D Printer
    csv_filename = "testing/file2.csv"
    path_list = printer.get_path_list_csv(csv_filename)
    printer.initial_setup(path_list)

    sg.theme("LightGreen")

    # Define Window Layout
    layout = [
        [sg.Text("Video PlaceHolder", size=(60, 1), justification="center")],
        [sg.Text("", size=(3, 1)), sg.Button("Get Current Location", size=(20, 1))],
        [sg.Text("", size=(5, 1)), sg.Button("Up", size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button("z-", size=(5, 1))],
        [sg.Button("Left", size=(10, 1)), sg.Button("Right", size=(10, 1))],
        [sg.Text("", size=(5, 1)), sg.Button("Down", size=(10, 1)), sg.Text("", size=(5, 1)), sg.Button("z+", size=(5, 1))]
    ]
    # Have Camera Feed Window
    # To the right, xy, and z
    # Below camera Feed: Show Current Location, Get Current Location Button


    # Create window and show it without plot
    window = sg.Window("3D Printer GUI Test", layout, location=(800, 400))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "Get Current Location":
            print("You pressed Get Current Location!")
        elif event == "Up":
            print("You pressed Up!")
        elif event == "Down":
            print("You pressed Down!")
        elif event == "Left":
            print("You pressed Left!")
        elif event == "Right":
            print("You pressed Right!")
        elif event == "z-":
            print("You pressed z-!")
        elif event == "z+":
            print("You pressed z+!")
        # print("You entered ", values[0])

    window.close()
    # For loop to show camera feed
    pass

main()
# call main function