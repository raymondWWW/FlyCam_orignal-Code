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
import settings as C
import get_current_location_m114 as GCL
import printer_connection as printer

# define main function
def main():

    # Setup Camera
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
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

    sg.theme("LightGreen")

    # Define Window Layout
    layout = [
        [sg.Image(filename='', key='-IMAGE-')],
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
    
    # This for loop may cause problems if the camera feed dies, it will close everything?
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # while True:
        event, values = window.read(timeout=20)
        
        frame = frame.array
        
        if event == sg.WIN_CLOSED:
            break
        elif event == "Get Current Location":
            print("===================================")
            print("You pressed Get Current Location!")
            printer.run_gcode("M114")
            serial_string = printer.get_serial_data()
            if GCL.does_location_exist_m114(serial_string) == True:
                current_location_dictionary, is_location_found = GCL.parse_m114(serial_string)
                print(current_location_dictionary)
                printer.printer.flush()
            else:
                print("Location Not Found, Try Again")
                printer.printer.flush()
        elif event == "Up":
            print("You pressed Up!")
            printer.run_gcode("G91")
            printer.run_gcode("G0Y1.00")
        elif event == "Down":
            print("You pressed Down!")
            printer.run_gcode("G91")
            printer.run_gcode("G0Y-1.00")
        elif event == "Left":
            print("You pressed Left!")
            printer.run_gcode("G91")
            printer.run_gcode("G0X-1.00")
        elif event == "Right":
            print("You pressed Right!")
            printer.run_gcode("G91")
            printer.run_gcode("G0X1.00")
        elif event == "z-":
            print("You pressed z-!")
            printer.run_gcode("G91")
            printer.run_gcode("G0Z-1.00")
        elif event == "z+":
            print("You pressed z+!")
            printer.run_gcode("G91")
            printer.run_gcode("G0Z1.00")
        
        # print("You entered ", values[0])
        # Original
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        
        # Update GUI Window with new image
        window['-IMAGE-'].update(data=imgbytes)
        
        # clear the stream in preparation for the next frame
        # Must do this, else it won't work
        rawCapture.truncate(0)

    window.close()
    # For loop to show camera feed
    pass

main()
# call main function
