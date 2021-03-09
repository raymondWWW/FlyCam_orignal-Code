"""
3D Printer Sampler

Purpose: Opens up path list YAML file,
         goes to each location in path list,
         converts int values to Gcode string,
         then takes picture/records/previews.
"""

# import libraries
# camera, serial, time, yaml
import os
import time
import yaml

from datetime import datetime

# Import module that loads up 3D Printer settings and such
# Note: Bring over YAML files for 3D Printer Settings, and Path List
import settings as C

# Setup camera and printer
# Create printer/camera variables
# camera = picamera.PiCamera()
# camera.rotation = 90
#
# printer = serial.Serial(C.DEVICE_PATH, baudrate = C.BAUDRATE, timeout = C.TIMEOUT_TIME)

# User Defined Functions

# Define initial_setup() function for 3D printer


# Define function, run_gcode_ that runs a GCode string
# Function: Convert String to binary/Gcode, write to serial
def run_gcode(gcode_string):
    # Converts String to Binary UTF-8 Format for GCode Strings
    #  Adds new line character at the end.

    # GCode_string examples:
    #  G28
    #  G1X100Y100

    # Call the global printer variable
    global printer
    # Add new line character at the end of the string
    gcode_string = gcode_string + "\n"

    # print(gcode_string)

    # Convert to Binary with UTF-8 encoding for string, write to serial
    # printer.write(bytes(gcode_string, "utf-8"))
    # printer.write(str.encode(gcode_string))

    # camera.start_preview(fullscreen=False, window=(30, 30, 500, 500))
    # time.sleep(5)
    # camera.stop_preview()

# define function go_home() to go to home coordinates


# Define function to open YAML paths file, then extracts/returns paths list
def get_path_list(yaml_file):
    with open(yaml_file) as file:
        path_list = yaml.load(file, Loader=yaml.FullLoader)
        # print(path_list)
        return path_list


# Function that takes in a path list (not an array or matrix), but a list of lists,
# returns a similar dimension list of gcode formatted strings
def convert_list_to_gcode_strings(path_list):
    X = 0; Y = 1; Z = 2

    # print("convert_list_to_gcode_strings")
    # print(path_list)
    position = "G0"
    gcode_string_list = []
    number_of_locations = len(path_list)

    for location in path_list:
        x = location[X]
        y = location[Y]
        z = location[Z]
        # print(x, y, z)
        gcode_string = "{}X{}Y{}Z{}".format(position, x, y, z)
        # print(gcode_string)
        gcode_string_list.append(gcode_string)
    # print(gcode_string_list)

    # TODO: Can I achieve this with a list comprehension?
    return gcode_string_list
    pass


# Define function, start_experiment with flag isPreviewModeOn, isRecordingModeOn
def start_experiment(gcode_string_list):
    #   If isPreviewModeOn is true, no pictures/video taken, but camera stays on to show location movements
    #   else take picture or video (check isRecordingModeOn flag)

    # Create Folder (based on conditions)
    folder_path = create_and_get_folder_path()

    # Use for loop to go through each gcode string list
    well_number = 1
    for gcode_string in gcode_string_list:
        # print(gcode_string)
        run_gcode(gcode_string)
        if C.isPreviewModeOn == True:
            print("Preview Mode is On, only showing preview camera")
            # camera.start_preview(fullscreen=False, window=(30, 30, 500, 500))
            # time.sleep(5)
            # camera.stop_preview()
        elif C.isVideoCaptureModeOn == True:
            print("Recording Video Footage")
            file_full_path = get_file_full_path(folder_path, well_number)
            # TODO: Change to Video Captures
            # camera.capture(file_full_path)
        elif C.isPictureCaptureModeOn == True:
            print("Taking Pictures Only")
            file_full_path = get_file_full_path(folder_path, well_number)
            # TODO: Look up Camera settings to remove white balance (to deal with increasing brightness)

            # UNCOMMENT THIS
            # camera.capture(file_full_path)
        well_number += 1


# Define function that creates folder for experiment if VideoCapture or PictureCapture is on
# returns folder path too
# Creates a unique folder name using current date and time
def create_and_get_folder_path():
    # Get Folder Path
    folder_path = "{}{}".format(C.FOLDERPATH, C.FOLDERNAME_PREFIX)
    # print(folder_path)
    current_time = datetime.now()
    folder_name_suffix = current_time.strftime("%Y-%m-%d_%H%M%S")
    # print(folder_name_suffix)

    folder_path_complete = ""

    if C.isVideoCaptureModeOn == True:
        print("Recording Video Footage")
        folder_path_complete = "{}_Videos_{}".format(folder_path, folder_name_suffix)
        print(folder_path_complete)
    elif C.isPictureCaptureModeOn == True:
        folder_path_complete = "{}_Pictures_{}".format(folder_path, folder_name_suffix)
        print("Taking Pictures Only")

    # Check if folder exists, if not, create it
    if not os.path.isdir(folder_path_complete):
        print("Folder Does NOT exist! Making New Folder")
        os.mkdir(folder_path_complete)
    else:
        print("Folder Exists")

    # Return Folder Path
    return folder_path_complete


# Define function that creates the full file path to save video or pictures (folder and file name)
# Creates a unique file name using current date and time
def get_file_full_path(folder_path, well_number):
    current_time = datetime.now()
    # file_name_suffix = current_time.strftime("%Y-%m-%d_%H%M%S_%f")
    file_name_suffix = current_time.strftime("%Y-%m-%d_%H%M%S")
    file_name_full = "well{}_{}.jpg".format(well_number, file_name_suffix)
    file_full_path = "{}/{}".format(folder_path, file_name_full)
    # print(file_full_path)
    return file_full_path

# Define function that checks status of extruder
# TODO: Future feature


# Define function, main, to run things
def main():
    # initial_setup()
    yaml_file = "path_list_2x3_all.yaml"
    path_list = get_path_list(yaml_file)
    gcode_string_list = convert_list_to_gcode_strings(path_list)
    start_experiment(gcode_string_list)
    pass


main()
