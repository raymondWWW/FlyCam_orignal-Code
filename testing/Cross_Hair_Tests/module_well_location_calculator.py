"""
Well Location Calculation GUI

Author: Johnny Duong
Creation Date: 8-27-2022

Description: GUI to help calculate all well plate locations and the snaking path.

Ideas:
-Probably only include snaking path.

Changelog:
8-27-2022:
"""

# Import Statements
import PySimpleGUI as sg

# Constants

# GUI Events and Default Values

# ==== USER DEFINED FUNCTIONS ====


# Get Layout


# Event Manager


# Well Location Calculation Functions


# Main Function

def main():
    print("main")

    # Setup Theme
    sg.theme("LightGreen")

    # Setup Layout
    layout = [[sg.Text("Well Plate Locations Generator")]]

    # Setup Window
    window = sg.Window("Well Plate Location Generator", layout)

    # Setup GUI While Loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

    print("Closing GUI...")


    pass


if __name__ == "__main__":
    main()
