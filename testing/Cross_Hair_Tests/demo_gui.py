"""
Demo GUI
Author: Johnny Duong
Date: 8-16-2022

Grant: Blah blah

Changelog:
"""

import PySimpleGUI as sg


BUTTON_LABEL_TOO = "A Button That Smiles"


def main():
    print("Main")

    # Setup Theme
    sg.theme("LightGreen")

    # Setup Layout
    layout_demo = [[sg.Button(BUTTON_LABEL_TOO)]]

    # Setup Window
    window = sg.Window("A Title", layout=layout_demo)

    # Setup GUI While Loop
    while True:
        # Read window contents, store into event and values variable.
        event, values = window.read()

        # If closed, break out of loop
        if event == sg.WIN_CLOSED:
            break
        elif event == BUTTON_LABEL_TOO:
            print("You pressed a button")
    pass


if __name__ == "__main__":
    main()
