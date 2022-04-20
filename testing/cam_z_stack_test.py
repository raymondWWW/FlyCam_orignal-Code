"""
Test Code for Z-Stack Capturing using a Raspberry Pi, Camera, and 3D printer.

Test code will only be algorithm that does not include camera and 3D printer.

Algorithm:
-Gets Current Location, assumes sending out of dictionary with location X, Y, and Z (gets z_current)
   - For actual, will have to be called twice to remove old location?
-Runs for loop with z_start, z_end and z_increment
   -z_current will be used in saving image file. Filename format: image_[z].jpg
   -For loop converts z_current float to GCODE string (if I have code that does this, use that)
-Saves images to a unique folder that is created (use my modification of Adrian's code for this)
-GUI:
  -allows user to set z_start, z_end and z_increment
  -Has button to start z_stack creation
  -is a different tab
  -Optional: Displays current location and allows user to input x/y/z for absolute input

Optional:
-Create function to convert float x/y/z to GCODE, and send GCODE.
"""

import PySimpleGUI as sg


def main():

    # Setup GUI Layout

    # Layout contents:
    #   Text that says unit is in mm
    #   Text boxes for in z_start, z_end, z_increment
    #   Folder Selection of where to save folder
    #   Button to "Create Z Stack"

    layout_z_stack = [ [sg.Text("Units are in mm")]]



    # Initiliaze GUI Window

    # Run forever while loop to start GUI
    pass


if __name__ == "__main__":
    main()
